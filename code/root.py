from impostazioni import SettingsUI
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Combobox
from ttkbootstrap.widgets import Label
import json

class UI():
    def __init__(self):
        self.root = None
        self.settingsUi = SettingsUI(self.root)
        self.aziende = ["Azienda Uno", "Azienda Due", "Azienda Tre", "Azienda Quattro", "Azienda Cinque"]
        self.articoli = ["Lenzuola", "CopriMaterasso", "Federa"]

    def saveAziende(id, azienda):
        # DA MODIFICARE NO MAPPA MA LISTA
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
        self.root = ttk.Window(themename="superhero")
        self.root.title("Smistatore")
        self.root.geometry("1100x500")
        self.root.resizable(False, False)
        self.comboList = []

        
        toolbar = ttk.Frame(self.root, bootstyle="secondary")
        toolbar.pack(side=ttk.TOP, fill=ttk.X)

        newBtn = ttk.Button(toolbar, text="Nuovo", bootstyle=PRIMARY)
        newBtn.pack(side=ttk.LEFT, padx=20, pady=5)

        saveBtn = ttk.Button(toolbar, text="Salva", bootstyle=SUCCESS)
        saveBtn.pack(side=ttk.LEFT, padx=20, pady=5)

        settingsBtn = ttk.Button(toolbar, text="Impostazioni", bootstyle=INFO,command= self.settingsUi.BuildUi)
        settingsBtn.pack(side=ttk.LEFT, padx=20, pady=5)


        def creaBuche():
            for i in range(10):
                colonna = i % 5
                riga = i // 5
                x = (200 * colonna) + (10*colonna)
                y = 50 + (riga * 200) + (20 * riga)
                frame = ttk.Frame(self.root, bootstyle="dark", borderwidth=2, relief="solid")
                frame.place(x=x, y=y, width=200, height=200)
                
                nList = ["Uno", "Due", "Tre", "Quattro", "Cinque", "Sei", "Sette", "Otto", "Nove", "Dieci"]
                n = nList[i]

                bucaLbl = Label(frame, text = f"Buca {n}", bootstyle = "dark", foreground="orange") #<----------- METTERE FONT ARIAL E BOLD
                bucaLbl.place(x = 5, y = 5)

                aziendaLbl = Label(frame, text = "Azienda: ", bootstyle = "dark", foreground="white")
                aziendaLbl.place(x = 5, y = 45)
                aziendaCB = Combobox(frame, values = self.aziende, bootstyle = "info", state = "readonly")
                aziendaCB.set(self.aziende[0])
                aziendaCB.place(x = 60, y = 40, height= 30, width=130)

                articoliLbl = Label(frame, text = "Articolo: ", bootstyle = "dark", foreground= "white")
                articoliLbl.place(x = 5, y = 75)

                comboB = Combobox(frame, values= self.articoli, bootstyle="info", state="readonly")
                comboB.set(self.articoli[0])
                comboB.place(x = 60, y = 70, height=30, width=130)

                self.comboList.append(comboB) # <------------ SERVIRA PER CREARE FUNZIONE SELEZIONA UN'UNICA AZIENDA PER TUTTE BUCHE

                count = 0   #***************************QUESTO COUNT PER IL MOMENTO è SOLO UN PLACEHOLDER <------------

                countLbl = Label(frame, text = f"Count: {count}", bootstyle = "dark", foreground = "white")
                countLbl.place(x = 80, y = 120)

        creaBuche()
if __name__ == '__main__':
    app = UI()
    app.BuildUi()
    app.root.mainloop()    