import tkinter as tk

# Configurazione finestra e cerchi
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
CIRCLE_RADIUS = 25
CIRCLES_PER_ROW = 5
ROWS = 2
HORIZONTAL_SPACING = (WINDOW_WIDTH - 2 * CIRCLE_RADIUS) // CIRCLES_PER_ROW
VERTICAL_SPACING = (WINDOW_HEIGHT - 2 * CIRCLE_RADIUS) // ROWS

# Crea la finestra
root = tk.Tk()
root.title("20 cerchi su due righe")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(False, False)

# Canvas su cui disegnare
canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="white")
canvas.pack()

# Disegna i cerchi
def draw_circles():
    for row in range(ROWS):
        for col in range(CIRCLES_PER_ROW):
            x_center = CIRCLE_RADIUS + col * HORIZONTAL_SPACING
            y_center = CIRCLE_RADIUS + row * VERTICAL_SPACING

            x0 = x_center - CIRCLE_RADIUS
            y0 = y_center - CIRCLE_RADIUS
            x1 = x_center + CIRCLE_RADIUS
            y1 = y_center + CIRCLE_RADIUS

            canvas.create_oval(x0, y0, x1, y1, fill="lightblue", outline="black")

draw_circles()

# Avvia l'app
root.mainloop()