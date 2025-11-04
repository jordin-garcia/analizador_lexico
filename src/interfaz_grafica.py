import tkinter as tk
from tkinter import filedialog, ttk, messagebox
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
        self._configurar_tema_oscuro()
        self._configurar_ventana()
        self._crear_widgets()

    def _configurar_tema_oscuro(self):
        """
        Configura el tema oscuro moderno para toda la interfaz.
        """
        # Colores del tema oscuro
        self.colores = {
            "bg_principal": "#1e1e1e",  # Fondo principal (muy oscuro)
            "bg_secundario": "#2d2d2d",  # Fondo secundario (oscuro)
            "bg_terciario": "#252526",  # Fondo terciario (entre principal y secundario)
            "fg_principal": "#ffffff",  # Texto principal (blanco)
            "fg_secundario": "#cccccc",  # Texto secundario (gris claro)
            "fg_deshabilitado": "#6e6e6e",  # Texto deshabilitado
            "acento": "#0078d4",  # Color de acento (azul moderno)
            "acento_hover": "#1e88e5",  # Acento hover (azul más claro)
            "acento_press": "#005a9e",  # Acento presionado (azul más oscuro)
            "borde": "#3f3f3f",  # Color de bordes
            "seleccion": "#264f78",  # Color de selección
            "error": "#f44336",  # Color de error (rojo)
            "exito": "#4caf50",  # Color de éxito (verde)
            "advertencia": "#ff9800",  # Color de advertencia (naranja)
        }

        # Configurar ventana principal
        self.root.configure(bg=self.colores["bg_principal"])

        # Configurar estilo ttk
        style = ttk.Style()
        style.theme_use("clam")  # Tema base que permite más personalización

        # Configurar Frame
        style.configure("TFrame", background=self.colores["bg_principal"])

        # Configurar LabelFrame
        style.configure(
            "TLabelframe",
            background=self.colores["bg_secundario"],
            foreground=self.colores["fg_principal"],
            bordercolor=self.colores["borde"],
            borderwidth=1,
        )
        style.configure(
            "TLabelframe.Label",
            background=self.colores["bg_secundario"],
            foreground=self.colores["fg_principal"],
            font=("Segoe UI", 10, "bold"),
        )

        # Configurar Button
        style.configure(
            "TButton",
            background=self.colores["acento"],
            foreground=self.colores["fg_principal"],
            bordercolor=self.colores["acento"],
            focuscolor=self.colores["acento_hover"],
            lightcolor=self.colores["acento"],
            darkcolor=self.colores["acento_press"],
            borderwidth=1,
            font=("Segoe UI", 9),
            padding=(10, 5),
        )
        style.map(
            "TButton",
            background=[
                ("active", self.colores["acento_hover"]),
                ("pressed", self.colores["acento_press"]),
                ("disabled", self.colores["bg_terciario"]),
            ],
            foreground=[("disabled", self.colores["fg_deshabilitado"])],
        )

        # Configurar Treeview
        style.configure(
            "Treeview",
            background=self.colores["bg_secundario"],
            foreground=self.colores["fg_principal"],
            fieldbackground=self.colores["bg_secundario"],
            bordercolor=self.colores["borde"],
            borderwidth=1,
        )
        style.configure(
            "Treeview.Heading",
            background=self.colores["bg_terciario"],
            foreground=self.colores["fg_principal"],
            bordercolor=self.colores["borde"],
            font=("Segoe UI", 9, "bold"),
            relief="flat",
        )
        style.map("Treeview.Heading", background=[("active", self.colores["acento"])])
        style.map(
            "Treeview",
            background=[("selected", self.colores["seleccion"])],
            foreground=[("selected", self.colores["fg_principal"])],
        )

        # Configurar Scrollbar
        style.configure(
            "Vertical.TScrollbar",
            background=self.colores["bg_terciario"],
            troughcolor=self.colores["bg_principal"],
            bordercolor=self.colores["borde"],
            arrowcolor=self.colores["fg_secundario"],
            borderwidth=0,
        )
        style.map(
            "Vertical.TScrollbar",
            background=[
                ("active", self.colores["acento"]),
                ("pressed", self.colores["acento_press"]),
            ],
        )

        style.configure(
            "Horizontal.TScrollbar",
            background=self.colores["bg_terciario"],
            troughcolor=self.colores["bg_principal"],
            bordercolor=self.colores["borde"],
            arrowcolor=self.colores["fg_secundario"],
            borderwidth=0,
        )
        style.map(
            "Horizontal.TScrollbar",
            background=[
                ("active", self.colores["acento"]),
                ("pressed", self.colores["acento_press"]),
            ],
        )

    def _configurar_ventana(self):
        """
        Configura las propiedades básicas de la ventana principal.
        """
        self.root.title("Analizador Léxico, Sintáctico y Semántico")
        # Abrir en pantalla completa
        self.root.state("zoomed")  # Para Windows
        # Para Linux/Mac también podríamos usar: self.root.attributes('-zoomed', True)

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

        self.btn_guardar = ttk.Button(
            top_frame, text="Guardar Documento", command=self.guardar_archivo
        )
        self.btn_guardar.pack(side=tk.LEFT, padx=10)

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
        Crea el editor de texto para el código fuente con números de línea.

        Args:
            parent: Widget padre donde se colocará el editor
        """
        editor_frame = ttk.LabelFrame(parent, text="Código Fuente", padding="5")
        editor_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(1, weight=1)

        # Frame interno para contener números de línea y texto
        text_frame = ttk.Frame(editor_frame)
        text_frame.grid(row=0, column=0, sticky="nsew")
        editor_frame.grid_rowconfigure(0, weight=1)
        editor_frame.grid_columnconfigure(0, weight=1)

        # Widget de números de línea
        self.numeros_linea = tk.Text(
            text_frame,
            width=4,
            padx=3,
            pady=5,
            takefocus=0,
            border=0,
            background=self.colores["bg_terciario"],
            foreground=self.colores["fg_secundario"],
            state="disabled",
            wrap="none",
            font=("Consolas", 10),
            relief="flat",
        )
        self.numeros_linea.pack(side=tk.LEFT, fill=tk.Y)

        # Editor de texto principal (sin ajuste de línea para mantener formato original)
        self.texto_entrada = tk.Text(
            text_frame,
            wrap="none",
            width=70,
            pady=5,
            undo=True,
            background=self.colores["bg_secundario"],
            foreground=self.colores["fg_principal"],
            insertbackground=self.colores["fg_principal"],  # Color del cursor
            selectbackground=self.colores["seleccion"],
            selectforeground=self.colores["fg_principal"],
            font=("Consolas", 10),
            relief="flat",
            borderwidth=0,
        )
        self.texto_entrada.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar vertical para el editor
        scrollbar_v = ttk.Scrollbar(
            text_frame, orient=tk.VERTICAL, command=self._on_scroll
        )
        scrollbar_v.pack(side=tk.RIGHT, fill=tk.Y)
        self.texto_entrada.config(yscrollcommand=scrollbar_v.set)

        # Scrollbar horizontal para el editor
        scrollbar_h = ttk.Scrollbar(
            editor_frame, orient=tk.HORIZONTAL, command=self.texto_entrada.xview
        )
        scrollbar_h.grid(row=1, column=0, sticky="ew")
        self.texto_entrada.config(xscrollcommand=scrollbar_h.set)

        # Vincular eventos para actualizar números de línea
        self.texto_entrada.bind("<<Modified>>", self._actualizar_numeros_linea)
        self.texto_entrada.bind("<KeyRelease>", self._actualizar_numeros_linea)
        self.texto_entrada.bind("<ButtonRelease>", self._actualizar_numeros_linea)

        # Inicializar números de línea
        self._actualizar_numeros_linea()

    def _crear_area_resultados(self, parent):
        """
        Crea el área de resultados con las tablas de tokens, resumen y símbolos.

        Args:
            parent: Widget padre donde se colocará el área de resultados
        """
        resultados_frame = ttk.Frame(parent)
        resultados_frame.grid(row=0, column=1, sticky="nsew")
        resultados_frame.grid_rowconfigure(0, weight=2)  # Tabla principal más grande
        resultados_frame.grid_rowconfigure(1, weight=1)  # Tabla resumen
        resultados_frame.grid_rowconfigure(2, weight=1)  # Tabla de símbolos
        resultados_frame.grid_columnconfigure(0, weight=1)

        # Tabla principal de tokens
        self._crear_tabla_principal(resultados_frame)

        # Tabla de resumen
        self._crear_tabla_resumen(resultados_frame)

        # Tabla de símbolos
        self._crear_tabla_simbolos(resultados_frame)

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

        # Frame interno para manejar scrollbars
        tree_frame = tk.Frame(tabla_frame, bg=self.colores["bg_secundario"])
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_resultados = ttk.Treeview(
            tree_frame, columns=("Tipo", "Valor", "Linea"), show="headings"
        )
        self.tree_resultados.heading("Tipo", text="Tipo")
        self.tree_resultados.heading("Valor", text="Token")
        self.tree_resultados.heading("Linea", text="Línea")

        # Anchos más grandes y con stretch para adaptarse al contenido
        self.tree_resultados.column("Tipo", width=150, minwidth=120, stretch=True)
        self.tree_resultados.column("Valor", width=600, minwidth=400, stretch=True)
        self.tree_resultados.column(
            "Linea", width=80, minwidth=60, anchor="center", stretch=False
        )

        # Scrollbar vertical
        scrollbar_vertical = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree_resultados.yview
        )
        # Scrollbar horizontal
        scrollbar_horizontal = ttk.Scrollbar(
            tree_frame, orient=tk.HORIZONTAL, command=self.tree_resultados.xview
        )
        self.tree_resultados.configure(
            yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set
        )

        # Posicionar los elementos con grid para mejor control
        self.tree_resultados.grid(row=0, column=0, sticky="nsew")
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

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

        # Frame interno para manejar scrollbars
        tree_frame = tk.Frame(resumen_frame, bg=self.colores["bg_secundario"])
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_resumen = ttk.Treeview(
            tree_frame, columns=("Tipo", "Token", "Cantidad"), show="headings"
        )
        self.tree_resumen.heading("Tipo", text="Tipo")
        self.tree_resumen.heading("Token", text="Token")
        self.tree_resumen.heading("Cantidad", text="Cantidad")

        # Anchos más grandes y con stretch
        self.tree_resumen.column("Tipo", width=200, minwidth=150, stretch=True)
        self.tree_resumen.column("Token", width=300, minwidth=200, stretch=True)
        self.tree_resumen.column(
            "Cantidad", width=100, minwidth=80, anchor="center", stretch=False
        )

        # Scrollbar vertical
        scrollbar_vertical = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree_resumen.yview
        )
        # Scrollbar horizontal
        scrollbar_horizontal = ttk.Scrollbar(
            tree_frame, orient=tk.HORIZONTAL, command=self.tree_resumen.xview
        )
        self.tree_resumen.configure(
            yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set
        )

        # Posicionar los elementos con grid
        self.tree_resumen.grid(row=0, column=0, sticky="nsew")
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def _crear_tabla_simbolos(self, parent):
        """
        Crea la tabla de símbolos para mostrar variables y funciones declaradas.

        Args:
            parent: Widget padre donde se colocará la tabla
        """
        simbolos_frame = ttk.LabelFrame(parent, text="Tabla de Símbolos", padding="5")
        simbolos_frame.grid(row=2, column=0, sticky="nsew", pady=(5, 0))
        simbolos_frame.grid_rowconfigure(0, weight=1)
        simbolos_frame.grid_columnconfigure(0, weight=1)

        # Frame interno para manejar scrollbars
        tree_frame = tk.Frame(simbolos_frame, bg=self.colores["bg_secundario"])
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree_simbolos = ttk.Treeview(
            tree_frame,
            columns=("Nombre", "Tipo", "Categoría", "Ámbito", "Línea"),
            show="headings",
        )
        self.tree_simbolos.heading("Nombre", text="Nombre")
        self.tree_simbolos.heading("Tipo", text="Tipo")
        self.tree_simbolos.heading("Categoría", text="Categoría")
        self.tree_simbolos.heading("Ámbito", text="Ámbito")
        self.tree_simbolos.heading("Línea", text="Línea")

        # Anchos más grandes y con stretch
        self.tree_simbolos.column("Nombre", width=150, minwidth=120, stretch=True)
        self.tree_simbolos.column("Tipo", width=120, minwidth=100, stretch=True)
        self.tree_simbolos.column("Categoría", width=120, minwidth=100, stretch=True)
        self.tree_simbolos.column("Ámbito", width=150, minwidth=120, stretch=True)
        self.tree_simbolos.column(
            "Línea", width=80, minwidth=60, anchor="center", stretch=False
        )

        # Scrollbar vertical
        scrollbar_vertical = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.tree_simbolos.yview
        )
        # Scrollbar horizontal
        scrollbar_horizontal = ttk.Scrollbar(
            tree_frame, orient=tk.HORIZONTAL, command=self.tree_simbolos.xview
        )
        self.tree_simbolos.configure(
            yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set
        )

        # Posicionar los elementos con grid
        self.tree_simbolos.grid(row=0, column=0, sticky="nsew")
        scrollbar_vertical.grid(row=0, column=1, sticky="ns")
        scrollbar_horizontal.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def cargar_archivo(self):
        """
        Abre un diálogo para cargar un archivo de texto y lo muestra en el editor.
        """
        filepath = filedialog.askopenfilename(
            title="Abrir archivo de texto", filetypes=[("Archivos de Texto", "*.txt")]
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
            # Actualizar números de línea después de cargar el archivo
            self._actualizar_numeros_linea()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")

    def guardar_archivo(self):
        """
        Abre un diálogo para guardar el contenido del editor en un archivo de texto.
        """
        contenido = self.texto_entrada.get("1.0", tk.END)

        # Verificar si hay contenido para guardar
        if not contenido.strip():
            messagebox.showwarning("Advertencia", "No hay contenido para guardar.")
            return

        # Abrir diálogo para seleccionar ubicación y nombre del archivo
        filepath = filedialog.asksaveasfilename(
            title="Guardar archivo",
            defaultextension=".txt",
            filetypes=(("Archivos de Texto", "*.txt"), ("Todos los archivos", "*.*")),
        )

        if not filepath:
            return  # Usuario canceló

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(contenido)

            messagebox.showinfo(
                "Éxito", f"Archivo guardado exitosamente en:\n{filepath}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")

    def analizar_codigo(self):
        """
        Analiza el código en el editor y muestra los resultados en las tablas.
        Realiza análisis léxico, sintáctico y semántico en secuencia.
        """
        # Limpiar resultados anteriores
        self._limpiar_tablas()

        codigo = self.texto_entrada.get("1.0", tk.END)

        # Verificar si hay código para analizar
        if not codigo.strip():
            messagebox.showwarning("Advertencia", "No hay código para analizar.")
            return

        # ============================================
        # FASE 1: ANÁLISIS LÉXICO
        # ============================================
        tokens = self.analizador.analizar(codigo)
        errores_lexicos = self.analizador.obtener_errores(tokens)

        if errores_lexicos:
            self._mostrar_errores(errores_lexicos, "LÉXICO")
            self._limpiar_tabla_resumen()
            return

        # ============================================
        # FASE 2: ANÁLISIS SINTÁCTICO
        # ============================================
        try:
            from analizador_sintactico import AnalizadorSintactico

            analizador_sintactico = AnalizadorSintactico(tokens)
            ast, errores_sintacticos = analizador_sintactico.analizar()

            if errores_sintacticos:
                self._mostrar_errores(errores_sintacticos, "SINTÁCTICO")
                self._limpiar_tabla_resumen()
                return

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error en el análisis sintáctico:\n{str(e)}",
            )
            return

        # ============================================
        # FASE 3: ANÁLISIS SEMÁNTICO
        # ============================================
        try:
            from analizador_semantico import AnalizadorSemantico

            analizador_semantico = AnalizadorSemantico(ast)
            errores_semanticos = analizador_semantico.analizar()

            if errores_semanticos:
                self._mostrar_errores(errores_semanticos, "SEMÁNTICO")
                self._limpiar_tabla_resumen()
                return

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error en el análisis semántico:\n{str(e)}",
            )
            return

        # ============================================
        # ANÁLISIS EXITOSO - MOSTRAR RESULTADOS
        # ============================================
        self._mostrar_lista_completa_tokens(tokens)
        self._mostrar_resumen_tokens(tokens)
        self._mostrar_tabla_simbolos(analizador_semantico.tabla_simbolos)

        messagebox.showinfo(
            "✓ Análisis Completo Exitoso",
            "El código es correcto:\n\n"
            "✓ Análisis Léxico\n"
            "✓ Análisis Sintáctico\n"
            "✓ Análisis Semántico\n\n"
            "No se encontraron errores.",
        )

    def _limpiar_tablas(self):
        """
        Limpia todas las tablas de resultados.
        """
        # Limpiar tabla principal
        for i in self.tree_resultados.get_children():
            self.tree_resultados.delete(i)

        # Limpiar tabla de resumen
        for i in self.tree_resumen.get_children():
            self.tree_resumen.delete(i)

        # Limpiar tabla de símbolos
        for i in self.tree_simbolos.get_children():
            self.tree_simbolos.delete(i)

    def _limpiar_tabla_resumen(self):
        """
        Limpia solo la tabla de resumen.
        """
        for i in self.tree_resumen.get_children():
            self.tree_resumen.delete(i)

    def _mostrar_errores(self, errores, tipo_analisis="LÉXICO"):
        """
        Muestra los errores encontrados en la tabla principal.

        Args:
            errores (list): Lista de errores (tuplas o diccionarios)
            tipo_analisis (str): Tipo de análisis ("LÉXICO", "SINTÁCTICO", "SEMÁNTICO")
        """
        self.tree_resultados.heading("Tipo", text="Error")
        self.tree_resultados.heading("Valor", text="Detalle")
        self.tree_resultados.heading("Linea", text="Línea")

        for error in errores:
            if isinstance(error, dict):
                # Formato nuevo (sintáctico/semántico)
                tipo = error.get("tipo", tipo_analisis)
                mensaje = error.get("mensaje", "Error desconocido")
                detalle = error.get("detalle", "")
                if detalle:
                    mensaje = f"{mensaje} - {detalle}"
                linea = error.get("linea", "?")
            else:
                # Usar tipo_analisis en lugar del primer elemento de la tupla
                tipo = tipo_analisis
                _, mensaje, linea = error

            self.tree_resultados.insert("", tk.END, values=(tipo, mensaje, linea))

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

    def _mostrar_tabla_simbolos(self, tabla_simbolos):
        """
        Muestra la tabla de símbolos en la interfaz.

        Args:
            tabla_simbolos (dict): Diccionario con los símbolos declarados
        """
        # Limpiar tabla
        for i in self.tree_simbolos.get_children():
            self.tree_simbolos.delete(i)

        # Llenar con los símbolos
        for clave, info in sorted(tabla_simbolos.items()):
            # La clave es "ambito:nombre", separamos
            partes = clave.split(":", 1)
            nombre = partes[1] if len(partes) > 1 else partes[0]

            self.tree_simbolos.insert(
                "",
                tk.END,
                values=(
                    nombre,
                    info["tipo"],
                    info["categoria"],
                    info["ambito"],
                    info["linea"],
                ),
            )

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

        # Actualizar números de línea
        self._actualizar_numeros_linea()

    def _actualizar_numeros_linea(self, event=None):
        """
        Actualiza los números de línea en el widget correspondiente.

        Args:
            event: Evento que disparó la actualización (opcional)
        """
        # Obtener el contenido actual
        lineas_texto = self.texto_entrada.get("1.0", "end-1c").split("\n")
        numero_lineas = len(lineas_texto)

        # Generar números de línea
        numeros = "\n".join(str(i) for i in range(1, numero_lineas + 1))

        # Actualizar el widget de números de línea
        self.numeros_linea.config(state="normal")
        self.numeros_linea.delete("1.0", tk.END)
        self.numeros_linea.insert("1.0", numeros)
        self.numeros_linea.config(state="disabled")

        # Sincronizar scroll
        self._sincronizar_scroll()

        # Reset del flag de modificación
        if event:
            self.texto_entrada.edit_modified(False)

    def _on_scroll(self, *args):
        """
        Maneja el evento de scroll para sincronizar ambos widgets de texto.

        Args:
            *args: Argumentos del evento de scroll
        """
        # Aplicar scroll a ambos widgets
        self.texto_entrada.yview(*args)
        self.numeros_linea.yview(*args)

    def _sincronizar_scroll(self):
        """
        Sincroniza el scroll entre el editor de texto y los números de línea.
        """
        # Obtener posición actual del scroll
        primera_linea = self.texto_entrada.yview()[0]

        # Aplicar a números de línea
        self.numeros_linea.yview_moveto(primera_linea)
