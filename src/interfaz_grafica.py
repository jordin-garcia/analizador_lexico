import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext, messagebox
from analizador_lexico import AnalizadorLexico


class InterfazGrafica:
    """
    Clase que maneja toda la interfaz gráfica del analizador léxico.
    """

    def __init__(self, root):
        """
        Inicializa la interfaz gráfica.

        Args:
            root: La ventana principal de tkinter
        """
        self.root = root
        self.analizador = AnalizadorLexico()
        self._configurar_ventana()
        self._crear_widgets()

    def _configurar_ventana(self):
        """
        Configura las propiedades básicas de la ventana principal.
        """
        self.root.title("Analizador Léxico")
        self.root.geometry("1000x700")

    def _crear_widgets(self):
        """
        Crea y configura todos los widgets de la interfaz.
        """
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Fila 1: Botones ---
        self._crear_botones(main_frame)

        # --- Fila 2: Editor de Texto y Resultados ---
        self._crear_area_contenido(main_frame)

    def _crear_botones(self, parent):
        """
        Crea la fila de botones en la parte superior.

        Args:
            parent: Widget padre donde se colocarán los botones
        """
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill=tk.X, pady=5)

        self.btn_cargar = ttk.Button(
            top_frame, text="Cargar Archivo (.txt)", command=self.cargar_archivo
        )
        self.btn_cargar.pack(side=tk.LEFT)

        self.btn_analizar = ttk.Button(
            top_frame, text="Analizar Código", command=self.analizar_codigo
        )
        self.btn_analizar.pack(side=tk.LEFT, padx=10)

        self.btn_limpiar = ttk.Button(
            top_frame, text="Limpiar", command=self.limpiar_todo
        )
        self.btn_limpiar.pack(side=tk.LEFT)

    def _crear_area_contenido(self, parent):
        """
        Crea el área de contenido con el editor de texto y las tablas de resultados.

        Args:
            parent: Widget padre donde se colocará el área de contenido
        """
        content_frame = ttk.Frame(parent)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        content_frame.grid_columnconfigure(
            1, weight=1
        )  # Columna de resultados se expande
        content_frame.grid_rowconfigure(0, weight=1)

        # Editor de texto
        self._crear_editor_texto(content_frame)

        # Área de resultados (tabla principal + tabla de resumen)
        self._crear_area_resultados(content_frame)

    def _crear_editor_texto(self, parent):
        """
        Crea el editor de texto para el código fuente.

        Args:
            parent: Widget padre donde se colocará el editor
        """
        editor_frame = ttk.LabelFrame(parent, text="Código Fuente", padding="5")
        editor_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        editor_frame.grid_rowconfigure(0, weight=1)
        self.texto_entrada = scrolledtext.ScrolledText(
            editor_frame, wrap=tk.WORD, width=50
        )
        self.texto_entrada.pack(fill=tk.BOTH, expand=True)

    def _crear_area_resultados(self, parent):
        """
        Crea el área de resultados con la tabla principal y la tabla de resumen.

        Args:
            parent: Widget padre donde se colocará el área de resultados
        """
        resultados_frame = ttk.Frame(parent)
        resultados_frame.grid(row=0, column=1, sticky="nsew")
        resultados_frame.grid_rowconfigure(0, weight=2)  # Tabla principal más grande
        resultados_frame.grid_rowconfigure(1, weight=1)  # Tabla resumen más pequeña
        resultados_frame.grid_columnconfigure(0, weight=1)

        # Tabla principal de tokens
        self._crear_tabla_principal(resultados_frame)

        # Tabla de resumen
        self._crear_tabla_resumen(resultados_frame)

    def _crear_tabla_principal(self, parent):
        """
        Crea la tabla principal para mostrar los tokens y errores.

        Args:
            parent: Widget padre donde se colocará la tabla
        """
        tabla_frame = ttk.LabelFrame(parent, text="Tokens y Errores", padding="5")
        tabla_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        tabla_frame.grid_rowconfigure(0, weight=1)
        tabla_frame.grid_columnconfigure(0, weight=1)

        self.tree_resultados = ttk.Treeview(
            tabla_frame, columns=("Tipo", "Valor", "Linea"), show="headings"
        )
        self.tree_resultados.heading("Tipo", text="Tipo")
        self.tree_resultados.heading("Valor", text="Token")
        self.tree_resultados.heading("Linea", text="Línea")

        self.tree_resultados.column("Tipo", width=120)
        self.tree_resultados.column("Valor", width=120)
        self.tree_resultados.column("Linea", width=50, anchor="center")

        # Scrollbar para la tabla principal
        scrollbar_principal = ttk.Scrollbar(
            tabla_frame, orient=tk.VERTICAL, command=self.tree_resultados.yview
        )
        self.tree_resultados.configure(yscroll=scrollbar_principal.set)

        self.tree_resultados.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_principal.pack(side=tk.RIGHT, fill=tk.Y)

    def _crear_tabla_resumen(self, parent):
        """
        Crea la tabla de resumen para mostrar estadísticas de tokens.

        Args:
            parent: Widget padre donde se colocará la tabla
        """
        resumen_frame = ttk.LabelFrame(parent, text="Resumen de Tokens", padding="5")
        resumen_frame.grid(row=1, column=0, sticky="nsew")
        resumen_frame.grid_rowconfigure(0, weight=1)
        resumen_frame.grid_columnconfigure(0, weight=1)

        self.tree_resumen = ttk.Treeview(
            resumen_frame, columns=("Tipo", "Token", "Cantidad"), show="headings"
        )
        self.tree_resumen.heading("Tipo", text="Tipo")
        self.tree_resumen.heading("Token", text="Token")
        self.tree_resumen.heading("Cantidad", text="Cantidad")

        self.tree_resumen.column("Tipo", width=120)
        self.tree_resumen.column("Token", width=120)
        self.tree_resumen.column("Cantidad", width=80, anchor="center")

        # Scrollbar para la tabla de resumen
        scrollbar_resumen = ttk.Scrollbar(
            resumen_frame, orient=tk.VERTICAL, command=self.tree_resumen.yview
        )
        self.tree_resumen.configure(yscroll=scrollbar_resumen.set)

        self.tree_resumen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_resumen.pack(side=tk.RIGHT, fill=tk.Y)

    def cargar_archivo(self):
        """
        Abre un diálogo para cargar un archivo de texto y lo muestra en el editor.
        """
        filepath = filedialog.askopenfilename(
            title="Abrir archivo de texto",
            filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")),
        )
        if not filepath:
            return

        try:
            # Intentar UTF-8 primero, luego latin-1 como fallback
            try:
                with open(filepath, "r", encoding="utf-8") as file:
                    contenido = file.read()
            except UnicodeDecodeError:
                with open(filepath, "r", encoding="latin-1") as file:
                    contenido = file.read()

            self.texto_entrada.delete("1.0", tk.END)
            self.texto_entrada.insert("1.0", contenido)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")

    def analizar_codigo(self):
        """
        Analiza el código en el editor y muestra los resultados en las tablas.
        """
        # Limpiar resultados anteriores
        self._limpiar_tablas()

        codigo = self.texto_entrada.get("1.0", tk.END)
        tokens = self.analizador.analizar(codigo)
        errores = self.analizador.obtener_errores(tokens)

        if errores:
            # Mostrar solo errores en la tabla principal
            self._mostrar_errores(errores)
            # Limpiar tabla de resumen cuando hay errores
            self._limpiar_tabla_resumen()
        else:
            # Mostrar lista completa de tokens en la tabla principal
            self._mostrar_lista_completa_tokens(tokens)
            # Mostrar resumen en la tabla de resumen
            self._mostrar_resumen_tokens(tokens)

    def _limpiar_tablas(self):
        """
        Limpia ambas tablas de resultados.
        """
        # Limpiar tabla principal
        for i in self.tree_resultados.get_children():
            self.tree_resultados.delete(i)

        # Limpiar tabla de resumen
        for i in self.tree_resumen.get_children():
            self.tree_resumen.delete(i)

    def _limpiar_tabla_resumen(self):
        """
        Limpia solo la tabla de resumen.
        """
        for i in self.tree_resumen.get_children():
            self.tree_resumen.delete(i)

    def _mostrar_errores(self, errores):
        """
        Muestra los errores encontrados en la tabla principal.

        Args:
            errores (list): Lista de tokens de error
        """
        self.tree_resultados.heading("Tipo", text="Error")
        self.tree_resultados.heading("Valor", text="Detalle")
        self.tree_resultados.heading("Linea", text="Línea")
        for tipo, valor, linea in errores:
            self.tree_resultados.insert("", tk.END, values=(tipo, valor, linea))

    def _mostrar_lista_completa_tokens(self, tokens):
        """
        Muestra la lista completa de tokens en la tabla principal.

        Args:
            tokens (list): Lista de tokens
        """
        # Configurar la tabla para la lista completa
        self.tree_resultados.heading("Tipo", text="Tipo")
        self.tree_resultados.heading("Valor", text="Token")
        self.tree_resultados.heading("Linea", text="Línea")

        # Mostrar todos los tokens en orden
        for tipo, valor, linea in tokens:
            self.tree_resultados.insert("", tk.END, values=(tipo, valor, linea))

    def _mostrar_resumen_tokens(self, tokens):
        """
        Muestra un resumen de los tokens en la tabla de resumen.

        Args:
            tokens (list): Lista de tokens
        """
        conteo_tokens = self.analizador.generar_resumen_tokens(tokens)

        # Llenar la tabla de resumen
        for (valor, tipo), cantidad in sorted(conteo_tokens.items()):
            self.tree_resumen.insert("", tk.END, values=(tipo, valor, cantidad))

    def limpiar_todo(self):
        """
        Limpia el editor de texto y ambas tablas de resultados.
        """
        self.texto_entrada.delete("1.0", tk.END)
        self._limpiar_tablas()

        # Restaurar encabezados originales de la tabla principal
        self.tree_resultados.heading("Tipo", text="Tipo")
        self.tree_resultados.heading("Valor", text="Token")
        self.tree_resultados.heading("Linea", text="Línea")
