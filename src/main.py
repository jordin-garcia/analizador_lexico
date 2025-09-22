import tkinter as tk
from interfaz_grafica import InterfazGrafica


def main():
    """
    Función principal que inicializa y ejecuta la aplicación del analizador léxico.
    """
    # Crear la ventana principal
    app_root = tk.Tk()

    # Crear la interfaz gráfica
    InterfazGrafica(app_root)

    # Iniciar el bucle principal de la aplicación
    app_root.mainloop()


if __name__ == "__main__":
    main()
