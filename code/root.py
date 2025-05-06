from impostazioni import SettingsUI
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Combobox
from ttkbootstrap.widgets import Checkbutton
from ttkbootstrap.widgets import Label
import json

class UI():
    def __init__(self):
        self.root = None
        self.settingsUi = SettingsUI(self.root)
        self.aziendeMap = self.loadAziende()
        self.aziende = list(self.aziendeMap.values())
        self.articoli = ["Lenzuola", "CopriMaterasso", "Federa"]
        self.listButtons = []
        self.cbVars = []
        self.selAll = None
        self.aziendaCB = None

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

    def loadAziende(self):
        try:
            with open('aziende.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}


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

        saveBtn = ttk.Button(toolbar, text="Salva", bootstyle=SUCCESS)
        saveBtn.pack(side=ttk.LEFT, padx=20, pady=5)

        settingsBtn = ttk.Button(toolbar, text="Impostazioni", bootstyle=INFO,command= self.settingsUi.BuildUi)
        settingsBtn.pack(side=ttk.LEFT, padx=20, pady=5)

        # selSelectedBuche = Checkbutton(toolbar, variable= self.selAll, bootstyle = "secondary", command = lambda: self.selAllFun())
        # selSelectedBuche.pack(side=ttk.LEFT, padx = 20, pady = 5)

        self.aziendaCB = Combobox(toolbar, values = self.aziende, bootstyle = "info", state = "readonly")
        self.aziendaCB.set(self.aziende[0])
        self.aziendaCB.pack(side = LEFT, padx = 20, pady= 5)

        style = ttk.Style()
        style.configure("Custom.TFrame", background="#2d2d2d")
        style.configure("title.TLabel", background = "#2d2d2d" ,foreground="orange")
        style.configure("lbl.TLabel", background = "#2d2d2d" ,foreground="white")


        def creaBuche():
            for i in range(10):
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

                count = 0   #***************************QUESTO COUNT PER IL MOMENTO è SOLO UN PLACEHOLDER <------------

                countLbl = Label(frame, text = f"Count: {count}", style = "lbl.TLabel")
                countLbl.place(x = 80, y = 120)

        creaBuche()

    def selAllFun(self):
        if self.selAll.get():
            for i, var in enumerate(self.cbVars):
                if var.get():  # Se il Checkbutton è selezionato
                    self.comboList[i].set(self.aziendaCB.get()) 

    def disableCB(self, var, combobox):
        if var.get():   # Se la checkbox è selezionata
            combobox.config(state="disabled")
        else:           # Se la checkbox è deselezionata
            combobox.config(state="readonly")
            

if __name__ == '__main__':
    app = UI()
    app.BuildUi()
    app.root.mainloop()    