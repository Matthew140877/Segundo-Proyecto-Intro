from tkinter import *

class MatrizApp:
    def __init__(self, master):
        self.master = master
        master.title("Matriz 10x10 con Muros")
        
        # Eliminar el padding del frame principal
        master.grid_propagate(False)
        master.configure(width=400, height=400)  # Ajusta estos valores según sea necesario

        self.buttons = []
        self.current_color = "green"  # Color inicial
        self.color_names = {
            "green": "Veneno",
            "brown": "Muro",
            "yellow": "Salida"
        }

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
        self.current_color = color  # Cambia el color actual

    def toggle_wall(self, i, j):
        button = self.buttons[i][j]
        current_color = button.cget("background")

        # Cambiar el color del botón al color actual
        if current_color == "SystemButtonFace" or current_color == "":
            button.configure(bg=self.current_color)  # Cambia al color seleccionado
        else:
            button.configure(bg="SystemButtonFace")  # Restablece al color por defecto

    def investigar(self):
        # Imprimir el nombre del color seleccionado actualmente
        print("El color seleccionado es:", self.color_names[self.current_color])



root = Tk()
app = MatrizApp(root)
root.mainloop()