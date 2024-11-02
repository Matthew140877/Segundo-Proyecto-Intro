import json
import random
from tkinter import *


class MatrizApp:
    def __init__(self, master):
        self.master = master
        master.title("Matriz 10x10 con Hormiga")

        # Configuración del Canvas
        self.canvas = Canvas(master, width=400, height=400)
        self.canvas.pack()

        # Colores para la matriz
        self.colors = {
            "SystemButtonFace": "white",
            "green": "green",
            "brown": "brown",
            "yellow": "yellow"
        }

        # Inicialización de la matriz (10x10 por defecto en blanco)
        self.matriz = [["SystemButtonFace" for _ in range(10)] for _ in range(10)]
        self.draw_matrix()  # Dibuja la matriz inicial

        # Menú para guardar y cargar mapas
        self.menu = Menu(master)
        master.config(menu=self.menu)

        # Menú de colores
        color_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Colores", menu=color_menu)
        color_menu.add_command(label="Veneno", command=lambda: self.set_color("green"))
        color_menu.add_command(label="Muro", command=lambda: self.set_color("brown"))
        color_menu.add_command(label="Salida", command=lambda: self.set_color("yellow"))

        # Menús para guardar y cargar
        guardar_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Guardar Mapa", menu=guardar_menu)
        guardar_menu.add_command(label="Espacio 1", command=lambda: self.guardar_mapa(1))
        guardar_menu.add_command(label="Espacio 2", command=lambda: self.guardar_mapa(2))
        guardar_menu.add_command(label="Espacio 3", command=lambda: self.guardar_mapa(3))

        cargar_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Cargar Mapa", menu=cargar_menu)
        cargar_menu.add_command(label="Mapa 1", command=lambda: self.cargar_mapa(1))
        cargar_menu.add_command(label="Mapa 2", command=lambda: self.cargar_mapa(2))
        cargar_menu.add_command(label="Mapa 3", command=lambda: self.cargar_mapa(3))

        # Instanciación de la hormiga y movimiento
        self.hormiga = Hormiga(self.canvas)
        self.hormiga.mover()

        # Guardar coordenadas al cerrar la ventana
        master.protocol("WM_DELETE_WINDOW", self.guardar_coordenadas)

    def set_color(self, color):
        """Cambia el color actual para la matriz."""
        self.current_color = color
        self.canvas.bind("<Button-1>", self.color_cell)

    def color_cell(self, event):
        """Cambia el color de la celda seleccionada en la matriz y actualiza el canvas."""
        i, j = event.x // 40, event.y // 40
        self.matriz[j][i] = self.current_color
        self.draw_matrix()

    def draw_matrix(self):
        """Dibuja la matriz en el Canvas."""
        self.canvas.delete("matrix")
        for i in range(10):
            for j in range(10):
                color = self.colors.get(self.matriz[i][j], "white")
                x1, y1 = j * 40, i * 40
                x2, y2 = x1 + 40, y1 + 40
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="matrix")

    def guardar_mapa(self, numero):
        """Guarda la configuración actual de la matriz en el archivo JSON."""
        if numero < 1 or numero > 3:
            print("Número inválido. Debe ser del 1 al 3.")
            return
        try:
            with open('mapas.json', 'r') as f:
                mapas = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            mapas = {1: [], 2: [], 3: []}

        mapas[numero] = self.matriz
        with open('mapas.json', 'w') as f:
            json.dump(mapas, f)
        print(f"Mapa {numero} guardado en 'mapas.json'.")

    def cargar_mapa(self, numero):
        """Carga una configuración de la matriz desde el archivo JSON."""
        if numero < 1 or numero > 3:
            print("Número inválido. Debe ser del 1 al 3.")
            return
        try:
            with open('mapas.json', 'r') as f:
                mapas = json.load(f)
            mapa = mapas.get(str(numero))
            if mapa:
                self.matriz = mapa
                self.draw_matrix()
                print(f"Mapa {numero} cargado desde 'mapas.json'.")
            else:
                print(f"No se encontró el mapa {numero}.")
        except FileNotFoundError:
            print("El archivo 'mapas.json' no fue encontrado.")
        except json.JSONDecodeError:
            print("Error al leer el archivo 'mapas.json'.")

    def guardar_coordenadas(self):
        """Guarda las coordenadas de la hormiga al cerrar la aplicación."""
        self.hormiga.guardar_coordenadas()
        self.master.destroy()


class Hormiga:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = random.randint(0, 9)
        self.y = random.randint(0, 9)
        self.direccion_x = random.choice([-1, 1])
        self.direccion_y = random.choice([-1, 1])
        self.rectangulo = None
        self.coor_pasadas = []

    def crear_rectangulo(self):
        """Crea o actualiza la posición del rectángulo que representa a la hormiga."""
        if self.rectangulo:
            self.canvas.delete(self.rectangulo)
        x1, y1 = self.x * 40, self.y * 40
        x2, y2 = x1 + 40, y1 + 40
        self.rectangulo = self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="")

    def mover(self):
        """Mueve la hormiga y actualiza su posición en el Canvas."""
        self.coor_pasadas.append((self.x, self.y))

        # Actualizar posición de la hormiga
        self.x += self.direccion_x
        self.y += self.direccion_y

        # Colisiones con los bordes
        if self.x < 0 or self.x >= 10:
            self.direccion_x *= -1
            self.x += self.direccion_x
        if self.y < 0 or self.y >= 10:
            self.direccion_y *= -1
            self.y += self.direccion_y

        # Dibujar la hormiga en la nueva posición
        self.crear_rectangulo()

        # Programar el siguiente movimiento
        self.canvas.after(500, self.mover)

    def guardar_coordenadas(self):
        """Guarda las coordenadas por las que ha pasado la hormiga en un archivo JSON."""
        coordenadas_dict = {"coordenadas": self.coor_pasadas}
        with open('coordenadas_hormiga.json', 'w') as archivo:
            json.dump(coordenadas_dict, archivo)
        print("Coordenadas guardadas en 'coordenadas_hormiga.json'.")

# Configuración e inicio de la aplicación
root = Tk()
app = MatrizApp(root)
root.mainloop()