import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json

class SettingsUI():
    def __init__(self, root):
        self.root = root
        self.settingsWin = None
        self.aziende = []

    def saveAziende(id, azienda):
        try:
            try:
                with open('aziende.json', 'r') as file:
                    dati = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                dati = {}
            
            dati[id] = azienda
            
            with open('settings.json', 'w') as file:
                json.dump(dati, file, indent = 4)
                
        except Exception as e:
            print(f'Errore during the JSON update: {e}')

    def loadAziende():
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

        save_button = ttk.Button(self.settingsWin, text="Aggiungi Società", bootstyle=SUCCESS, command=self.salvaSocieta)
        save_button.pack(pady=20)

    def salvaSocieta(self):
        nome_azienda = self.entry_nome.get()
        if nome_azienda:
            self.saveAzienda(nome_azienda)
            self.entry_nome.delete(0, 'end')  # Svuota il campo dopo il salvataggio
            print(f"Azienda '{nome_azienda}' salvata con successo.")
        else:
            print("Inserisci un nome valido.")


        main_content = ttk.Label(self.root, text="Contenuto principale", font=("Helvetica", 16))
        main_content.pack(pady=50)