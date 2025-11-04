"""
Analizador Semántico para el lenguaje de programación simple.
Verifica la coherencia semántica del código: tipos, declaraciones, uso de variables, etc.
"""


class AnalizadorSemantico:
    """
    Analizador semántico que verifica reglas semánticas del lenguaje.
    Mantiene una tabla de símbolos y verifica compatibilidad de tipos.
    """

    # Matriz de compatibilidad de tipos para operaciones
    COMPATIBILIDAD_TIPOS = {
        ("entero", "entero"): {
            "+": "entero",
            "-": "entero",
            "*": "entero",
            "/": "entero",
            "%": "entero",
        },
        ("decimal", "decimal"): {
            "+": "decimal",
            "-": "decimal",
            "*": "decimal",
            "/": "decimal",
        },
        ("entero", "decimal"): {
            "+": "decimal",
            "-": "decimal",
            "*": "decimal",
            "/": "decimal",
        },
        ("decimal", "entero"): {
            "+": "decimal",
            "-": "decimal",
            "*": "decimal",
            "/": "decimal",
        },
        ("cadena", "cadena"): {"+": "cadena"},  # Concatenación
        ("booleano", "booleano"): {},  # Solo comparaciones, no operaciones aritméticas
    }

    # Tipos de datos válidos
    TIPOS_VALIDOS = {"entero", "decimal", "booleano", "cadena"}

    def __init__(self, ast):
        """
        Inicializa el analizador semántico.

        Args:
            ast: Árbol de sintaxis abstracta del parser sintáctico
        """
        self.ast = ast
        self.tabla_simbolos = {}  # {ambito:nombre: {tipo, categoria, ambito, linea}}
        self.errores = []
        self.ambito_actual = "global"
        self.pila_ambitos = ["global"]  # Pila para manejar ámbitos anidados
        self.funciones = {}  # {nombre: {tipo_retorno, parametros}}

    def analizar(self):
        """
        Realiza el análisis semántico completo del AST.

        Returns:
            list: Lista de errores semánticos encontrados
        """
        self.errores = []
        if self.ast:
            self._recorrer_ast(self.ast)
        return self.errores

    def _recorrer_ast(self, nodo):
        """
        Recorre el AST aplicando las reglas semánticas usando el patrón Visitor.

        Args:
            nodo: Nodo actual del AST a procesar
        """
        if nodo is None:
            return

        # Procesar según el tipo de nodo
        if nodo.tipo == "DECLARACION_VARIABLE":
            self._verificar_declaracion_variable(nodo)
        elif nodo.tipo == "ASIGNACION":
            self._verificar_asignacion(nodo)
        elif nodo.tipo == "DECLARACION_FUNCION":
            # Las funciones manejan sus hijos (parámetros y bloque) internamente
            self._verificar_declaracion_funcion(nodo)
            return  # No procesar hijos automáticamente
        elif nodo.tipo == "IDENTIFICADOR":
            # Solo verificar uso si no está en contexto de declaración
            if self._es_uso_variable(nodo):
                self._verificar_uso_variable(nodo)
        elif nodo.tipo == "OPERACION_BINARIA":
            self._verificar_operacion_binaria(nodo)
        elif nodo.tipo == "CONDICION":
            self._verificar_condicion(nodo)

        # Recorrer hijos recursivamente
        for hijo in nodo.hijos:
            self._recorrer_ast(hijo)

    def _es_uso_variable(self, nodo):
        """
        Determina si un nodo IDENTIFICADOR es un uso de variable
        (no una declaración).

        Args:
            nodo: Nodo a verificar

        Returns:
            bool: True si es uso, False si es declaración
        """
        # Esta es una simplificación. En un compilador real, se haría
        # tracking más sofisticado del contexto
        return True

    def _verificar_declaracion_variable(self, nodo):
        """
        Verifica que una variable sea declarada correctamente.

        Reglas:
        - Variable no debe estar declarada previamente en el mismo ámbito
        - Tipo de dato debe ser válido
        - El valor asignado debe ser compatible con el tipo

        Args:
            nodo: Nodo DECLARACION_VARIABLE del AST
        """
        if len(nodo.hijos) < 3:
            return

        tipo_nodo = nodo.hijos[0]
        nombre_nodo = nodo.hijos[1]
        expresion_nodo = nodo.hijos[2]

        tipo = tipo_nodo.valor
        nombre = nombre_nodo.valor
        linea = nodo.linea

        # Verificar que el tipo sea válido
        if tipo not in self.TIPOS_VALIDOS:
            self._agregar_error(
                f"Tipo de dato inválido: '{tipo}'",
                linea,
                f"Los tipos válidos son: {', '.join(self.TIPOS_VALIDOS)}",
            )
            return

        # Verificar que no esté declarada en el ámbito actual
        clave = f"{self.ambito_actual}:{nombre}"
        if clave in self.tabla_simbolos:
            self._agregar_error(
                f"La variable '{nombre}' ya fue declarada en este ámbito",
                linea,
                f"Primera declaración en línea {self.tabla_simbolos[clave]['linea']}",
            )
            return

        # Inferir tipo de la expresión
        tipo_expresion = self._inferir_tipo_expresion(expresion_nodo)

        # Verificar compatibilidad de tipos
        if tipo_expresion and not self._es_asignacion_compatible(tipo, tipo_expresion):
            self._agregar_error(
                f"Incompatibilidad de tipos en la declaración de '{nombre}'",
                linea,
                f"Se esperaba '{tipo}' pero la expresión es de tipo '{tipo_expresion}'",
            )
            return

        # Agregar a la tabla de símbolos
        self._agregar_simbolo(nombre, tipo, "variable", linea)

    def _verificar_asignacion(self, nodo):
        """
        Verifica que una asignación a variable existente sea correcta.

        Reglas:
        - La variable debe estar declarada previamente
        - El tipo de la expresión debe ser compatible con el tipo de la variable

        Args:
            nodo: Nodo ASIGNACION del AST
        """
        nombre = nodo.valor
        linea = nodo.linea

        # Verificar que la variable exista
        simbolo = self._buscar_simbolo(nombre)
        if simbolo is None:
            self._agregar_error(
                f"Variable '{nombre}' no ha sido declarada",
                linea,
                "Se está intentando asignar a una variable que no existe",
            )
            return

        # Si no hay expresión, no hay más que verificar
        if len(nodo.hijos) == 0:
            return

        expresion_nodo = nodo.hijos[0]

        # Inferir tipo de la expresión
        tipo_expresion = self._inferir_tipo_expresion(expresion_nodo)

        # Verificar compatibilidad de tipos
        tipo_variable = simbolo["tipo"]
        if not self._verificar_compatibilidad_tipos(
            tipo_variable, tipo_expresion, "asignacion"
        ):
            self._agregar_error(
                f"Incompatibilidad de tipos en la asignación a '{nombre}'",
                linea,
                f"La variable es de tipo '{tipo_variable}' pero la expresión es de tipo '{tipo_expresion}'",
            )

    def _verificar_declaracion_funcion(self, nodo):
        """
        Verifica declaración de función.

        Reglas:
        - Función no debe estar declarada previamente
        - Debe tener mínimo 2 parámetros (requisito del proyecto)
        - Los parámetros deben tener nombres únicos
        - El tipo de retorno debe ser válido

        Args:
            nodo: Nodo DECLARACION_FUNCION del AST
        """
        nombre = nodo.valor
        linea = nodo.linea

        if len(nodo.hijos) < 2:
            return

        tipo_retorno_nodo = nodo.hijos[0]
        parametros_nodo = nodo.hijos[1] if len(nodo.hijos) > 1 else None

        tipo_retorno = tipo_retorno_nodo.valor

        # Verificar que el tipo de retorno sea válido
        if tipo_retorno not in self.TIPOS_VALIDOS:
            self._agregar_error(
                f"Tipo de retorno inválido en función '{nombre}': '{tipo_retorno}'",
                linea,
            )

        # Verificar que no esté declarada
        if nombre in self.funciones:
            self._agregar_error(
                f"La función '{nombre}' ya fue declarada",
                linea,
                f"Primera declaración en línea {self.funciones[nombre]['linea']}",
            )
            return

        # Verificar parámetros
        parametros_lista = []
        nombres_parametros = set()

        if parametros_nodo and parametros_nodo.tipo == "PARAMETROS":
            for parametro in parametros_nodo.hijos:
                if parametro.tipo == "PARAMETRO" and len(parametro.hijos) >= 2:
                    tipo_param = parametro.hijos[0].valor
                    nombre_param = parametro.hijos[1].valor

                    # Verificar nombres duplicados
                    if nombre_param in nombres_parametros:
                        self._agregar_error(
                            f"Parámetro duplicado en función '{nombre}': '{nombre_param}'",
                            linea,
                        )
                    else:
                        nombres_parametros.add(nombre_param)
                        parametros_lista.append(
                            {"tipo": tipo_param, "nombre": nombre_param}
                        )

        # REQUISITO: Verificar que tenga mínimo 2 parámetros
        # (Esta verificación ya se hace en el parser, pero la reforzamos aquí)
        if len(parametros_lista) < 2:
            self._agregar_error(
                f"La función '{nombre}' debe tener mínimo 2 parámetros",
                linea,
                f"Se encontraron {len(parametros_lista)} parámetro(s)",
            )

        # Agregar función a la tabla
        self.funciones[nombre] = {
            "tipo_retorno": tipo_retorno,
            "parametros": parametros_lista,
            "linea": linea,
        }

        # Agregar función a tabla de símbolos (en ámbito global)
        self._agregar_simbolo(nombre, tipo_retorno, "funcion", linea)

        # Entrar en el ámbito de la función
        self._entrar_ambito(nombre)

        # Agregar parámetros a la tabla de símbolos (en ámbito local de la función)
        for parametro in parametros_lista:
            self._agregar_simbolo(
                parametro["nombre"], parametro["tipo"], "parametro", linea
            )

        # Procesar el cuerpo de la función (bloque)
        if len(nodo.hijos) >= 3:
            bloque_nodo = nodo.hijos[2]
            if bloque_nodo and bloque_nodo.tipo == "BLOQUE":
                # Recorrer los hijos del bloque (declaraciones dentro de la función)
                for hijo in bloque_nodo.hijos:
                    self._recorrer_ast(hijo)

        # Salir del ámbito de la función
        self._salir_ambito()

    def _verificar_uso_variable(self, nodo):
        """
        Verifica que una variable usada exista.

        Reglas:
        - Variable debe estar declarada antes de usarse

        Args:
            nodo: Nodo IDENTIFICADOR del AST
        """
        nombre = nodo.valor
        linea = nodo.linea

        # Buscar en tabla de símbolos
        simbolo = self._buscar_simbolo(nombre)

        if simbolo is None:
            self._agregar_error(
                f"La variable '{nombre}' no ha sido declarada",
                linea,
                "Debe declarar la variable antes de usarla",
            )

    def _verificar_operacion_binaria(self, nodo):
        """
        Verifica que una operación binaria sea semánticamente correcta.

        Reglas:
        - Operaciones entre tipos compatibles

        Args:
            nodo: Nodo OPERACION_BINARIA del AST
        """
        if len(nodo.hijos) < 2:
            return

        operador = nodo.valor
        operando_izq = nodo.hijos[0]
        operando_der = nodo.hijos[1]

        # Inferir tipos de ambos operandos
        tipo_izq = self._inferir_tipo_expresion(operando_izq)
        tipo_der = self._inferir_tipo_expresion(operando_der)

        if tipo_izq and tipo_der:
            # Verificar compatibilidad
            if not self._verificar_compatibilidad_tipos(tipo_izq, tipo_der, operador):
                self._agregar_error(
                    f"Operación '{operador}' no permitida entre tipos '{tipo_izq}' y '{tipo_der}'",
                    nodo.linea,
                    "Los tipos no son compatibles para esta operación",
                )

    def _verificar_condicion(self, nodo):
        """
        Verifica que una condición sea semánticamente correcta.

        Reglas:
        - Comparaciones entre tipos compatibles

        Args:
            nodo: Nodo CONDICION del AST
        """
        if len(nodo.hijos) < 3:
            return

        expr_izq = nodo.hijos[0]
        expr_der = nodo.hijos[2]

        # Inferir tipos
        tipo_izq = self._inferir_tipo_expresion(expr_izq)
        tipo_der = self._inferir_tipo_expresion(expr_der)

        if tipo_izq and tipo_der:
            # Para comparaciones, los tipos deben ser iguales o compatibles
            if tipo_izq != tipo_der:
                # Permitir comparación entre entero y decimal
                if not (
                    (tipo_izq == "entero" and tipo_der == "decimal")
                    or (tipo_izq == "decimal" and tipo_der == "entero")
                ):
                    self._agregar_error(
                        f"Comparación entre tipos incompatibles: '{tipo_izq}' y '{tipo_der}'",
                        nodo.linea,
                        "Las comparaciones requieren tipos compatibles",
                    )

    def _verificar_compatibilidad_tipos(self, tipo1, tipo2, operacion=None):
        """
        Verifica si dos tipos son compatibles para una operación.

        Args:
            tipo1 (str): Primer tipo
            tipo2 (str): Segundo tipo
            operacion (str): Operación a realizar ('+', '-', '*', '/', '%', 'asignacion')

        Returns:
            bool: True si son compatibles, False en caso contrario
        """
        # Caso especial: asignación
        if operacion == "asignacion":
            # Mismo tipo siempre compatible
            if tipo1 == tipo2:
                return True
            # entero puede asignarse a decimal (conversión implícita)
            if tipo1 == "decimal" and tipo2 == "entero":
                return True
            # Otras conversiones no permitidas
            return False

        # Para operaciones aritméticas, buscar en la matriz de compatibilidad
        clave = (tipo1, tipo2)
        if clave in self.COMPATIBILIDAD_TIPOS:
            if operacion:
                return operacion in self.COMPATIBILIDAD_TIPOS[clave]
            else:
                return True
        return False

    def _inferir_tipo_expresion(self, nodo):
        """
        Infiere el tipo de una expresión.

        Args:
            nodo: Nodo de tipo EXPRESION o similar

        Returns:
            str: Tipo inferido ('entero', 'decimal', 'cadena', 'booleano') o None
        """
        if nodo is None:
            return None

        # Literales
        if nodo.tipo == "NUMERO_ENTERO":
            return "entero"
        elif nodo.tipo == "NUMERO_DECIMAL":
            return "decimal"
        elif nodo.tipo == "CADENA":
            return "cadena"
        elif nodo.tipo == "BOOLEANO":
            return "booleano"

        # Identificador (variable)
        elif nodo.tipo == "IDENTIFICADOR":
            simbolo = self._buscar_simbolo(nodo.valor)
            if simbolo:
                return simbolo["tipo"]
            return None

        # Operación binaria
        elif nodo.tipo == "OPERACION_BINARIA":
            if len(nodo.hijos) >= 2:
                operador = nodo.valor
                tipo_izq = self._inferir_tipo_expresion(nodo.hijos[0])
                tipo_der = self._inferir_tipo_expresion(nodo.hijos[1])

                if tipo_izq and tipo_der:
                    clave = (tipo_izq, tipo_der)
                    if clave in self.COMPATIBILIDAD_TIPOS:
                        ops = self.COMPATIBILIDAD_TIPOS[clave]
                        if operador in ops:
                            return ops[operador]

        # Para otros tipos de nodos, intentar inferir del primer hijo
        elif nodo.hijos:
            return self._inferir_tipo_expresion(nodo.hijos[0])

        return None

    def _es_asignacion_compatible(self, tipo_declarado, tipo_expresion):
        """
        Verifica si una asignación es compatible.

        Args:
            tipo_declarado (str): Tipo declarado de la variable
            tipo_expresion (str): Tipo de la expresión a asignar

        Returns:
            bool: True si la asignación es compatible
        """
        # Tipos iguales siempre son compatibles
        if tipo_declarado == tipo_expresion:
            return True

        # Permitir asignación de entero a decimal (conversión implícita)
        if tipo_declarado == "decimal" and tipo_expresion == "entero":
            return True

        return False

    def _agregar_simbolo(self, nombre, tipo, categoria, linea):
        """
        Agrega un símbolo a la tabla de símbolos.

        Args:
            nombre (str): Nombre del símbolo
            tipo (str): Tipo del símbolo
            categoria (str): Categoría: 'variable', 'funcion', 'parametro'
            linea (int): Línea donde se declaró
        """
        clave = f"{self.ambito_actual}:{nombre}"

        if clave in self.tabla_simbolos:
            # Ya existe, no agregar (el error ya se reportó)
            return

        self.tabla_simbolos[clave] = {
            "tipo": tipo,
            "categoria": categoria,
            "ambito": self.ambito_actual,
            "linea": linea,
        }

    def _buscar_simbolo(self, nombre):
        """
        Busca un símbolo en la tabla de símbolos.
        Busca en la pila de ámbitos desde el más reciente al más antiguo.

        Args:
            nombre (str): Nombre del símbolo a buscar

        Returns:
            dict: Información del símbolo o None si no existe
        """
        # Buscar en la pila de ámbitos desde el más reciente
        for ambito in reversed(self.pila_ambitos):
            clave = f"{ambito}:{nombre}"
            if clave in self.tabla_simbolos:
                return self.tabla_simbolos[clave]

        return None

    def _entrar_ambito(self, nombre_ambito):
        """
        Entra en un nuevo ámbito (por ejemplo, una función).

        Args:
            nombre_ambito (str): Nombre del nuevo ámbito
        """
        self.ambito_actual = nombre_ambito
        self.pila_ambitos.append(nombre_ambito)

    def _salir_ambito(self):
        """
        Sale del ámbito actual y vuelve al anterior.
        """
        if len(self.pila_ambitos) > 1:
            self.pila_ambitos.pop()
            self.ambito_actual = self.pila_ambitos[-1]

    def _agregar_error(self, mensaje, linea, detalle=""):
        """
        Agrega un error a la lista de errores semánticos.

        Args:
            mensaje (str): Mensaje de error
            linea (int): Línea donde ocurrió el error
            detalle (str): Información adicional (opcional)
        """
        self.errores.append(
            {
                "tipo": "SEMÁNTICO",
                "mensaje": mensaje,
                "linea": linea,
                "detalle": detalle,
            }
        )
