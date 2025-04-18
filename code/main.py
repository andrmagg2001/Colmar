from smistatore import *
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import math

class App:
    def __init__(self):
        # Parametri finestra e layout
        self.WIN_WIDTH   = 1200
        self.WIN_HEIGHT  = 800
        self.RADIUS      = 90      # raggio dei cerchi
        self.PADDING_X   = 30      # margine orizzontale
        self.SPACING_Y   = 100     # distanza verticale tra le due file
        self.button_frames = []    # per tenere traccia e distruggere i frame
       
        # Lista di istanze Smistatore
        self.smistatori = []
        
        self._build_ui()
        self._layout_smistatori()

    def _build_ui(self):
        self.root = tk.Tk()
        self.root.title("Gestione Smistatori")
        self.root.geometry(f"{self.WIN_WIDTH}x{self.WIN_HEIGHT}")
        self.root.resizable(False, False)

        # Frame in alto: input e bottoni globali
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill='x', pady=5)

        tk.Label(top_frame, text="Nome azienda:").pack(side='left', padx=(10,5))
        self.entry_name = tk.Entry(top_frame)
        self.entry_name.pack(side='left')
        tk.Button(top_frame, text="Aggiungi", command=self._aggiungi_azienda).pack(side='left', padx=5)

        tk.Button(top_frame, text="Esporta", command=self._esporta_excel).pack(side='right', padx=10)
        tk.Button(top_frame, text="Reset All", command=self._reset_all).pack(side='right')

        # Canvas per cerchi e controlli
        canvas_height = self.WIN_HEIGHT - 60  # spazio per top_frame
        self.canvas = tk.Canvas(self.root, width=self.WIN_WIDTH,
                                height=canvas_height, bg='white')
        self.canvas.pack()

    def _aggiungi_azienda(self):
        nome = self.entry_name.get().strip()
        if not nome:
            messagebox.showwarning("Attenzione", "Inserisci un nome azienda valido.")
            return
        # aggiungo nuova istanza
        self.smistatori.append(Smistatore(nome))
        self.entry_name.delete(0, 'end')
        self._layout_smistatori()

    def _reset_all(self):
        for s in self.smistatori:
            s.reset()
        self._layout_smistatori()

    def _esporta_excel(self):
        if not self.smistatori:
            messagebox.showinfo("Esporta", "Nessuna azienda da esportare.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Excel files', '*.xlsx'), ('Tutti i file', '*.*')]
        )
        if not file_path:
            return
        # preparo DataFrame
        dati = {
            'Azienda': [s.azienda for s in self.smistatori],
            'Contatore': [s.contatorePanni for s in self.smistatori]
        }
        df = pd.DataFrame(dati)
        try:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Esporta", f"Dati esportati in {file_path}")
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile salvare il file:\n{e}")

    def _layout_smistatori(self):
        # rimuovo vecchi frame bottoni
        for fr in self.button_frames:
            fr.destroy()
        self.button_frames.clear()
        self.canvas.delete('all')

        n = len(self.smistatori)
        if n == 0:
            return

        # due righe, colonne calcolate
        rows = 2
        cols = math.ceil(n / rows)

        # dimensioni canvas
        W = self.WIN_WIDTH
        H = int(self.canvas['height'])

        # spacing orizzontale per centrare
        total_circles_w = 2*self.RADIUS*cols
        avail_w = W - 2*self.PADDING_X - total_circles_w
        spacing_x = avail_w / (cols - 1) if cols > 1 else 0

        # dimensione griglia e offset
        grid_w = total_circles_w + spacing_x*(cols - 1)
        grid_h = 2*self.RADIUS*rows + self.SPACING_Y*(rows - 1)
        offset_x = (W - grid_w) / 2
        offset_y = (H - grid_h) / 2

        # disegno ciascun smistatore
        for idx, s in enumerate(self.smistatori):
            r = idx // cols
            c = idx % cols
            x = offset_x + self.RADIUS + c*(2*self.RADIUS + spacing_x)
            y = offset_y + self.RADIUS + r*(2*self.RADIUS + self.SPACING_Y)

            # nome sopra
            self.canvas.create_text(
                x, y - self.RADIUS - 15,
                text=s.azienda, font=("Arial", 12, "bold")
            )
            # cerchio
            self.canvas.create_oval(
                x-self.RADIUS, y-self.RADIUS,
                x+self.RADIUS, y+self.RADIUS,
                outline="black", fill="lightblue"
            )
            # contatore al centro
            tid = self.canvas.create_text(
                x, y,
                text=str(s.contatorePanni), font=("Arial", 14, "bold")
            )
            s._text_id = tid

            # frame bottoni
            btn_frame = tk.Frame(self.root)
            tk.Button(
                btn_frame, text="-", width=3,
                command=lambda sm=s: self._update_counter(sm, -1)
            ).pack(side='left', padx=2)
            tk.Button(
                btn_frame, text="+", width=3,
                command=lambda sm=s: self._update_counter(sm, +1)
            ).pack(side='left', padx=2)
            tk.Button(
                btn_frame, text="reset", width=5,
                command=lambda sm=s: self._do_reset(sm)
            ).pack(side='left', padx=2)

            # inserisco frame nel canvas
            self.canvas.create_window(
                x, y + self.RADIUS + 15,
                window=btn_frame
            )
            self.button_frames.append(btn_frame)

    def _update_counter(self, sm: Smistatore, delta: int):
        if delta > 0:
            sm.incremento(delta)
        else:
            sm.decremento(-delta)
        # aggiorno testo
        self.canvas.itemconfigure(sm._text_id, text=str(sm.contatorePanni))

    def _do_reset(self, sm: Smistatore):
        sm.reset()
        self.canvas.itemconfigure(sm._text_id, text=str(sm.contatorePanni))

if __name__ == '__main__':
    App()
    tk.mainloop()