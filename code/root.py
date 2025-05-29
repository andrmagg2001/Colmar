#ULTIMO COMMENTO ADNREA CULO
from impostazioni import SettingsUI

import threading
import RPi.GPIO as GPIO
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Combobox
from ttkbootstrap.widgets import Checkbutton
from ttkbootstrap.widgets import Label
from ttkbootstrap.widgets import Button
import json
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import sys


class UI():
    def __init__(self):
        self.root = None
        self.settingsUi = SettingsUI(self.root, self.aggiornaAziende)
        self.aziende = self.loadAziende()
        self.articoli = self.loadProdotti()
        self.listButtons = []
        self.cbVars = []
        self.selAll = None
        self.aziendaCB = None
        self.artCount = {}
        self.savedCounts = {}
        self.oldVList = []
        self.artCombo = []
        self.counts = []
        self.counterDict = {}
        self.lblCount = {}
        self.pins = [21,2, 17,24,25,16, 4, 6]
        self.entrato = False
        self.pin_map = {}  # pin → (label, index)
        self.frameList = []
        self.fLabels = []
    
    def loadAziende(self):
        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute("SELECT cliente FROM clienti ORDER BY id ASC")
            risultati = cur.fetchall()
            conn.close()
            return [r[0] for r in risultati]
        except Exception as e:
            print(f"Errore durante il caricamento delle aziende: {e}")
            return []
        
    def loadProdotti(self):
        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute("SELECT prodotto FROM prodotti ORDER BY id ASC")
            risultati = cur.fetchall()
            conn.close()
            return [r[0] for r in risultati]
        except Exception as e:
            print(f"Errore durante il caricamento delle aziende: {e}")
            return []


    def BuildUi(self):
        self.root = ttk.Window(themename="darkly")
        self.root.title("Smistatore")
        self.root.geometry("1100x500")
        self.root.resizable(False, False)
        self.comboList = []
        self.selAll = ttk.BooleanVar(value=False)

        
        toolbar = ttk.Frame(self.root, bootstyle="secondary")
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        newBtn = ttk.Button(toolbar, text="Inizia", bootstyle=PRIMARY, command = lambda : self.threadCounter())
        newBtn.pack(side=ttk.LEFT, padx=20, pady=5)

        saveBtn = ttk.Button(toolbar, text="Salva", bootstyle=SUCCESS, command = lambda: self.saveData())
        saveBtn.pack(side=ttk.LEFT, padx=20, pady=5)

        settingsBtn = ttk.Button(toolbar, text="Impostazioni", bootstyle=INFO,command= self.settingsUi.BuildUi)
        settingsBtn.pack(side=ttk.LEFT, padx=20, pady=5)

        self.aziendaCB = Combobox(toolbar, values = self.aziende, bootstyle = "info", state = "readonly")
        self.aziendaCB.set(self.aziende[0])
        self.aziendaCB.pack(side = LEFT, padx = 20, pady= 5)

        style = ttk.Style()
        style.configure("Custom.TFrame", background="#2d2d2d")
        style.configure("Red.TFrame", background="#8b0000")
        style.configure("Red.TLabel", background="#8b0000", foreground="white")
        style.configure("title.TLabel", background = "#2d2d2d" ,foreground="orange")
        style.configure("lbl.TLabel", background = "#2d2d2d" ,foreground="white")
        style.configure("lbl.TButton", background = "#2d2d2d" ,foreground="white")



        def creaBuche():
            GPIO.setmode(GPIO.BCM)
            #nList = ["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto", "Nove", "Dieci"]

            for i in range(8):
                titolo = self.articoli[i] if i < len(self.articoli) else 'N/D'
                if i > 3:                  #DA TOGLIERE SE LA BUCA 4 VERRA USATA
                    t = i - 1
                    titolo = self.articoli[t] if t < len(self.articoli) else 'N/D'
                colonna = i % 4
                riga = i // 4
                x = (200 * colonna) + (10 * colonna)
                y = 50 + (riga * 200) + (20 * riga)
                frame = ttk.Frame(self.root, style="Custom.TFrame", borderwidth=2, relief="solid")
                frame.place(x=x, y=y, width=200, height=200)

                bucaLbl = ttk.Label(frame, text="N/D" if i == 3 else titolo, style="title.TLabel")
                bucaLbl.place(x=5, y=5)

                articoliLbl = Label(frame, text="Articolo: ", style="lbl.TLabel")
                articoliLbl.place(x=5, y=45)

                comboB = Combobox(frame, values=self.articoli, style="info", state="readonly")
                comboB.set(titolo)
                comboB.place(x=60, y=40, height=30, width=130)

                oldVal = comboB.get()  # Inizializza old_value con il valore corrente

                self.oldVList.append(oldVal)

                def on_combobox_changed(event, i=i):
                    old = self.oldVList[i]
                    print(old)
                    new = comboB.get()
                    count = self.counts[i]

                    # Salva count associato al vecchio articolo
                    if old:
                        if old in self.savedCounts:
                            self.savedCounts[old] += count
                        else:
                            self.savedCounts[old] = count

                    # Reset contatore e label
                    self.counts[i] = 0
                    self.fLabels[i][2].config(text=f"Count: 0")

                    # Aggiorna old_value
                    comboB.old_value = new

                comboB.bind("<<ComboboxSelected>>", on_combobox_changed)

                count = 0
                countLbl = Label(frame, text=f"Count: {count}", style="lbl.TLabel")
                countLbl.place(x=60, y=100)

                stopBtn = Button(frame, text = "Stop", style="btn.TButton", command = self.stopBtnAction)

                self.fLabels.append((bucaLbl, articoliLbl, countLbl, stopBtn))
                self.frameList.append(frame)


                self.artCombo.append(comboB)
                self.counts.append(count)
                
                if i < len(self.pins):
                    pin = self.pins[i]
                    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                    self.pin_map[pin] = (countLbl, i)

        creaBuche()

    def threadCounter(self):
        GPIO.setup(27, GPIO.OUT)
        self.pwm = GPIO.PWM(27, 1000)
        for pin in self.pin_map:
            thread = threading.Thread(target=self.counter, args=(pin,), daemon=True)
            thread.start()

    

    def suona_allarme(self):
        try:
            self.pwm.start(50)
            time.sleep(5)
            self.pwm.stop()
        except Exception as e:
            print("Errore nel suono:", e)

    def counter(self, pin):
        label, idx = self.pin_map[pin]
        start_time = None
        allarme_attivato = False
        stato_prec = GPIO.LOW

        while True:
             stato = GPIO.input(pin)

             if stato == GPIO.HIGH:
                 if stato_prec == GPIO.LOW:
                     # nuova attivazione
                     start_time = None
                     start_time = time.time()
                     allarme_attivato = False

                 if start_time is not None:
                    elapsed = time.time() - start_time
                 else:
                    elapsed = 0

                 if elapsed > 3 and not allarme_attivato:
                     allarme_attivato = True
                     self.sensBlocked(idx)
                     threading.Thread(target=self.suona_allarme, daemon=True).start()

             elif stato == GPIO.LOW and stato_prec == GPIO.HIGH:
                 # rilascio: conta l'evento
                 self.counts[idx] += 1
                 count = self.counts[idx]
                 self.root.after(0, lambda l=label, c=count: l.config(text=f"Count: {c}"))

                 # reset
                 start_time = None
                 allarme_attivato = False

             stato_prec = stato
             time.sleep(0.4)


    def stopBtnAction(self):
        self.stop = True
    
    def sensBlocked(self, n):
        self.stop = False
        self.placed = False
        def toggle_frame_style(i):
            bLbl, artLbl, countLbl, stopBtn = self.fLabels[n]
            if not self.placed:    
                stopBtn.place(x=60, y=150)
                self.placed = True
            if i % 2 == 0:
                self.frameList[n].config(style='Red.TFrame')
                bLbl.config(style='Red.TLabel')
                artLbl.config(style='Red.TLabel')
                countLbl.config(style='Red.TLabel')
            else:
                self.frameList[n].config(style='Custom.TFrame')
                bLbl.config(style='lbl.TLabel')
                artLbl.config(style='lbl.TLabel')
                countLbl.config(style='lbl.TLabel')
            
            if not self.stop:
                self.root.after(300, toggle_frame_style, i + 1) 
            else:
                self.frameList[n].config(style='Custom.TFrame')
                bLbl.config(style='lbl.TLabel')
                artLbl.config(style='lbl.TLabel')
                countLbl.config(style='lbl.TLabel')
                stopBtn.place_forget()
                self.placed = False


        toggle_frame_style(0)

    def modDict(self, key, value):
        self.counterDict[key] += value

    def saveData(self):
        self.artCount = {}
        self.artCount = self.savedCounts.copy()

        print(self.savedCounts)

        for i in range(len(self.artCombo)):
            articolo = self.artCombo[i].get()
            count = self.counts[i]
            if count == 0:
                continue
            if articolo in self.artCount:
                self.artCount[articolo] += count
            else:
                self.artCount[articolo] = count

        #print(self.artCount)

        if self.aziendaCB.get():
            cliente = self.aziendaCB.get()

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("DELETE FROM relazione")

        cur.execute(f"SELECT id FROM clienti WHERE cliente = '{cliente}'")

        result = cur.fetchone()
        if result:
            idCliente = result[0]

        prodotti = {}
        for prodotto in self.artCount:
            if self.artCount[prodotto] != 0:
                cur.execute(f"SELECT id FROM prodotti WHERE prodotto = '{prodotto}'")
                result = cur.fetchone()
                if result:
                    idProd = result[0]
                    prodotti[idProd] = self.artCount[prodotto]
        
        for idPr in prodotti:
            cur.execute("INSERT INTO relazione (idCliente, idProdotto, Quantità) VALUES (?, ?, ?)", (idCliente, idPr, prodotti[idPr]))

        conn.commit()

        cur.execute("""
            SELECT prodotti.prodotto, SUM(relazione.quantità)
            FROM clienti
            JOIN relazione ON relazione.idCliente = clienti.id
            JOIN prodotti ON relazione.idProdotto = prodotti.id
            WHERE clienti.cliente = ?
            GROUP BY prodotti.prodotto;
        """, (cliente,))
        result = cur.fetchall()
        artCliente = {prodotto: quantita for prodotto, quantita in result}
        print(artCliente)

        oggi = datetime.now()
        data = f"{oggi.year}{oggi.month}{oggi.day} - {oggi.hour}-{oggi.minute}"

        nomePDF = cliente + " " + data + ".pdf"
        self.crea_pdf(nomePDF, cliente, artCliente)
        self.savedCounts.clear()


        cur.close()
        conn.close()

        for i, (bucaLbl, articoliLbl, countLbl, stopBtn) in enumerate(self.fLabels):
            self.counts[i] = 0
            countLbl.config(text = f"Count: {self.counts[i]}")

    def aggiornaAziende(self):
        self.aziende = self.loadAziende()
        self.aziendaCB['values'] = self.aziende
        if self.aziende:
            self.aziendaCB.set(self.aziende[0])

        self.articoli = self.loadProdotti()
        for combo in self.artCombo:
            combo['values'] = self.articoli
            # if self.aziende:
            #     self.aziendaCB.set(self.aziende[0])
        

    def crea_pdf(self, nome_file, cliente, articoli):
        c = canvas.Canvas(nome_file, pagesize=A4)
        larghezza, altezza = A4

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, altezza - 100, f"{cliente}")

        c.setFont("Helvetica", 12)
        y = altezza - 130
        for nome, quantita in articoli.items():
            c.drawString(100, y, f"{nome}: {quantita}")
            y -= 20

        c.save()

    


if __name__ == '__main__':
    app = UI()
    app.BuildUi()
    app.root.mainloop()    



