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
        # Operadores y símbolos
        ("ASIGNACION", r"="),
        ("OPERADOR", r"[+\-*/%]"),
        ("COMPARACION", r"==|!=|<=|>="),
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
        linea_num = 1

        for mo in re.finditer(self.regex_maestra, codigo):
            tipo_token = mo.lastgroup
            valor = mo.group()

            if tipo_token == "NUEVALINEA":
                linea_num += 1
                continue
            elif tipo_token == "ESPACIO":
                continue
            elif tipo_token in ["COMENTARIO_LINEA", "COMENTARIO_BLOQUE"]:
                # Los comentarios se ignoran pero pueden contener saltos de línea
                linea_num += valor.count("\n")
                continue
            elif tipo_token == "ERROR":
                tokens.append(("ERROR", f"Token inesperado '{valor}'", linea_num))
            else:
                # Es un identificador? Verificar si es una palabra reservada
                if tipo_token == "IDENTIFICADOR" and valor in self.PALABRAS_RESERVADAS:
                    tipo_token = "PALABRA_RESERVADA"

                tokens.append((tipo_token, valor, linea_num))

        return tokens

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
