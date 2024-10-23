import json
from tkinter import *

class MatrizApp:
    def __init__(self, master):
        self.master = master
        master.title("Matriz 10x10 con Muros")
        
        # Eliminar el padding del frame principal
        master.grid_propagate(False)
        master.configure(width=400, height=400)

        self.buttons = []
        self.current_color = "green"  # Color inicial
        self.color_names = {
            "green": "Veneno",
            "brown": "Muro",
            "yellow": "Salida",
            "SystemButtonFace": "Vacío"  # Añadido para botones sin color
        }
        self.investigating = False  # Nueva variable para controlar el modo investigación

        # Crear el menú
        self.menu = Menu(master)
        master.config(menu=self.menu)

        # Crear un submenú para los colores
        color_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Colores", menu=color_menu)
        color_menu.add_command(label="Veneno", command=lambda: self.set_color("green"))
        color_menu.add_command(label="Muro", command=lambda: self.set_color("brown"))
        color_menu.add_command(label="Salida", command=lambda: self.set_color("yellow"))
        color_menu.add_command(label="Investigar", command=self.investigar)
        
        # Añadir opciones para guardar y cargar mapa
        self.menu.add_command(label="Guardar Mapa", command=self.guardar_mapa)
        self.menu.add_command(label="Cargar Mapa", command=self.cargar_mapa)

        for i in range(10):
            row = []
            for j in range(10):
                button = Button(master, text="", width=4, height=2,
                                command=lambda x=i, y=j: self.toggle_wall(x, y),
                                borderwidth=1, relief="raised")
                button.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
                row.append(button)
            self.buttons.append(row)
        
        # Hacer que las filas y columnas se expandan uniformemente
        for i in range(10):
            master.grid_rowconfigure(i, weight=1)
            master.grid_columnconfigure(i, weight=1)

    def set_color(self, color):
        self.investigating = False  # Desactivar modo investigación
        self.current_color = color

    def toggle_wall(self, i, j):
        button = self.buttons[i][j]
        
        if self.investigating:
            # Si estamos en modo investigación
            current_color = button.cget("background")
            if current_color == "":
                current_color = "SystemButtonFace"
            print(f"Casilla [{i},{j}] - Color: {self.color_names.get(current_color, 'Desconocido')}")
            self.investigating = False  # Desactivar modo investigación después de investigar
        else:
            # Comportamiento normal de toggle
            current_color = button.cget("background")
            if current_color == "SystemButtonFace" or current_color == "":
                button.configure(bg=self.current_color)
            else:
                button.configure(bg="SystemButtonFace")

    def investigar(self):
        self.investigating = True  # Activar modo investigación
        print("Modo investigación activado. Haz clic en una casilla para investigarla.")

    def guardar_mapa(self):
        mapa = []
        for row in self.buttons:
            fila = []
            for button in row:
                color = button.cget("background")
                fila.append(color)
            mapa.append(fila)
        
        with open('mapas.json', 'w') as f:
            json.dump(mapa, f)
        print("Mapa guardado en 'mapas.json'.")

    def cargar_mapa(self):
        try:
            with open('mapas.json', 'r') as f:
                mapa = json.load(f)
            for i in range(10):
                for j in range(10):
                    color = mapa[i][j]
                    self.buttons[i][j].configure(bg=color)
            print("Mapa cargado desde 'mapas.json'.")
        except FileNotFoundError:
            print("El archivo 'mapas.json' no fue encontrado.")
        except json.JSONDecodeError:
            print("Error al leer el archivo 'mapas.json'.")

root = Tk()
app = MatrizApp(root)
root.mainloop()