from tkinter import Tk, Frame, Button, Toplevel, messagebox, Label
import os
import json
from Clases.Clase_matriz import MatrizApp
from Clases.Mapa_simulacion import MapaCanvas

class Master:
    def __init__(self, root):
        self.root = root
        self.root.geometry("300x200")
        self.root.resizable(0, 0)

        # Crear un marco para los botones
        self.frame = Frame(self.root)
        self.frame.pack(pady=20)

        # Botón para crear mapa
        self.boton_crear_mapa = Button(self.frame, text="Crear Mapa", command=self.crear_mapa)
        self.boton_crear_mapa.pack(side="left", padx=10)

        # Botón para iniciar simulación
        self.boton_iniciar_simulacion = Button(self.frame, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.boton_iniciar_simulacion.pack(side="right", padx=10)

    def crear_mapa(self):
        """Crear un nuevo mapa."""
        top = Toplevel(self.root)
        top.title("Mapa")
        self.matriz_app = MatrizApp(top)

    def iniciar_simulacion(self):
        """Desplegar ventana para seleccionar un mapa."""
        top = Toplevel(self.root)
        top.title("Seleccionar Mapa")

        for i in range(1, 4):
            Button(top, text=f"Mapa {i}", command=lambda mapa=i: self.mostrar_mapa(mapa)).pack(pady=10)

    def mostrar_mapa(self, mapa):
        """Muestra la matriz del mapa seleccionado en un nuevo Canvas."""
        mapa_top = Toplevel(self.root)
        mapa_top.title(f"Mapa {mapa}")

        ruta_mapa = os.path.join("Mapas", f"mapa_{mapa}.json")
        if not os.path.exists(ruta_mapa):
            messagebox.showerror("Error", f"El archivo {ruta_mapa} no existe.")
            return

        try:
            with open(ruta_mapa, 'r') as f:
                matriz = json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo de mapa no es válido.")
            return

        # Crear el MapaCanvas para mostrar la matriz
        mapa_canvas = MapaCanvas(mapa_top, matriz)

        # Crear un Frame para mostrar los datos
        datos_frame = Frame(mapa_top)
        datos_frame.pack()

        # Crear etiquetas para mostrar la vida, el contador y el contador de puntos
        self.vida_label = Label(datos_frame, text="Vida: 3")
        self.vida_label.pack(side="left")
        mapa_canvas.vida_label = self.vida_label

        self.contador_label = Label(datos_frame, text="Contador: 0")
        self.contador_label.pack(side="left")
        mapa_canvas.contador_label = self.contador_label

        self.puntos_label = Label(datos_frame, text="Puntos: 0")
        self.puntos_label.pack(side="left")
        mapa_canvas.puntos_label = self.puntos_label

        # Inicializar la hormiga con referencia a las etiquetas
        mapa_canvas.inicializar_datos(self.vida_label, self.contador_label, self.puntos_label)

# Inicializar la aplicación
root = Tk()
app = Master(root)
root.mainloop()