import json
import random
import os  # Importar os para manejar rutas
from tkinter import *

class MatrizApp:
    def __init__(self, master):
        self.master = master
        master.title("Matriz con Hormiga")

        # Inicialización de la matriz (10x10 por defecto en blanco)
        self.tamano_matriz = 10
        self.matriz = [["white" for _ in range(self.tamano_matriz)] for _ in range(self.tamano_matriz)]

        # Crear un Canvas para la matriz
        self.canvas = Canvas(master, width=400, height=400)  # Tamaño estándar
        self.canvas.pack()

        # Dibuja la matriz inicial
        self.draw_matrix()

        # Reconfigurar el evento de clic para cambiar colores
        self.canvas.bind("<Button-1>", self.color_cell)

        # Inicialización de la hormiga
        self.hormiga = None

        # Crear el menú
        self.menu = Menu(master)
        master.config(menu=self.menu)

        # Menú de colores
        color_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Colores", menu=color_menu)
        color_menu.add_command(label="Veneno", command=lambda: self.set_color("green"))
        color_menu.add_command(label="Muro", command=lambda: self.set_color("brown"))
        color_menu.add_command(label="Salida", command=lambda: self.set_color("yellow"))

        # Menú para cambiar tamaño de la matriz
        tamaño_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Tamaño de Matriz", menu=tamaño_menu)
        tamaño_menu.add_command(label="5x5", command=lambda: self.cambiar_tamano(5))
        tamaño_menu.add_command(label="7x7", command=lambda: self.cambiar_tamano(7))
        tamaño_menu.add_command(label="10x10", command=lambda: self.cambiar_tamano(10))

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

        # Opción para volver al menú principal
        self.menu.add_command(label="Volver", command=self.volver)

        # Guardar coordenadas al cerrar la ventana
        master.protocol("WM_DELETE_WINDOW", self.guardar_coordenadas)

    def cambiar_tamano(self, nuevo_tamano):
        """Cambia el tamaño de la matriz y redibuja."""
        self.tamano_matriz = nuevo_tamano
        self.matriz = [["SystemButtonFace" for _ in range(self.tamano_matriz)] for _ in range(self.tamano_matriz)]
        self.draw_matrix()

    def volver(self):
        """Destruye la ventana de la matriz."""
        self.master.destroy()

    def iniciar_simulacion(self):
    # Asegúrate de que la hormiga esté inicializada y en una posición válida
        if self.hormiga is None:
            self.hormiga = Hormiga(self.canvas, self.tamano_matriz)  # Inicializa la hormiga
            self.hormiga.x, self.hormiga.y = 0, 0  # Cambia esto a la posición inicial dese

    def set_color(self, color):
        """Cambia el color actual para la matriz."""
        self.current_color = color

    def color_cell(self, event):
        """Cambia el color de la celda seleccionada en la matriz y actualiza el canvas."""
        i, j = event.x // 40, event .y // 40
        if i < self.tamano_matriz and j < self.tamano_matriz:  # Verifica que las coordenadas estén dentro de la matriz
            self.matriz[j][i] = self.current_color
            self.draw_matrix()

    def draw_matrix(self):
        """Dibuja la matriz en el Canvas."""
        self.canvas.delete("matrix")
        for i in range(self.tamano_matriz):
            for j in range(self.tamano_matriz):
                color = self.matriz[i][j]
                x1, y1 = j * 40, i * 40
                x2, y2 = x1 + 40, y1 + 40
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tag="matrix")

    def guardar_mapa(self, espacio):
        """Guarda el mapa actual en un archivo JSON en la carpeta 'Mapas'."""
        ruta_mapa = os.path.join("Mapas", f"mapa_{espacio}.json")
        with open(ruta_mapa, "w") as f:
            json.dump(self.matriz, f)

    def cargar_mapa(self, espacio):
        """Carga un mapa desde un archivo JSON en la carpeta 'Mapas'."""
        ruta_mapa = os.path.join("Mapas", f"mapa_{espacio}.json")
        if os.path.exists(ruta_mapa):
            with open(ruta_mapa, "r") as f:
                self.matriz = json.load(f)
            self.tamano_matriz = len(self.matriz)
            self.canvas.config(width=self.tamano_matriz * 40, height=self.tamano_matriz * 40)  # Ajusta el tamaño del Canvas
            self.draw_matrix()
        else:
            print(f"El archivo {ruta_mapa} no existe.")

    def guardar_coordenadas(self):
        """Guarda las coordenadas actuales al cerrar la ventana."""
        with open("coordenadas.txt", "w") as f:
            if self.hormiga is not None:  # Verifica si la hormiga ha sido inicializada
                f.write(f"{self.hormiga.x} {self.hormiga.y}")
            else:
                f.write("Hormiga no ha sido inicializada.") # Mensaje alternativo