"""
Analizador Sintáctico (Parser) para el lenguaje de programación simple.
Implementa un parser descendente recursivo que construye un Árbol de Sintaxis Abstracta (AST).
"""


class NodoAST:
    """
    Representa un nodo en el Árbol de Sintaxis Abstracta (AST).
    """

    def __init__(self, tipo, valor=None, hijos=None, linea=None):
        """
        Inicializa un nodo del AST.

        Args:
            tipo (str): Tipo de nodo (ej: 'DECLARACION_VARIABLE', 'EXPRESION', etc.)
            valor: Valor asociado al nodo (nombre de variable, operador, literal, etc.)
            hijos (list): Lista de nodos hijos
            linea (int): Número de línea en el código fuente
        """
        self.tipo = tipo
        self.valor = valor
        self.hijos = hijos if hijos is not None else []
        self.linea = linea

    def agregar_hijo(self, nodo):
        """
        Agrega un nodo hijo a la lista de hijos.

        Args:
            nodo (NodoAST): Nodo hijo a agregar
        """
        if nodo is not None:
            self.hijos.append(nodo)

    def __repr__(self):
        """
        Representación legible del nodo para debugging.

        Returns:
            str: Representación del nodo
        """
        if self.valor:
            return f"NodoAST(tipo={self.tipo}, valor={self.valor}, linea={self.linea})"
        return f"NodoAST(tipo={self.tipo}, linea={self.linea})"


class AnalizadorSintactico:
    """
    Analizador sintáctico que implementa un parser descendente recursivo.
    Verifica la estructura gramatical del código y construye un AST.
    """

    # Tipos de datos válidos del lenguaje
    TIPOS_VALIDOS = {"entero", "decimal", "booleano", "cadena"}

    # Palabras reservadas que representan estructuras de control
    ESTRUCTURAS_CONTROL = {"si", "mientras", "hacer"}

    def __init__(self, tokens):
        """
        Inicializa el analizador sintáctico.

        Args:
            tokens (list): Lista de tuplas (tipo_token, valor, linea) del analizador léxico
        """
        self.tokens = tokens
        self.posicion = 0
        self.token_actual = None
        self.errores = []

        # Inicializar el primer token
        if self.tokens:
            self.token_actual = self.tokens[0]

    def analizar(self):
        """
        Inicia el análisis sintáctico del programa completo.

        Returns:
            tuple: (arbol_sintactico, errores)
                - arbol_sintactico: NodoAST raíz del programa o None si hay errores
                - errores: Lista de errores sintácticos encontrados
        """
        try:
            ast = self._programa()
            return (ast, self.errores)
        except Exception as e:
            self._agregar_error(
                f"Error inesperado durante el análisis sintáctico: {str(e)}",
                self._linea_actual(),
            )
            return (None, self.errores)

    def _avanzar(self):
        """
        Avanza al siguiente token en la lista.
        """
        self.posicion += 1
        if self.posicion < len(self.tokens):
            self.token_actual = self.tokens[self.posicion]
        else:
            self.token_actual = None

    def _token_actual_es(self, tipo_esperado):
        """
        Verifica si el token actual es del tipo esperado.

        Args:
            tipo_esperado (str): Tipo de token esperado

        Returns:
            bool: True si el token actual es del tipo esperado, False en caso contrario
        """
        if self.token_actual is None:
            return False
        return self.token_actual[0] == tipo_esperado

    def _valor_actual_es(self, valor_esperado):
        """
        Verifica si el valor del token actual coincide con el esperado.

        Args:
            valor_esperado (str): Valor esperado del token

        Returns:
            bool: True si el valor coincide, False en caso contrario
        """
        if self.token_actual is None:
            return False
        return self.token_actual[1] == valor_esperado

    def _consumir(self, tipo_esperado, mensaje_error=None):
        """
        Consume un token del tipo esperado o genera un error.

        Args:
            tipo_esperado (str): Tipo de token que se espera consumir
            mensaje_error (str): Mensaje personalizado de error (opcional)

        Returns:
            tuple: Token consumido (tipo, valor, linea) o None si hay error
        """
        if self.token_actual is None:
            if mensaje_error:
                self._agregar_error(mensaje_error, self._linea_actual())
            else:
                self._agregar_error(
                    f"Se esperaba '{tipo_esperado}' pero se llegó al final del archivo",
                    self._linea_actual(),
                )
            return None

        if self._token_actual_es(tipo_esperado):
            token = self.token_actual
            self._avanzar()
            return token
        else:
            if mensaje_error:
                self._agregar_error(mensaje_error, self._linea_actual())
            else:
                self._agregar_error(
                    f"Se esperaba '{tipo_esperado}' pero se encontró '{self.token_actual[0]}'",
                    self._linea_actual(),
                    f"Token encontrado: '{self.token_actual[1]}'",
                )
            return None

    def _linea_actual(self):
        """
        Obtiene el número de línea del token actual.

        Returns:
            int: Número de línea actual o -1 si no hay token actual
        """
        if self.token_actual:
            return self.token_actual[2]
        return -1

    def _agregar_error(self, mensaje, linea, detalle=""):
        """
        Agrega un error a la lista de errores sintácticos.

        Args:
            mensaje (str): Mensaje descriptivo del error
            linea (int): Número de línea donde ocurrió el error
            detalle (str): Información adicional sobre el error (opcional)
        """
        self.errores.append(
            {
                "tipo": "SINTÁCTICO",
                "mensaje": mensaje,
                "linea": linea,
                "detalle": detalle,
            }
        )

    # ========================================================================
    # MÉTODOS PARA CADA REGLA DE LA GRAMÁTICA
    # ========================================================================

    def _programa(self):
        """
        Regla: PROGRAMA → DECLARACION*

        Punto de entrada del parser. Procesa todas las declaraciones del programa.

        Returns:
            NodoAST: Nodo raíz del programa
        """
        nodo_programa = NodoAST("PROGRAMA", linea=1)

        while self.token_actual is not None:
            declaracion = self._declaracion()
            if declaracion:
                nodo_programa.agregar_hijo(declaracion)

            # Si hay errores, detener el análisis
            if self.errores:
                break

        return nodo_programa

    def _declaracion(self):
        """
        Regla: DECLARACION → DECLARACION_VARIABLE
                            | DECLARACION_FUNCION
                            | ESTRUCTURA_CONTROL
                            | ASIGNACION

        Determina el tipo de declaración y delega al método apropiado.

        Returns:
            NodoAST: Nodo de la declaración o None si hay error
        """
        if self.token_actual is None:
            return None

        # Verificar si es una palabra reservada de tipo
        if (
            self._token_actual_es("PALABRA_RESERVADA")
            and self.token_actual[1] in self.TIPOS_VALIDOS
        ):
            # Puede ser declaración de variable o función
            return self._declaracion_variable_o_funcion()

        # Verificar si es una estructura de control
        elif (
            self._token_actual_es("PALABRA_RESERVADA")
            and self.token_actual[1] in self.ESTRUCTURAS_CONTROL
        ):
            return self._estructura_control()

        # Verificar si es una asignación (IDENTIFICADOR = EXPRESION;)
        elif self._token_actual_es("IDENTIFICADOR"):
            # Verificar si parece un tipo de dato inválido
            # Patrón: IDENTIFICADOR IDENTIFICADOR = ...
            if self.posicion + 1 < len(self.tokens):
                siguiente_token = self.tokens[self.posicion + 1]
                if siguiente_token[0] == "IDENTIFICADOR":
                    # Probablemente un tipo de dato inválido
                    tipo_invalido = self.token_actual[1]
                    linea = self.token_actual[2]
                    self._agregar_error(
                        f"Tipo de dato inválido: '{tipo_invalido}'",
                        linea,
                        "Los tipos válidos son: entero, decimal, cadena, booleano",
                    )
                    self._avanzar()  # Saltar el tipo inválido
                    return None

            return self._asignacion()

        else:
            self._agregar_error(
                "Declaración inesperada: se esperaba un tipo de dato o palabra clave de control",
                self._linea_actual(),
                f"Token encontrado: '{self.token_actual[1]}'",
            )
            self._avanzar()  # Intentar recuperarse
            return None

    def _declaracion_variable_o_funcion(self):
        """
        Distingue entre declaración de variable y función.
        Ambas comienzan con TIPO IDENTIFICADOR, pero la función tiene paréntesis.

        Returns:
            NodoAST: Nodo de declaración de variable o función
        """
        # Guardar posición para poder retroceder si es necesario
        tipo_token = self.token_actual
        tipo = tipo_token[1]
        linea = tipo_token[2]
        self._avanzar()

        # Debe seguir un identificador
        if not self._token_actual_es("IDENTIFICADOR"):
            self._agregar_error(
                f"Se esperaba un identificador después del tipo '{tipo}'",
                self._linea_actual(),
            )
            return None

        nombre_token = self.token_actual
        nombre = nombre_token[1]
        self._avanzar()

        # Verificar si es función (tiene paréntesis) o variable (tiene asignación)
        if self._token_actual_es("PARENTESIS_IZQ"):
            # Es una función
            return self._declaracion_funcion_continuar(tipo, nombre, linea)
        elif self._token_actual_es("ASIGNACION"):
            # Es una variable
            return self._declaracion_variable_continuar(tipo, nombre, linea)
        else:
            self._agregar_error(
                f"Se esperaba '=' o '(' después del identificador '{nombre}'",
                self._linea_actual(),
                f"Token encontrado: '{self.token_actual[1] if self.token_actual else 'EOF'}'",
            )
            return None

    def _declaracion_variable_continuar(self, tipo, nombre, linea):
        """
        Continúa el análisis de una declaración de variable.
        Regla: TIPO IDENTIFICADOR '=' EXPRESION ';'

        Args:
            tipo (str): Tipo de la variable
            nombre (str): Nombre de la variable
            linea (int): Número de línea

        Returns:
            NodoAST: Nodo de declaración de variable
        """
        nodo = NodoAST("DECLARACION_VARIABLE", linea=linea)

        # Agregar tipo como hijo
        nodo.agregar_hijo(NodoAST("TIPO", valor=tipo, linea=linea))

        # Agregar identificador como hijo
        nodo.agregar_hijo(NodoAST("IDENTIFICADOR", valor=nombre, linea=linea))

        # Consumir '='
        self._consumir("ASIGNACION", f"Se esperaba '=' en la declaración de '{nombre}'")

        # Parsear expresión
        expresion = self._expresion()
        if expresion:
            nodo.agregar_hijo(expresion)

        # Verificar si hay tokens inesperados después de la expresión (probablemente falta operador)
        if not self._token_actual_es("PUNTOYCOMA") and self.token_actual is not None:
            if (
                self._token_actual_es("NUMERO_ENTERO")
                or self._token_actual_es("NUMERO_DECIMAL")
                or self._token_actual_es("IDENTIFICADOR")
            ):
                self._agregar_error(
                    f"Error en la expresión de la variable '{nombre}': falta operador",
                    self._linea_actual(),
                    f"Se encontró '{self.token_actual[1]}' sin operador previo. Verifique que los operadores (+, -, *, /, %) estén presentes",
                )
                return nodo

        # Guardar línea del último token procesado (para reportar error correctamente)
        linea_ultimo_token = self._linea_actual()
        # Si el token actual no es un punto y coma, significa que el error está en la línea anterior
        if not self._token_actual_es("PUNTOYCOMA"):
            # Usar la línea del token anterior (donde debería estar el punto y coma)
            if self.posicion > 0:
                linea_ultimo_token = self.tokens[self.posicion - 1][2]

        # Consumir ';'
        if not self._consumir(
            "PUNTOYCOMA",
            f"Se esperaba ';' al final de la declaración de la variable '{nombre}'",
        ):
            # Si falla, reportar en la línea correcta
            if self.errores and self.errores[-1]["linea"] != linea_ultimo_token:
                self.errores[-1]["linea"] = linea_ultimo_token

        return nodo

    def _asignacion(self):
        """
        Maneja asignación a variable existente.
        Regla: IDENTIFICADOR '=' EXPRESION ';'

        Returns:
            NodoAST: Nodo de asignación o None si hay error
        """
        if not self._token_actual_es("IDENTIFICADOR"):
            return None

        nombre = self.token_actual[1]
        linea = self.token_actual[2]
        self._avanzar()

        # Crear nodo de asignación
        nodo = NodoAST("ASIGNACION", valor=nombre, linea=linea)

        # Consumir '='
        if not self._consumir("ASIGNACION", f"Se esperaba '=' después de '{nombre}'"):
            return None

        # Parsear expresión
        expresion = self._expresion()
        if expresion:
            nodo.agregar_hijo(expresion)

        # Guardar línea del último token procesado (para reportar error correctamente)
        linea_ultimo_token = self._linea_actual()
        # Si el token actual no es un punto y coma, significa que el error está en la línea anterior
        if not self._token_actual_es("PUNTOYCOMA"):
            # Usar la línea del token anterior (donde debería estar el punto y coma)
            if self.posicion > 0:
                linea_ultimo_token = self.tokens[self.posicion - 1][2]

        # Consumir ';'
        if not self._consumir(
            "PUNTOYCOMA",
            f"Se esperaba ';' al final de la asignación a '{nombre}'",
        ):
            # Si falla, reportar en la línea correcta
            if self.errores and self.errores[-1]["linea"] != linea_ultimo_token:
                self.errores[-1]["linea"] = linea_ultimo_token

        return nodo

    def _declaracion_funcion_continuar(self, tipo_retorno, nombre, linea):
        """
        Continúa el análisis de una declaración de función.
        Regla: TIPO IDENTIFICADOR '(' PARAMETROS ')' BLOQUE

        Args:
            tipo_retorno (str): Tipo de retorno de la función
            nombre (str): Nombre de la función
            linea (int): Número de línea

        Returns:
            NodoAST: Nodo de declaración de función
        """
        nodo = NodoAST("DECLARACION_FUNCION", valor=nombre, linea=linea)

        # Agregar tipo de retorno
        nodo.agregar_hijo(NodoAST("TIPO_RETORNO", valor=tipo_retorno, linea=linea))

        # Consumir '('
        self._consumir("PARENTESIS_IZQ", f"Se esperaba '(' en la función '{nombre}'")

        # Parsear parámetros
        parametros = self._parametros()
        if parametros:
            nodo.agregar_hijo(parametros)

        # NOTA: La validación de mínimo 2 parámetros se hace en análisis semántico,
        # no en sintáctico, ya que es una regla de significado, no de estructura.

        # Consumir ')'
        self._consumir("PARENTESIS_DER", f"Se esperaba ')' en la función '{nombre}'")

        # Parsear bloque
        bloque = self._bloque()
        if bloque:
            nodo.agregar_hijo(bloque)

        return nodo

    def _parametros(self):
        """
        Regla: PARAMETROS → TIPO IDENTIFICADOR (',' TIPO IDENTIFICADOR)*

        Parsea la lista de parámetros de una función.

        Returns:
            NodoAST: Nodo con la lista de parámetros
        """
        nodo_parametros = NodoAST("PARAMETROS", linea=self._linea_actual())

        # Si el siguiente token es ')', no hay parámetros
        if self._token_actual_es("PARENTESIS_DER"):
            return nodo_parametros

        # Parsear primer parámetro
        parametro = self._parametro()
        if parametro:
            nodo_parametros.agregar_hijo(parametro)

        # Parsear parámetros adicionales
        while self._token_actual_es("COMA"):
            self._consumir("COMA")
            parametro = self._parametro()
            if parametro:
                nodo_parametros.agregar_hijo(parametro)
            else:
                break

        return nodo_parametros

    def _parametro(self):
        """
        Parsea un parámetro individual: TIPO IDENTIFICADOR

        Returns:
            NodoAST: Nodo del parámetro
        """
        linea = self._linea_actual()

        # Verificar tipo
        if not self._token_actual_es("PALABRA_RESERVADA"):
            self._agregar_error(
                "Se esperaba un tipo de dato en el parámetro", self._linea_actual()
            )
            return None

        tipo = self.token_actual[1]
        if tipo not in self.TIPOS_VALIDOS:
            self._agregar_error(
                f"Tipo de dato inválido en parámetro: '{tipo}'", self._linea_actual()
            )
            return None

        self._avanzar()

        # Verificar identificador
        if not self._token_actual_es("IDENTIFICADOR"):
            self._agregar_error(
                "Se esperaba un identificador para el parámetro", self._linea_actual()
            )
            return None

        nombre = self.token_actual[1]
        self._avanzar()

        nodo_parametro = NodoAST("PARAMETRO", linea=linea)
        nodo_parametro.agregar_hijo(NodoAST("TIPO", valor=tipo, linea=linea))
        nodo_parametro.agregar_hijo(NodoAST("IDENTIFICADOR", valor=nombre, linea=linea))

        return nodo_parametro

    def _estructura_control(self):
        """
        Regla: ESTRUCTURA_CONTROL → ESTRUCTURA_SI
                                   | ESTRUCTURA_MIENTRAS
                                   | ESTRUCTURA_HACER

        Determina el tipo de estructura de control y delega.

        Returns:
            NodoAST: Nodo de la estructura de control
        """
        if self._valor_actual_es("si"):
            return self._estructura_si()
        elif self._valor_actual_es("mientras"):
            return self._estructura_mientras()
        elif self._valor_actual_es("hacer"):
            return self._estructura_hacer()
        else:
            self._agregar_error(
                "Estructura de control no reconocida", self._linea_actual()
            )
            return None

    def _estructura_si(self):
        """
        Regla: ESTRUCTURA_SI → 'si' '(' CONDICION ')' BLOQUE ('sino' BLOQUE)?

        Parsea una estructura si-sino.

        Returns:
            NodoAST: Nodo de la estructura si
        """
        linea = self._linea_actual()
        nodo = NodoAST("ESTRUCTURA_SI", linea=linea)

        # Consumir 'si'
        self._consumir("PALABRA_RESERVADA")

        # Consumir '('
        self._consumir("PARENTESIS_IZQ", "Se esperaba '(' después de 'si'")

        # Parsear condición
        condicion = self._condicion()
        if condicion:
            nodo.agregar_hijo(condicion)

        # Si hay errores en la condición, detener aquí para evitar errores en cascada
        if self.errores:
            return nodo

        # Consumir ')'
        self._consumir("PARENTESIS_DER", "Se esperaba ')' después de la condición")

        # Parsear bloque 'si'
        bloque_si = self._bloque()
        if bloque_si:
            nodo.agregar_hijo(bloque_si)

        # Verificar si hay 'sino'
        if self._token_actual_es("PALABRA_RESERVADA") and self._valor_actual_es("sino"):
            self._consumir("PALABRA_RESERVADA")

            # Parsear bloque 'sino'
            bloque_sino = self._bloque()
            if bloque_sino:
                bloque_sino.tipo = "BLOQUE_SINO"  # Marcar como bloque sino
                nodo.agregar_hijo(bloque_sino)

        return nodo

    def _estructura_mientras(self):
        """
        Regla: ESTRUCTURA_MIENTRAS → 'mientras' '(' CONDICION ')' BLOQUE

        Parsea una estructura mientras.

        Returns:
            NodoAST: Nodo de la estructura mientras
        """
        linea = self._linea_actual()
        nodo = NodoAST("ESTRUCTURA_MIENTRAS", linea=linea)

        # Consumir 'mientras'
        self._consumir("PALABRA_RESERVADA")

        # Consumir '('
        self._consumir("PARENTESIS_IZQ", "Se esperaba '(' después de 'mientras'")

        # Parsear condición
        condicion = self._condicion()
        if condicion:
            nodo.agregar_hijo(condicion)

        # Consumir ')'
        self._consumir("PARENTESIS_DER", "Se esperaba ')' después de la condición")

        # Parsear bloque
        bloque = self._bloque()
        if bloque:
            nodo.agregar_hijo(bloque)

        return nodo

    def _estructura_hacer(self):
        """
        Regla: ESTRUCTURA_HACER → 'hacer' BLOQUE 'mientras' '(' CONDICION ')'

        Parsea una estructura hacer-mientras (do-while).

        Returns:
            NodoAST: Nodo de la estructura hacer
        """
        linea = self._linea_actual()
        nodo = NodoAST("ESTRUCTURA_HACER", linea=linea)

        # Consumir 'hacer'
        self._consumir("PALABRA_RESERVADA")

        # Parsear bloque
        bloque = self._bloque()
        if bloque:
            nodo.agregar_hijo(bloque)

        # Capturar línea de la llave de cierre del bloque (último token procesado)
        linea_cierre_bloque = (
            self.tokens[self.posicion - 1][2] if self.posicion > 0 else linea
        )

        # Verificar y consumir 'mientras'
        if not self._token_actual_es("PALABRA_RESERVADA") or not self._valor_actual_es(
            "mientras"
        ):
            self._agregar_error(
                "Se esperaba 'mientras' después del bloque de la estructura hacer",
                linea_cierre_bloque,
                "La sintaxis correcta es: hacer { ... } mientras (condicion)",
            )
            return nodo

        self._consumir("PALABRA_RESERVADA")  # Consumir 'mientras'

        # Consumir '('
        self._consumir("PARENTESIS_IZQ", "Se esperaba '(' después de 'mientras'")

        # Parsear condición
        condicion = self._condicion()
        if condicion:
            nodo.agregar_hijo(condicion)

        # Consumir ')'
        self._consumir("PARENTESIS_DER", "Se esperaba ')' después de la condición")

        return nodo

    def _bloque(self):
        """
        Regla: BLOQUE → '{' DECLARACION* '}'

        Parsea un bloque de código entre llaves.

        Returns:
            NodoAST: Nodo del bloque
        """
        linea_inicio = self._linea_actual()
        nodo = NodoAST("BLOQUE", linea=linea_inicio)

        # Consumir '{'
        self._consumir("LLAVE_IZQ", "Se esperaba '{' al inicio del bloque")

        # Parsear declaraciones hasta encontrar '}'
        while not self._token_actual_es("LLAVE_DER") and self.token_actual is not None:
            declaracion = self._declaracion()
            if declaracion:
                nodo.agregar_hijo(declaracion)

            # Si hay errores, detener
            if self.errores:
                break

        # SIEMPRE verificar la llave de cierre (incluso si hay errores previos)
        # Si falta la llave, es probable que sea la causa raíz del problema
        if not self._token_actual_es("LLAVE_DER"):
            # Limpiar errores anteriores si falta la llave (es la causa raíz)
            if self.errores:
                # Si ya hay errores y falta la llave, el problema es la llave faltante
                self.errores = []

            # Reportar error en la línea donde se ABRIÓ el bloque
            self._agregar_error(
                "Se esperaba '}' al final del bloque",
                linea_inicio,
                f"El bloque se abrió en la línea {linea_inicio} pero no se cerró correctamente",
            )
        else:
            self._consumir("LLAVE_DER", "Se esperaba '}' al final del bloque")

        return nodo

    def _condicion(self):
        """
        Regla: CONDICION → EXPRESION COMPARADOR EXPRESION

        Parsea una condición (comparación entre dos expresiones).

        Returns:
            NodoAST: Nodo de la condición
        """
        linea = self._linea_actual()
        nodo = NodoAST("CONDICION", linea=linea)

        # Parsear expresión izquierda
        expr_izq = self._expresion()
        if expr_izq:
            nodo.agregar_hijo(expr_izq)

        # Verificar comparador
        comparador = None
        if self._token_actual_es("COMPARACION"):
            comparador = self.token_actual[1]
            self._consumir("COMPARACION")
        elif self._token_actual_es("MENORQUE"):
            comparador = self.token_actual[1]
            self._consumir("MENORQUE")
        elif self._token_actual_es("MAYORQUE"):
            comparador = self.token_actual[1]
            self._consumir("MAYORQUE")
        else:
            self._agregar_error(
                "Se esperaba un comparador (==, !=, <, >, <=, >=)", self._linea_actual()
            )
            return nodo

        # Verificar si hay un '=' adicional después del comparador (ej: ===)
        if self._token_actual_es("ASIGNACION"):
            self._agregar_error(
                f"Comparador inválido: '{comparador}=' no es válido",
                self._linea_actual(),
                "Los comparadores válidos son: ==, !=, <, >, <=, >=. No use tres signos '=' consecutivos",
            )
            return nodo

        # Agregar comparador como hijo
        nodo.agregar_hijo(NodoAST("COMPARADOR", valor=comparador, linea=linea))

        # Parsear expresión derecha
        expr_der = self._expresion()
        if expr_der:
            nodo.agregar_hijo(expr_der)

        return nodo

    def _expresion(self):
        """
        Regla: EXPRESION → TERMINO (('+' | '-') TERMINO)*

        Parsea una expresión aritmética con suma y resta.

        Returns:
            NodoAST: Nodo de la expresión
        """
        linea = self._linea_actual()

        # Parsear primer término
        nodo = self._termino()

        # Parsear operadores + o - y términos adicionales
        while self._token_actual_es("OPERADOR") and self.token_actual[1] in ["+", "-"]:
            operador = self.token_actual[1]
            self._consumir("OPERADOR")

            termino_der = self._termino()
            if termino_der:
                # Crear nodo de operación binaria
                nodo_operacion = NodoAST(
                    "OPERACION_BINARIA", valor=operador, linea=linea
                )
                nodo_operacion.agregar_hijo(nodo)
                nodo_operacion.agregar_hijo(termino_der)
                nodo = nodo_operacion

        return nodo

    def _termino(self):
        """
        Regla: TERMINO → FACTOR (('*' | '/' | '%') FACTOR)*

        Parsea un término aritmético con multiplicación, división y módulo.

        Returns:
            NodoAST: Nodo del término
        """
        linea = self._linea_actual()

        # Parsear primer factor
        nodo = self._factor()

        # Parsear operadores *, / o % y factores adicionales
        while self._token_actual_es("OPERADOR") and self.token_actual[1] in [
            "*",
            "/",
            "%",
        ]:
            operador = self.token_actual[1]
            self._consumir("OPERADOR")

            factor_der = self._factor()
            if factor_der:
                # Crear nodo de operación binaria
                nodo_operacion = NodoAST(
                    "OPERACION_BINARIA", valor=operador, linea=linea
                )
                nodo_operacion.agregar_hijo(nodo)
                nodo_operacion.agregar_hijo(factor_der)
                nodo = nodo_operacion

        return nodo

    def _factor(self):
        """
        Regla: FACTOR → NUMERO_ENTERO
                      | NUMERO_DECIMAL
                      | IDENTIFICADOR
                      | CADENA
                      | 'verdadero'
                      | 'falso'
                      | '(' EXPRESION ')'

        Parsea un factor (elemento básico de una expresión).

        Returns:
            NodoAST: Nodo del factor
        """
        linea = self._linea_actual()

        # Número entero
        if self._token_actual_es("NUMERO_ENTERO"):
            valor = self.token_actual[1]
            self._consumir("NUMERO_ENTERO")
            return NodoAST("NUMERO_ENTERO", valor=valor, linea=linea)

        # Número decimal
        elif self._token_actual_es("NUMERO_DECIMAL"):
            valor = self.token_actual[1]
            self._consumir("NUMERO_DECIMAL")
            return NodoAST("NUMERO_DECIMAL", valor=valor, linea=linea)

        # Identificador (variable)
        elif self._token_actual_es("IDENTIFICADOR"):
            valor = self.token_actual[1]
            self._consumir("IDENTIFICADOR")
            return NodoAST("IDENTIFICADOR", valor=valor, linea=linea)

        # Cadena
        elif self._token_actual_es("CADENA_SIMPLE") or self._token_actual_es(
            "CADENA_DOBLE"
        ):
            tipo_cadena = self.token_actual[0]
            valor = self.token_actual[1]
            self._consumir(tipo_cadena)
            return NodoAST("CADENA", valor=valor, linea=linea)

        # Booleanos: verdadero o falso
        elif self._token_actual_es("PALABRA_RESERVADA") and self.token_actual[1] in [
            "verdadero",
            "falso",
        ]:
            valor = self.token_actual[1]
            self._consumir("PALABRA_RESERVADA")
            return NodoAST("BOOLEANO", valor=valor, linea=linea)

        # Expresión entre paréntesis
        elif self._token_actual_es("PARENTESIS_IZQ"):
            self._consumir("PARENTESIS_IZQ")
            expresion = self._expresion()
            self._consumir("PARENTESIS_DER", "Se esperaba ')' después de la expresión")
            return expresion

        else:
            self._agregar_error(
                "Factor inesperado en expresión",
                self._linea_actual(),
                f"Token: '{self.token_actual[1] if self.token_actual else 'EOF'}'",
            )
            return None
