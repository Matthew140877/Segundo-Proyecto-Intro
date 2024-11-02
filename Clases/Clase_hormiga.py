import random

class Hormiga:
    def __init__(self, canvas, tamano_matriz=10):
        self.canvas = canvas
        self.tamano_matriz = tamano_matriz
        self.x, self.y = 5, 5  # Inicializa la hormiga en el centro de la matriz
        self.direccion = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Dirección aleatoria
        self.hormiga_oval = None  # Variable para guardar la referencia del óvalo de la hormiga

    def mover(self):
        """Mueve la hormiga en la dirección actual."""
        # Borra la posición anterior de la hormiga
        if self.hormiga_oval:
            self.canvas.delete(self.hormiga_oval)

        # Verifica si la hormiga ha alcanzado el borde de la matriz
        if self.x < 0 or self.x >= self.tamano_matriz or self.y < 0 or self.y >= self.tamano_matriz:
            self.direccion = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Cambia la dirección
            return  # No mueve la hormiga si está fuera de los límites

        # Actualiza la posición de la hormiga
        self.x += self.direccion[0]
        self.y += self.direccion[1]

        # Verifica el color de la celda actual
        color_actual = self.canvas.winfo_rgb(self.canvas.find_closest(self.x * 40 + 20, self.y * 40 + 20)[0])
        # Cambia la dirección si encuentra un "muro" (suponiendo que el color del muro es marrón)
        if color_actual == self.canvas.winfo_rgb("brown"):
            self.direccion = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Cambia la dirección

        # Dibuja la nueva posición de la hormiga
        self.hormiga_oval = self.canvas.create_oval(self.x * 40, self.y * 40, (self.x + 1) * 40, (self.y + 1) * 40, fill="red")

        # Llama a sí misma para continuar el movimiento
        self.canvas.after(100, self.mover)