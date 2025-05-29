import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Combobox
from ttkbootstrap.widgets import Checkbutton
from ttkbootstrap.widgets import Frame
from ttkbootstrap.widgets import Label
from ttkbootstrap.widgets import Button
import tkinter.font as tkFont
import sqlite3
import sys
import os

class SettingsUI():
    def __init__(self, root, aggiornaAziende):
        self.root = root
        self.aggiornaAziende = aggiornaAziende
        self.settingsWin = None
        self.aziende = self.loadAziende()
        self.mapWidg = {}


    def saveAziende(self, what, id):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        if id == 'cliente':
            cur.execute("SELECT COUNT(*) FROM clienti WHERE cliente = ?", (what,))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO clienti (cliente) VALUES (?)", (what,))
            else:
                print("Cliente già esistente.")
        elif id == 'prodotto':
            cur.execute("SELECT COUNT(*) FROM prodotti WHERE prodotto = ?", (what,))
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO prodotti (prodotto) VALUES (?)", (what,))
            else:
                print("Prodotto già esistente.")

        conn.commit()

        cur.close()
        conn.close()

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
        self.settingsWin = ttk.Toplevel(self.root)
        self.settingsWin.title("App con Toolbar")
        self.settingsWin.geometry("500x400")

        self.arial = tkFont.Font(family="Arial", size=12, weight="bold")

        toolbar = ttk.Frame(self.settingsWin, bootstyle="secondary")
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        settSec = ttk.Button(toolbar, text="Impostazioni", bootstyle=SUCCESS, command=lambda: self.changeFrame(self.settWin, settSec, listAzieSec, listProds))
        settSec.pack(side=ttk.LEFT, padx=0, pady=0)

        listAzieSec = ttk.Button(toolbar, text="Lista Aziende", bootstyle="primary", command = lambda: self.changeFrame(self.listWin, listAzieSec, settSec, listProds))
        listAzieSec.pack(side=ttk.LEFT, padx=0, pady=0)

        listProds = ttk.Button(toolbar, text="Lista Prodotti", bootstyle="primary", command = lambda: self.changeFrame(self.prodWin, listProds,listAzieSec, settSec))
        listProds.pack(side=ttk.LEFT, padx=0, pady=0)

        #************* SETTINGS WINDOW *************

        self.settWin = ttk.Frame(self.settingsWin)
        self.settWin.pack(fill="both")

        label = ttk.Label(self.settWin, text="Nome Cliente:", font=("Helvetica", 12))
        label.pack(pady=10)

        self.entry_nome = ttk.Entry(self.settWin, width=30)
        self.entry_nome.pack(pady=5)

        save_button = ttk.Button(self.settWin, text="Aggiungi Cliente", bootstyle=SUCCESS, command= lambda: self.salvaSocieta('cliente'))
        save_button.pack(pady=20)


        prodLbl = ttk.Label(self.settWin, text="Nome Prodotto:", font=("Helvetica", 12))
        prodLbl.pack(pady=10)

        self.entryProd = ttk.Entry(self.settWin, width=30)
        self.entryProd.pack(pady=5)

        saveProdbutton = ttk.Button(self.settWin, text="Aggiungi Prodotto", bootstyle=SUCCESS, command= lambda: self.salvaSocieta('prodotto'))
        saveProdbutton.pack(pady=20)

        #************ LISTA AZIENDE WINDOW ************
        self.listWin = ttk.Frame(self.settingsWin)
        self.listWin.pack(fill="both")

        self.clientiLbl = ttk.Label(self.listWin, text="CLIENTI:", font=("Helvetica", 12))

        self.clSclContainer = ttk.Frame(self.listWin)
        self.clCanvas = ttk.Canvas(self.clSclContainer)
        self.clScrollBar = ttk.Scrollbar(self.clSclContainer, orient = 'vertical', command=self.clCanvas.yview)
        self.clscrFrame = ttk.Frame(self.clCanvas)

                
        self.clscrFrame.bind(
            '<Configure>',
            lambda e: self.clCanvas.configure(
                scrollregion=self.clCanvas.bbox('all')
            )
        )

        def _on_mousew(event):
            if event.num == 4:
                self.clCanvas.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.clCanvas.yview_scroll(1,'units')

        def _bind_mousew(event):
            self.clCanvas.bind_all('<Button-4>', _on_mousew)
            self.artCanvas.bind_all('<Button-5>', _on_mousew)

        def _unbind_mousew(event):
            self.clCanvas.unbind_all('<Button-4>')
            self.clCanvas.unbind_all('<Button-5>')

        self.clCanvas.create_window((0, 0), window=self.clscrFrame, anchor='nw')
        self.clCanvas.configure(yscrollcommand=self.clScrollBar.set)

        self.clCanvas.bind('<Enter>', _bind_mousew)
        self.clCanvas.bind('<Leave>', _unbind_mousew)

        self.clientiLbl.pack(pady=10)
        self.clSclContainer.pack(fill='both', expand = True)
        self.clCanvas.pack(side= 'left', fill = 'both', expand=True, padx = 5)
        self.clScrollBar.pack(side = 'right', fill = 'y')




        #*********** LISTA PRODOTTI WINDOW *************+
        
        self.prodWin = ttk.Frame(self.settingsWin)
        self.prodWin.pack(fill="both")

        self.articoliLbl = ttk.Label(self.prodWin, text="Articoli:", font=("Helvetica", 12))

        self.artSclContainer = ttk.Frame(self.prodWin)
        self.artCanvas = ttk.Canvas(self.artSclContainer)
        self.artScrollBar = ttk.Scrollbar(self.artSclContainer, orient = 'vertical', command=self.artCanvas.yview)
        self.scrFrame = ttk.Frame(self.artCanvas)

                
        self.scrFrame.bind(
            '<Configure>',
            lambda e: self.artCanvas.configure(
                scrollregion=self.artCanvas.bbox('all')
            )
        )

        def _on_mousew(event):
            if event.num == 4:
                self.artCanvas.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.artCanvas.yview_scroll(1,'units')

        def _bind_mousew(event):
            self.artCanvas.bind_all('<Button-4>', _on_mousew)
            self.artCanvas.bind_all('<Button-5>', _on_mousew)

        def _unbind_mousew(event):
            self.artCanvas.unbind_all('<Button-4>')
            self.artCanvas.unbind_all('<Button-5>')

        self.artCanvas.create_window((0, 0), window=self.scrFrame, anchor='nw')
        self.artCanvas.configure(yscrollcommand=self.artScrollBar.set)

        self.artCanvas.bind('<Enter>', _bind_mousew)
        self.artCanvas.bind('<Leave>', _unbind_mousew)


        self.articoliLbl.pack(side = 'top', pady=10)
        self.artSclContainer.pack(fill='both', expand = True)
        self.artCanvas.pack(side= 'left', fill = 'both', expand=True, padx = 5)
        self.artScrollBar.pack(side = 'right', fill = 'y')
       
    def popolaArt(self):
        self.prodotti = self.loadProdotti()
        for widget in self.scrFrame.winfo_children():
            if isinstance(widget, Frame):  # elimina solo i Frame (che contengono Label e Button)
                widget.destroy()

        for nome in self.prodotti:
            frame = Frame(self.scrFrame, borderwidth=2, relief="solid")
            frame.pack(pady=2, padx=20, fill="both")

            lbl = Label(frame, text=nome, font=self.arial)
            lbl.pack(side=ttk.LEFT, padx=30, pady=5)

            deleteBtn = Button(frame, text="Delete", bootstyle="danger",
                            command=lambda articolo=nome, f=frame: self.deleteProd(articolo, f))
            deleteBtn.pack(side=ttk.RIGHT, pady=5, padx = 50)



    def popolaLista(self):
        self.aziende = self.loadAziende()
        self.aziende = self.loadAziende()
        for widget in self.clscrFrame.winfo_children():
            if isinstance(widget, Frame):  # elimina solo i Frame (che contengono Label e Button)
                widget.destroy()

        for nome in self.aziende:
            frame = Frame(self.clscrFrame, borderwidth=2, relief="solid")
            frame.pack(pady=2, padx=20, fill="both")

            lbl = Label(frame, text=nome, font=self.arial)
            lbl.pack(side=ttk.LEFT, padx=50, pady=5)

            deleteBtn = Button(frame, text="Elimina", bootstyle="danger",
                            command=lambda cliente=nome, f=frame: self.deleteAzienda(cliente, f))
            deleteBtn.pack(side=ttk.RIGHT, pady=5,padx= 50)

            

    def deleteAzienda(self, cliente, frame):
        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()

            cur.execute(f"SELECT id FROM clienti WHERE cliente = '{cliente}'")

            result = cur.fetchone()
            if result:
                idCliente = result[0]

            cur.execute("DELETE FROM clienti WHERE id = ?", (idCliente,))
            conn.commit()

            cur.close()
            conn.close()

            frame.destroy()

            # Aggiorna self.aziende dopo l'eliminazione
            self.aziende = self.loadAziende()

            print(f"{cliente} eliminato.")

        except Exception as e:
            print(f"Errore durante l'eliminazione: {e}")


    def deleteProd(self, prod, frame):
        try:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()

            cur.execute(f"SELECT id FROM prodotti WHERE prodotto = '{prod}'")

            result = cur.fetchone()
            if result:
                idProd = result[0]

            cur.execute("DELETE FROM prodotti WHERE id = ?", (idProd,))
            conn.commit()

            cur.close()
            conn.close()

            frame.destroy()

            # Aggiorna self.aziende dopo l'eliminazione
            self.prodotti = self.loadProdotti()
            self.aggiornaAziende()

            print(f"{prod} eliminato.")

        except Exception as e:
            print(f"Errore durante l'eliminazione: {e}")
    

    def changeFrame(self, frame, btnOn, btnOff, btOff):
        self.settWin.pack_forget()
        self.listWin.pack_forget()
        self.prodWin.pack_forget()
        frame.pack()
        btnOff.config(bootstyle="primary")
        btOff.config(bootstyle="primary")
        btnOn.config(bootstyle=SUCCESS)
        if frame == self.listWin:
            self.popolaLista()
        elif frame == self.prodWin:
            self.popolaArt()



    def salvaSocieta(self, id):
        if id == 'cliente':
            entry = self.entry_nome.get()
        elif id == 'prodotto':
            entry = self.entryProd.get()
        if entry:
            self.saveAziende(entry, id)
            self.entry_nome.delete(0, 'end')
            self.entryProd.delete(0, 'end')
            self.aggiornaAziende()
        else:
            print("Inserisci un nome valido.")