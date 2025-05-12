from impostazioni import SettingsUI
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Combobox
from ttkbootstrap.widgets import Checkbutton
from ttkbootstrap.widgets import Label
import json
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime


class UI():
    def __init__(self):
        self.root = None
        self.settingsUi = SettingsUI(self.root, self.aggiornaAziende)
        self.aziende = self.loadAziende()
        self.articoli = ["Lenzuola", "CopriMaterasso", "Federa"]
        self.listButtons = []
        self.cbVars = []
        self.selAll = None
        self.aziendaCB = None
        self.artCount = {}
        self.artCombo = []
        self.counts = []

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


    def BuildUi(self):
        self.root = ttk.Window(themename="darkly")
        self.root.title("Smistatore")
        self.root.geometry("1100x500")
        self.root.resizable(False, False)
        self.comboList = []
        self.selAll = ttk.BooleanVar(value=False)

        
        toolbar = ttk.Frame(self.root, bootstyle="secondary")
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        newBtn = ttk.Button(toolbar, text="Nuovo", bootstyle=PRIMARY)
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
        style.configure("title.TLabel", background = "#2d2d2d" ,foreground="orange")
        style.configure("lbl.TLabel", background = "#2d2d2d" ,foreground="white")


        def creaBuche():
            for i in range(10):
                
                
                bucaId = i+1


                colonna = i % 5
                riga = i // 5
                x = (200 * colonna) + (10*colonna)
                y = 50 + (riga * 200) + (20 * riga)
                frame = ttk.Frame(self.root, style="Custom.TFrame", borderwidth=2, relief="solid")
                frame.place(x=x, y=y, width=200, height=200)
                
                nList = ["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto", "Nove", "Dieci"]
                n = nList[i]

                bucaLbl = ttk.Label(frame, text = f"Buca {n}", style = "title.TLabel") #<----------- METTERE FONT ARIAL E BOLD
                bucaLbl.place(x = 5, y = 5)

                articoliLbl = Label(frame, text = "Articolo: ", style = "lbl.TLabel")
                articoliLbl.place(x = 5, y = 45)

                comboB = Combobox(frame, values= self.articoli, style ="info", state="readonly")
                comboB.set(self.articoli[0])
                comboB.place(x = 60, y = 40, height=30, width=130)

                count = 1 if i == 9 else i  #***************************QUESTO COUNT PER IL MOMENTO è SOLO UN PLACEHOLDER <------------

                countLbl = Label(frame, text = f"Count: {count}", style = "lbl.TLabel")
                countLbl.place(x = 80, y = 120)

                self.artCombo.append(comboB)
                self.counts.append(count)

        creaBuche()

    def associaCount(self):
        pass

    def saveData(self):
        self.artCount = {}
        for i in range(len(self.artCombo)):
            articolo = self.artCombo[i]
            if articolo.get() in self.artCount:
                self.artCount[articolo.get()] += self.counts[i]
            else:                  
                self.artCount[articolo.get()] = self.counts[i]

        print(self.artCount)

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
        data = f"{oggi.year}-{oggi.month}-{oggi.day}"

        nomePDF = cliente + " " + data + ".pdf"
        self.crea_pdf(nomePDF, cliente, artCliente)


        cur.close()
        conn.close()


    def aggiornaAziende(self):
        self.aziende = self.loadAziende()
        self.aziendaCB['values'] = self.aziende
        if self.aziende:
            self.aziendaCB.set(self.aziende[0])

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
