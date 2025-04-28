import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json

class SettingsUI():
    def __init__(self, root):
        self.root = root
        self.settingsWin = None
        self.aziende = []

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


        label = ttk.Label(self.settingsWin, text="Nome Società:", font=("Helvetica", 12))
        label.pack(pady=10)

        self.entry_nome = ttk.Entry(self.settingsWin, width=30)
        self.entry_nome.pack(pady=5)

        save_button = ttk.Button(self.settingsWin, text="Aggiungi Società", bootstyle=SUCCESS, command= lambda: self.salvaSocieta())
        save_button.pack(pady=20)

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