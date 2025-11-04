import re


class AnalizadorLexico:
    """
    Clase que implementa un analizador léxico para un lenguaje de programación simple.
    """

    # Definición de los tokens según el documento del proyecto
    TOKEN_ESPECIFICACION = [
        # Comentarios (deben ir primero para tener prioridad)
        ("COMENTARIO_LINEA", r"//.*"),
        ("COMENTARIO_BLOQUE", r"/\*[\s\S]*?\*/"),
        # Números decimales
        ("NUMERO_DECIMAL", r"\d+\.\d+"),
        # Números enteros
        ("NUMERO_ENTERO", r"\d+"),
        # Literales de cadena
        ("CADENA_SIMPLE", r"'[^'\\]*(?:\\.[^'\\]*)*'"),
        ("CADENA_DOBLE", r'"[^"\\]*(?:\\.[^"\\]*)*"'),
        # Identificadores (soporta mayúsculas, minúsculas y guiones bajos)
        ("IDENTIFICADOR", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        # Operadores y símbolos (comparadores ANTES de asignación para prioridad)
        ("COMPARACION", r"==|!=|<=|>="),
        ("ASIGNACION", r"="),
        ("OPERADOR", r"[+\-*/%]"),
        ("MENORQUE", r"<"),
        ("MAYORQUE", r">"),
        # Delimitadores
        ("PARENTESIS_IZQ", r"\("),
        ("PARENTESIS_DER", r"\)"),
        ("LLAVE_IZQ", r"\{"),
        ("LLAVE_DER", r"\}"),
        ("PUNTOYCOMA", r";"),
        ("COMA", r","),
        ("PUNTO", r"\."),
        # Espacios en blanco
        ("NUEVALINEA", r"\n"),
        ("ESPACIO", r"[ \t]+"),
        # Token de error para caracteres no reconocidos
        ("ERROR", r"."),
    ]

    # Palabras reservadas
    PALABRAS_RESERVADAS = {
        "entero",
        "decimal",
        "booleano",
        "cadena",
        "si",
        "sino",
        "mientras",
        "hacer",
        "verdadero",
        "falso",
    }

    def __init__(self):
        """
        Inicializa el analizador léxico.
        """
        # Compilar la expresión regular maestra una sola vez para mejor rendimiento
        self.regex_maestra = "|".join(
            "(?P<%s>%s)" % par for par in self.TOKEN_ESPECIFICACION
        )

    def analizar(self, codigo):
        """
        Analizador Léxico.
        Toma un string de código y lo divide en una lista de tokens.

        Args:
            codigo (str): El código fuente a analizar

        Returns:
            list: Lista de tuplas (tipo_token, valor, numero_linea)
        """
        tokens = []

        # PASO 1: Detectar comentarios de bloque sin cerrar
        error_comentario = self._detectar_comentario_sin_cerrar(codigo)
        if error_comentario:
            return [error_comentario]

        # PASO 2: Detectar cadenas sin cerrar
        error_cadena = self._detectar_cadena_sin_cerrar(codigo)
        if error_cadena:
            return [error_cadena]

        # PASO 3: Análisis léxico normal
        for mo in re.finditer(self.regex_maestra, codigo):
            tipo_token = mo.lastgroup
            valor = mo.group()

            # Calcular número de línea basado en la posición del match
            linea_num = codigo[: mo.start()].count("\n") + 1

            if tipo_token == "NUEVALINEA":
                continue
            elif tipo_token == "ESPACIO":
                continue
            elif tipo_token in ["COMENTARIO_LINEA", "COMENTARIO_BLOQUE"]:
                # Los comentarios se ignoran
                continue
            elif tipo_token == "ERROR":
                tokens.append(("ERROR", f"Token inesperado '{valor}'", linea_num))
            else:
                # Es un identificador? Verificar si es una palabra reservada
                if tipo_token == "IDENTIFICADOR" and valor in self.PALABRAS_RESERVADAS:
                    tipo_token = "PALABRA_RESERVADA"

                tokens.append((tipo_token, valor, linea_num))

        return tokens

    def _detectar_comentario_sin_cerrar(self, codigo):
        """
        Detecta si hay un comentario de bloque sin cerrar.

        Args:
            codigo (str): El código fuente a analizar

        Returns:
            tuple o None: Token de error si se detecta comentario sin cerrar, None en caso contrario
        """
        # Buscar todos los comentarios de bloque abiertos y cerrados
        patron_apertura = r"/\*"
        patron_cierre = r"\*/"

        aperturas = [(m.start(), m.end()) for m in re.finditer(patron_apertura, codigo)]
        cierres = [(m.start(), m.end()) for m in re.finditer(patron_cierre, codigo)]

        if not aperturas:
            return None  # No hay comentarios de bloque

        # Emparejar aperturas con cierres
        i_cierre = 0
        for apertura_inicio, apertura_fin in aperturas:
            # Buscar el primer cierre después de esta apertura
            encontrado_cierre = False
            while i_cierre < len(cierres):
                cierre_inicio, _ = cierres[i_cierre]
                if cierre_inicio > apertura_inicio:
                    # Encontramos el cierre correspondiente
                    encontrado_cierre = True
                    i_cierre += 1
                    break
                i_cierre += 1

            # Si esta apertura no tiene cierre, es un error
            if not encontrado_cierre:
                linea_num = codigo[:apertura_inicio].count("\n") + 1
                return (
                    "ERROR",
                    "Comentario de bloque sin cerrar: se esperaba '*/' para cerrar el comentario",
                    linea_num,
                )

        return None

    def _detectar_cadena_sin_cerrar(self, codigo):
        """
        Detecta si hay una cadena sin cerrar.

        Args:
            codigo (str): El código fuente a analizar

        Returns:
            tuple o None: Token de error si se detecta cadena sin cerrar, None en caso contrario
        """
        # Eliminar comentarios primero para no detectar comillas dentro de comentarios
        codigo_sin_comentarios = re.sub(r"//.*", "", codigo)  # Comentarios de línea
        codigo_sin_comentarios = re.sub(
            r"/\*[\s\S]*?\*/", "", codigo_sin_comentarios
        )  # Comentarios de bloque

        # Buscar cadenas con comillas simples o dobles
        i = 0
        while i < len(codigo_sin_comentarios):
            char = codigo_sin_comentarios[i]

            # Encontramos el inicio de una cadena
            if char in ('"', "'"):
                comilla_tipo = char
                i += 1
                cadena_cerrada = False

                # Buscar el cierre de la cadena
                while i < len(codigo_sin_comentarios):
                    char_actual = codigo_sin_comentarios[i]

                    # Si encontramos la comilla de cierre (y no está escapada)
                    if char_actual == comilla_tipo:
                        # Verificar si está escapada
                        if i > 0 and codigo_sin_comentarios[i - 1] == "\\":
                            # Está escapada, continuar
                            i += 1
                            continue
                        else:
                            # Cadena cerrada correctamente
                            cadena_cerrada = True
                            break

                    # Si encontramos un salto de línea antes de cerrar, es un error
                    if char_actual == "\n":
                        linea_num = codigo_sin_comentarios[:i].count("\n") + 1
                        return (
                            "ERROR",
                            f"Cadena sin cerrar: se esperaba {comilla_tipo} para cerrar la cadena",
                            linea_num,
                        )

                    i += 1

                # Si llegamos al final sin cerrar la cadena
                if not cadena_cerrada:
                    linea_num = codigo_sin_comentarios[:i].count("\n") + 1
                    return (
                        "ERROR",
                        f"Cadena sin cerrar: se esperaba {comilla_tipo} para cerrar la cadena",
                        linea_num,
                    )

            i += 1

        return None

    def obtener_errores(self, tokens):
        """
        Filtra solo los tokens de error de la lista de tokens.

        Args:
            tokens (list): Lista de tokens

        Returns:
            list: Lista de tokens de error
        """
        return [t for t in tokens if t[0] == "ERROR"]

    def generar_resumen_tokens(self, tokens):
        """
        Genera un resumen de los tokens agrupados por tipo.

        Args:
            tokens (list): Lista de tokens

        Returns:
            dict: Diccionario con el conteo de tokens por tipo y valor
        """
        conteo_tokens = {}
        for tipo, valor, _ in tokens:
            # Agrupar todos los operadores en una sola categoría para el resumen
            if tipo in [
                "ASIGNACION",
                "OPERADOR",
                "COMPARACION",
                "MENORQUE",
                "MAYORQUE",
            ]:
                tipo_resumen = "Operador"
            elif tipo in [
                "PARENTESIS_IZQ",
                "PARENTESIS_DER",
                "LLAVE_IZQ",
                "LLAVE_DER",
                "PUNTOYCOMA",
                "COMA",
                "PUNTO",
            ]:
                tipo_resumen = "Signo"
            elif tipo == "PALABRA_RESERVADA":
                tipo_resumen = "Palabra Reservada"
            elif tipo == "IDENTIFICADOR":
                tipo_resumen = "Identificador"
            elif tipo == "NUMERO_ENTERO":
                tipo_resumen = "Numero Entero"
            elif tipo == "NUMERO_DECIMAL":
                tipo_resumen = "Numero Decimal"
            elif tipo in ["CADENA_SIMPLE", "CADENA_DOBLE"]:
                tipo_resumen = "Cadena"
            else:
                tipo_resumen = tipo

            # Contar por valor de token
            if (valor, tipo_resumen) in conteo_tokens:
                conteo_tokens[(valor, tipo_resumen)] += 1
            else:
                conteo_tokens[(valor, tipo_resumen)] = 1

        return conteo_tokens
