import random
from tkinter import Canvas, Tk, messagebox

class Hormiga:
    def __init__(self, canvas, tamano_matriz=10):
        self.canvas = canvas
        self.tamano_matriz = tamano_matriz
        self.start_x, self.start_y = 5, 5  # Inicializa la posición de inicio
        self.x, self.y = self.start_x, self.start_y  # Inicializa la hormiga en la posición de inicio
        self.direccion = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Dirección aleatoria
        self.hormiga_oval = None  # Variable para guardar la referencia del óvalo de la hormiga
        self.vida = 3  # Vida inicial de la hormiga
        self.contador = 0  # Contador inicial
        self.puntos = 0
        self.nivel_alcohol = 0

    caminos_fallidos = set()  # Memoria compartida de caminos fallidos (almacena coordenadas)
    coordenadas_pendientes = {}  # Almacena coordenadas de posibles entradas a callejones

    def mover(self, vida_label, contador_label, puntos_label, alcohol_label):
        """Mueve la hormiga en la dirección actual y registra caminos fallidos."""
        if self.hormiga_oval:
            self.canvas.delete(self.hormiga_oval)

        rect_id = self.canvas.find_closest(self.x * 40 + 20, self.y * 40 + 20)[0]
        color_actual = self.canvas.itemcget(rect_id, 'fill')

        if color_actual == "yellow":
            print("La hormiga ha llegado a la meta. Movimiento detenido.")
            return

        if color_actual == "green":
            if (self.x, self.y) not in Hormiga.caminos_fallidos:
                Hormiga.caminos_fallidos.add((self.x, self.y))
                print(f"Agregado a caminos fallidos (veneno): {(self.x, self.y)}")
            self.vida = 0  # La hormiga muere instantáneamente
            self.reiniciar_hormiga(vida_label, contador_label, puntos_label, alcohol_label)
            return

        if color_actual == "red":
            self.nivel_alcohol += 5
            print(f"Vino encontrado en ({self.x}, {self.y}). Alcohol: {self.nivel_alcohol}")
            self.canvas.itemconfig(rect_id, fill="white")

        if self.vida <= 0:
            if (self.start_x, self.start_y) not in Hormiga.caminos_fallidos:
                Hormiga.caminos_fallidos.add((self.start_x, self.start_y))
                print(f"Agregado a caminos fallidos (inicio muerto): {(self.start_x, self.start_y)}")
            self.reiniciar_hormiga(vida_label, contador_label, puntos_label, alcohol_label)
            return

        elif color_actual == "gray":  # Azúcar

            self.puntos += 3
            print(f"Azúcar encontrada en ({self.x}, {self.y}). Puntos: {self.puntos}")
            # Cambia la celda a blanco para simular que el azúcar desaparece
            self.canvas.itemconfig(rect_id, fill="white")


        posibles_direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        direcciones_validas = []

        for dx, dy in posibles_direcciones:
            nueva_x = self.x + dx
            nueva_y = self.y + dy
            if 0 <= nueva_x < self.tamano_matriz and 0 <= nueva_y < self.tamano_matriz:
                rect_id_nueva = self.canvas.find_closest(nueva_x * 40 + 20, nueva_y * 40 + 20)[0]
                color_nueva = self.canvas.itemcget(rect_id_nueva, 'fill')
                if (nueva_x, nueva_y) not in Hormiga.caminos_fallidos and color_nueva != "brown" and (dx, dy) != (-self.direccion[0], -self.direccion[1]):
                    direcciones_validas.append((dx, dy))

        if len(direcciones_validas) > 1:
            # Marca la coordenada actual como posible entrada al callejón
            Hormiga.coordenadas_pendientes[(self.x, self.y)] = True

        if not direcciones_validas:
            for dx, dy in posibles_direcciones:
                nueva_x = self.x + dx
                nueva_y = self.y + dy
                if 0 <= nueva_x < self.tamano_matriz and 0 <= nueva_y < self.tamano_matriz:
                    rect_id_nueva = self.canvas.find_closest(nueva_x * 40 + 20, nueva_y * 40 + 20)[0]
                    color_nueva = self.canvas.itemcget(rect_id_nueva, 'fill')
                    if (nueva_x, nueva_y) not in Hormiga.caminos_fallidos and color_nueva != "brown":
                        direcciones_validas.append((dx, dy))

            if len(direcciones_validas) == 1 and (self.x, self.y) in Hormiga.coordenadas_pendientes:
                # Marca la entrada al camino como callejón solo si la hormiga ha regresado a ella
                entrada_callejon = (self.x - self.direccion[0], self.y - self.direccion[1])
                if entrada_callejon in Hormiga.coordenadas_pendientes:
                    Hormiga.caminos_fallidos.add(entrada_callejon)
                    print(f"Agregado a caminos fallidos (callejón sin salida): {entrada_callejon}")
                    del Hormiga.coordenadas_pendientes[entrada_callejon]

        if direcciones_validas:
            if len(direcciones_validas) == 1:
                # Si solo hay una dirección válida, marca la entrada a este camino
                Hormiga.coordenadas_pendientes[(self.x, self.y)] = True

            self.direccion = random.choice(direcciones_validas)
            nueva_x = self.x + self.direccion[0]
            nueva_y = self.y + self.direccion[1]
            self.x = nueva_x
            self.y = nueva_y
            self.contador += 1

        self.hormiga_oval = self.canvas.create_oval(self.x * 40, self.y * 40, (self.x + 1) * 40, (self.y + 1) * 40, fill="red")
        vida_label.config(text=f"Vida: {self.vida}")
        contador_label.config(text=f"Movimientos: {self.contador}")
        puntos_label.config(text=f"Puntos:{self.puntos}")
        alcohol_label.config(text=f"Alcohol:{self.nivel_alcohol}")
        self.canvas.after(200, self.mover, vida_label, contador_label,puntos_label,alcohol_label)

    def reiniciar_hormiga(self, vida_label, contador_label,puntos_label,alcohol_label):
        """Reinicia la posición y vida de la hormiga."""
        self.x = self.start_x
        self.y = self.start_y
        self.vida = 100  # O el valor que corresponda
        self.contador = 0
        self.puntos = self.puntos
        self.nivel_alcohol = self.nivel_alcohol
        vida_label.config(text=f"Vida: {self.vida}")
        contador_label.config(text=f"Movimientos: {self.contador}")
        puntos_label.config(text=f"Puntos:{self.puntos}")
        alcohol_label.config(text=f"Alcohol:{self.nivel_alcohol}")
        self.hormiga_oval = self.canvas.create_oval(self.x * 40, self.y * 40, (self.x + 1) * 40, (self.y + 1) * 40, fill="red")



    def reiniciar_hormiga(self, vida_label, contador_label,puntos_label,alcohol_label):
        """Reinicia la hormiga cuando muere."""
        self.x, self.y = self.start_x, self.start_y
        self.vida = 3  # Reinicia la vida
        self.contador = 0  # Reinicia el contador
        self.puntos = self.puntos
        self.nivel_alcohol = self.nivel_alcohol
        self.direccion = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Cambia la dirección
        self.hormiga_oval = self.canvas.create_oval(self.x * 40, self.y * 40, (self.x + 1) * 40, (self.y + 1) * 40, fill="red")
        vida_label.config(text=f"Vida: {self.vida}")
        contador_label.config(text=f"Movimientos: {self.contador}")
        puntos_label.config(text=f"Puntos:{self.puntos}")
        alcohol_label.config(text=f"Alcohol:{self.nivel_alcohol}")
        self.canvas.after(200, self.mover, vida_label, contador_label,puntos_label, alcohol_label)

    def comer(self,item):
        if isinstance(item,Azucar):
            item.consumir(self)
        elif isinstance(item,Vino):
            item.consumir(self)

    def modificar_salud(self,cantidad):
        self.vida = max(0,min(100,self.vida + cantidad))

    def modificar_nivel_alcohol(self,cantidad):
        self.nivel_alcohol = max(0,min(50,self.nivel_alcohol + cantidad))



class Azucar:
    def __init__(self, puntos=10):
        self.puntos = puntos

    def consumir(self,hormiga):
        hormiga.puntos += self.puntos
        print(f"Azúcar consumida. Puntos: {hormiga.puntos}")

class Vino:
    def __init__(self, nivel_alcohol=5):
        self.nivel_alcohol = nivel_alcohol

    def consumir(self,hormiga):
        hormiga.modificar_nivel_alcohol(self.nivel_alcohol)
        print(f"Vino consumido. Nivel de alcohol: {hormiga.nivel_alcohol}")




class MapaCanvas:
    def __init__(self, master, matriz):
        self.master = master
        self.matriz = matriz
        self.tamano_matriz = len(matriz)
        self.canvas = Canvas(self.master, width=self.tamano_matriz * 40, height=self.tamano_matriz * 40)
        self.canvas.pack()
        self.dibujar_mapa()
        self.canvas.bind("<Button-1>", self.seleccionar_celda)  # Bind para seleccionar celda

        self.hormiga = None  # Variable para la hormiga
        self.vida_label = None
        self.contador_label = None
        self.puntos_label = None
        self.alcohol_label=None
        self.tiempo = 0  # Inicializa el tiempo
        self.cronometro_corriendo = False  # Estado del cronómetro

    def inicializar_datos(self, vida_label, contador_label, puntos_label, alcohol_label):
        self.vida_label = vida_label
        self.contador_label = contador_label
        self.puntos_label = puntos_label
        self.alcohol_label = alcohol_label
        # Inicializar la hormiga con los valores iniciales
        self.hormiga = Hormiga(self.canvas, self.tamano_matriz)
        self.hormiga.vida = 3
        self.hormiga.contador = 0
        self.hormiga.puntos=0
        self.hormiga.alcohol = 0

        # Actualizar las etiquetas con los valores iniciales
        self.vida_label.config(text=f"Vida: {self.hormiga.vida}")
        self.contador_label.config(text=f"Tiempo: {self.tiempo}")
        self.puntos_label.config(text=f"Puntos: {self.hormiga.puntos}")
        self.alcohol_label.config(text=f"Alcohol: {self.hormiga.alcohol}")

    def seleccionar_celda(self, event):
        """Selecciona la celda en la que se hizo clic y comienza la simulación de la hormiga."""
        j = event.x // 40
        i = event.y // 40

        if 0 <= i < self.tamano_matriz and 0 <= j < self.tamano_matriz:
            # Establece la posición inicial de la hormiga
            self.hormiga.start_x, self.hormiga.start_y = j, i  # Guarda la posición de inicio
            self.hormiga.x, self.hormiga.y = j, i
            self.hormiga.mover(self.vida_label, self.contador_label, self.puntos_label, self.alcohol_label)  # Inicia el movimiento de la hormiga

    def dibujar_mapa(self):
        """Dibuja la matriz en el Canvas."""
        self.canvas.delete("all")  # Limpiar el canvas antes de dibujar
        self.rect_ids = []  # Lista para almacenar los IDs de los rectángulos
        for i in range(self.tamano_matriz):
            row_ids = []  # Lista para la fila actual
            for j in range(self.tamano_matriz):
                color = self.matriz[i][j]  # Asumimos que la matriz ya tiene colores como cadenas
                rect_id = self.canvas.create_rectangle(j * 40, i * 40, (j + 1) * 40, (i + 1) * 40, fill=color)
                row_ids.append(rect_id)  # Guarda el ID del rectángulo
            self.rect_ids.append(row_ids)  # Guarda la fila de IDs
