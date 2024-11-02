from tkinter import Canvas
import os
import json


class MapaCanvas:
    def __init__(self, master, matriz):
        self.master = master
        self.matriz = matriz
        self.tamano_matriz = len(matriz)
        self.canvas = Canvas(self.master, width=self.tamano_matriz * 40, height=self.tamano_matriz * 40)
        self.canvas.pack()
        self.dibujar_mapa()

    def dibujar_mapa(self):
        """Dibuja la matriz en el Canvas."""
        self.canvas.delete("all")  # Limpiar el canvas antes de dibujar
        for i in range(self.tamano_matriz):
            for j in range(self.tamano_matriz):
                color = self.matriz[i][j]  # Asumimos que la matriz ya tiene colores como cadenas
                self.canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill=color)

def cargar_mapa(self, espacio):
    """Carga un mapa desde un archivo JSON en la carpeta 'Mapas'."""
    ruta_mapa = os.path.join("Mapas", f"mapa_{espacio}.json")
    if os.path.exists(ruta_mapa):
        with open(ruta_mapa, "r") as f:
            self.matriz = json.load(f)
        self.tamano_matriz = len(self.matriz)
        self.canvas.config(width=self.tamano_matriz * 40, height=self.tamano_matriz * 40)  # Ajusta el tamaño del Canvas
        # Instancia MapaCanvas con la nueva matriz
        mapa_canvas = MapaCanvas(self.master, self.matriz)
    else:
        print(f"El archivo {ruta_mapa} no existe.")