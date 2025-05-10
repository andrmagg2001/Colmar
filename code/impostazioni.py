import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Combobox
from ttkbootstrap.widgets import Checkbutton
from ttkbootstrap.widgets import Frame
from ttkbootstrap.widgets import Label
from ttkbootstrap.widgets import Button
import tkinter.font as tkFont
import sqlite3

class SettingsUI():
    def __init__(self, root, aggiornaAziende):
        self.root = root
        self.aggiornaAziende = aggiornaAziende
        self.settingsWin = None
        self.aziende = self.loadAziende()
        self.mapWidg = {}

    def saveAziende(self, azienda):
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM clienti WHERE cliente = ?", (azienda,))
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO clienti (cliente) VALUES (?)", (azienda,))
        else:
            print("Cliente già esistente.")

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


    def BuildUi(self):
        self.settingsWin = ttk.Toplevel(self.root)
        self.settingsWin.title("App con Toolbar")
        self.settingsWin.geometry("500x400")

        self.arial = tkFont.Font(family="Arial", size=12, weight="bold")

        toolbar = ttk.Frame(self.settingsWin, bootstyle="secondary")
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        settSec = ttk.Button(toolbar, text="Impostazioni", bootstyle=SUCCESS, command=lambda: self.changeFrame(self.settWin, settSec, listAzieSec))
        settSec.pack(side=ttk.LEFT, padx=0, pady=0)

        listAzieSec = ttk.Button(toolbar, text="Lista Aziende", bootstyle="primary", command = lambda: self.changeFrame(self.listWin, listAzieSec, settSec))
        listAzieSec.pack(side=ttk.LEFT, padx=0, pady=0)

        # selSelectedBuche = Checkbutton(toolbar, variable= self.selAll, bootstyle = "secondary", command = lambda: self.selAllFun())
        # selSelectedBuche.pack(side=ttk.LEFT, padx = 20, pady = 5)



        #************* SETTINGS WINDOW *************

        self.settWin = ttk.Frame(self.settingsWin)
        self.settWin.pack(fill="both")

        label = ttk.Label(self.settWin, text="Nome Cliente:", font=("Helvetica", 12))
        label.pack(pady=10)

        self.entry_nome = ttk.Entry(self.settWin, width=30)
        self.entry_nome.pack(pady=5)

        save_button = ttk.Button(self.settWin, text="Aggiungi Cliente", bootstyle=SUCCESS, command= lambda: self.salvaSocieta())
        save_button.pack(pady=20)

        #************ LISTA AZIENDE WINDOW ************

        self.listWin = ttk.Frame(self.settingsWin)
        self.listWin.pack(fill="both")

        label = ttk.Label(self.listWin, text="CLIENTI:", font=("Helvetica", 12))
        label.pack(pady=10)
        


    def popolaLista(self):
        self.aziende = self.loadAziende()
        for widget in self.listWin.winfo_children():
            if isinstance(widget, Frame):  # elimina solo i Frame (che contengono Label e Button)
                widget.destroy()

        for nome in self.aziende:
            frame = Frame(self.listWin, borderwidth=2, relief="solid")
            frame.pack(pady=0, padx=10, fill="both")

            lbl = Label(frame, text=nome, font=self.arial)
            lbl.pack(side=ttk.LEFT, padx=50, pady=5)

            deleteBtn = Button(frame, text="Delete", bootstyle="danger",
                            command=lambda cliente=nome, f=frame: self.deleteAzienda(cliente, f))
            deleteBtn.pack(side=ttk.RIGHT, pady=5)

            

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

    def changeFrame(self, frame, btnOn, btnOff):
        self.settWin.pack_forget()
        self.listWin.pack_forget()
        frame.pack()
        btnOff.config(bootstyle="primary")
        btnOn.config(bootstyle=SUCCESS)
        if frame == self.listWin:
            self.popolaLista()


    def salvaSocieta(self):
        nome_azienda = self.entry_nome.get()
        if nome_azienda:
            self.saveAziende(nome_azienda)
            self.entry_nome.delete(0, 'end')
            self.aggiornaAziende()
        else:
            print("Inserisci un nome valido.")