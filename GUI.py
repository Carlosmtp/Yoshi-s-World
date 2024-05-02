import tkinter as tk
from PIL import Image, ImageTk
from models.GameGUI import GameGUI

class GUI:
    def __init__(self, master):
        # Configurar ventana principal
        self.master = master
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 1280
        window_height = 720
        self.master.title("Yoshi's World")
        self.master.geometry(f"{window_width}x{window_height}")
        self.master.maxsize(window_width, window_height)
        self.master.minsize(window_width, window_height)
        self.master.resizable(False, False)
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.dificultad = 0
        
        # Cargar imagen de fondo
        self.background_image = Image.open("images/background.png")
        self.background_image = self.background_image.resize((window_width, window_height), Image.BICUBIC)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(master, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Crear selector de dificultad
        self.dificultad_var = tk.StringVar(master)
        self.dificultad_var.set("Seleccionar La Dificultad")
        self.dificultad_menu = tk.OptionMenu(master, self.dificultad_var, "Principiante (profundidad 2)", "Intermedio (profundidad 4)", "Avanzado (profundidad 6)", command=self.enable_play_button)
        self.dificultad_menu.place(x=600, y=200)
        
        # Botón para iniciar el juego
        self.play = tk.Button(master, text="Jugar", font=("Arial", 20), command=self.play_game)
        self.play.place(x=600, y=260)
        self.play.config(state=tk.DISABLED)
    
    def enable_play_button(self, *args):
        self.play.config(state=tk.NORMAL)
        
    def play_game(self):
        self.master.withdraw()
        tablero_inicial = [[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 4, 3, 2, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]
        game = GameGUI(tablero_inicial)
        game.draw_board()
        self.master.deiconify()
        
        
def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
