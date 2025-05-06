import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Combobox
from ttkbootstrap.widgets import Checkbutton
from ttkbootstrap.widgets import Frame
from ttkbootstrap.widgets import Label
from ttkbootstrap.widgets import Button
import tkinter.font as tkFont
import json


class SettingsUI():
    def __init__(self, root):
        self.root = root
        self.settingsWin = None
        self.aziende = self.loadAziende()
        self.mapWidg = {}

    def saveAziende(self, id, azienda):
        try:
            try:
                with open('aziende.json', 'r') as file:
                    aziende = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                aziende = {}
            
            aziende[id] = azienda
            
            with open('aziende.json', 'w') as file:
                json.dump(aziende, file, indent = 4)
                
        except Exception as e:
            print(f'Errore during the JSON update: {e}')

    def loadAziende(self):
        try:
            with open('aziende.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}


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

        label = ttk.Label(self.settWin, text="Nome Società:", font=("Helvetica", 12))
        label.pack(pady=10)

        self.entry_nome = ttk.Entry(self.settWin, width=30)
        self.entry_nome.pack(pady=5)

        save_button = ttk.Button(self.settWin, text="Aggiungi Società", bootstyle=SUCCESS, command= lambda: self.salvaSocieta())
        save_button.pack(pady=20)

        #************ LISTA AZIENDE WINDOW ************

        self.listWin = ttk.Frame(self.settingsWin)
        self.listWin.pack(fill="both")

        label = ttk.Label(self.listWin, text="AZIENDE:", font=("Helvetica", 12))
        label.pack(pady=10)
        


    def popolaLista(self):
        self.aziende = self.loadAziende()
        for widget in self.listWin.winfo_children():
            if isinstance(widget, Frame):  # elimina solo i Frame (che contengono Label e Button)
                widget.destroy()

        for azienda_id, nome in self.aziende.items():
            frame = Frame(self.listWin, borderwidth=2, relief="solid")
            frame.pack(pady=0, padx=10, fill="both")

            lbl = Label(frame, text=nome, font=self.arial)
            lbl.pack(side=ttk.LEFT, padx=50, pady=5)

            deleteBtn = Button(frame, text="Delete", bootstyle="danger",
                            command=lambda id=azienda_id, f=frame: self.deleteAzienda(id, f))
            deleteBtn.pack(side=ttk.RIGHT, pady=5)

            

    def deleteAzienda(self, id, frame):
        try:
            with open('aziende.json', 'r') as file:
                aziende = json.load(file)

            if str(id) in aziende:
                del aziende[str(id)]

                with open('aziende.json', 'w') as file:
                    json.dump(aziende, file, indent=4)

                frame.destroy()

                self.aziende = aziende

                print(f"Azienda con ID {id} eliminata.")
            else:
                print(f"Azienda con ID {id} non trovata.")

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
        mapAziende = self.loadAziende()
        id = int(len(mapAziende) + 1)
        if nome_azienda:
            self.saveAziende(id, nome_azienda)
            self.entry_nome.delete(0, 'end') 
            print(f"Azienda '{nome_azienda}' salvata con successo.")
        else:
            print("Inserisci un nome valido.")