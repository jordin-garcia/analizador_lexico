# Plan Detallado de Desarrollo - Analizador Léxico, Sintáctico y Semántico

## 📊 Análisis del Estado Actual

He revisado exhaustivamente el código y los documentos del proyecto. Actualmente tienen:

### ✅ Completado (Proyecto 1 - Fase 1):
- **Analizador Léxico funcional** que reconoce:
  - Palabras reservadas
  - Identificadores
  - Números (enteros y decimales)
  - Operadores y comparadores
  - Delimitadores
  - Cadenas de texto
  - Comentarios
- **Interfaz gráfica** con Tkinter
- **Detección de errores léxicos**
- **Resumen de tokens**

### ❌ Pendiente (Proyecto 2 - Fase 2):
- **Análisis Sintáctico (Parser)**: Verificar estructura correcta del código
- **Análisis Semántico**: Verificar coherencia de tipos y uso de variables
- **Nuevas estructuras a validar**:
  - Declaración de variables con tipos
  - Estructuras de control (si, sino, mientras, hacer)
  - Declaración de funciones con parámetros (mínimo 2)

---

## 🔀 División Equitativa del Trabajo

El trabajo se divide en dos partes iguales para que ambos contribuyan de manera equilibrada.

---

## 🔵 PARTE 1 - JORDIN (50% del trabajo)

### **Tarea Principal**: Implementar el Analizador Sintáctico Completo

#### **1.1 Crear el módulo `src/analizador_sintactico.py`** (archivo nuevo)

Deberás crear una clase que implemente un **Parser Descendente Recursivo** para validar la estructura sintáctica del código.

**Estructuras sintácticas a implementar:**

```
Gramática a validar:

PROGRAMA → DECLARACION*

DECLARACION → DECLARACION_VARIABLE
            | DECLARACION_FUNCION
            | ESTRUCTURA_CONTROL

DECLARACION_VARIABLE → TIPO IDENTIFICADOR '=' EXPRESION ';'

TIPO → 'entero' | 'decimal' | 'booleano' | 'cadena'

DECLARACION_FUNCION → TIPO IDENTIFICADOR '(' PARAMETROS ')' BLOQUE

PARAMETROS → TIPO IDENTIFICADOR (',' TIPO IDENTIFICADOR)*

ESTRUCTURA_CONTROL → ESTRUCTURA_SI
                   | ESTRUCTURA_MIENTRAS
                   | ESTRUCTURA_HACER

ESTRUCTURA_SI → 'si' '(' CONDICION ')' BLOQUE ('sino' BLOQUE)?

ESTRUCTURA_MIENTRAS → 'mientras' '(' CONDICION ')' BLOQUE

ESTRUCTURA_HACER → 'hacer' BLOQUE

BLOQUE → '{' DECLARACION* '}'

CONDICION → EXPRESION COMPARADOR EXPRESION

COMPARADOR → '==' | '!=' | '<' | '>' | '<=' | '>='

EXPRESION → TERMINO (('+' | '-') TERMINO)*

TERMINO → FACTOR (('*' | '/' | '%') FACTOR)*

FACTOR → NUMERO_ENTERO
       | NUMERO_DECIMAL
       | IDENTIFICADOR
       | CADENA
       | 'verdadero'
       | 'falso'
       | '(' EXPRESION ')'
```

**Estructura del archivo `analizador_sintactico.py`:**

```python
class AnalizadorSintactico:
    def __init__(self, tokens):
        """
        Inicializa el analizador sintáctico.
        
        Args:
            tokens: Lista de tokens del analizador léxico
        """
        self.tokens = tokens
        self.posicion = 0
        self.errores = []
        self.token_actual = None
        
    def analizar(self):
        """
        Inicia el análisis sintáctico del programa completo.
        
        Returns:
            tuple: (arbol_sintactico, errores)
        """
        pass
    
    def _avanzar(self):
        """Avanza al siguiente token"""
        pass
    
    def _token_actual_es(self, tipo_esperado):
        """Verifica si el token actual es del tipo esperado"""
        pass
    
    def _consumir(self, tipo_esperado):
        """Consume un token del tipo esperado o genera error"""
        pass
    
    # Métodos para cada regla de la gramática
    def _programa(self):
        pass
    
    def _declaracion(self):
        pass
    
    def _declaracion_variable(self):
        pass
    
    def _declaracion_funcion(self):
        pass
    
    def _estructura_control(self):
        pass
    
    def _estructura_si(self):
        pass
    
    def _estructura_mientras(self):
        pass
    
    def _estructura_hacer(self):
        pass
    
    def _bloque(self):
        pass
    
    def _condicion(self):
        pass
    
    def _expresion(self):
        pass
    
    def _termino(self):
        pass
    
    def _factor(self):
        pass
```

#### **1.2 Implementar detección de errores sintácticos específicos**

Debes detectar y reportar errores como:
- ✗ Falta de punto y coma
- ✗ Paréntesis, llaves o corchetes sin cerrar
- ✗ Función con menos de 2 parámetros
- ✗ Tipo de dato no declarado en variables
- ✗ Estructura `si` sin condición
- ✗ Operadores mal ubicados
- ✗ Estructura incorrecta de declaraciones
- ✗ Tokens inesperados

**Formato de error sugerido:**

```python
{
    'tipo': 'SINTÁCTICO',
    'mensaje': 'Se esperaba ";" después de la declaración',
    'linea': 5,
    'detalle': 'Encontrado: "entero" en lugar de ";"'
}
```

#### **1.3 Crear estructura de Árbol de Sintaxis Abstracta (AST)**

Crear una representación en forma de diccionario/objeto del código parseado:

```python
class NodoAST:
    """Representa un nodo en el árbol de sintaxis abstracta"""
    def __init__(self, tipo, valor=None, hijos=None, linea=None):
        self.tipo = tipo           # Tipo de nodo: 'PROGRAMA', 'DECLARACION_VAR', etc.
        self.valor = valor         # Valor asociado (nombre de variable, operador, etc.)
        self.hijos = hijos or []   # Lista de nodos hijos
        self.linea = linea         # Número de línea (para errores)
    
    def agregar_hijo(self, nodo):
        """Agrega un nodo hijo al nodo actual"""
        self.hijos.append(nodo)
    
    def __repr__(self):
        return f"NodoAST(tipo={self.tipo}, valor={self.valor})"
```

**Ejemplo de AST para `entero x = 10;`:**

```python
NodoAST(
    tipo='DECLARACION_VARIABLE',
    hijos=[
        NodoAST(tipo='TIPO', valor='entero'),
        NodoAST(tipo='IDENTIFICADOR', valor='x'),
        NodoAST(tipo='EXPRESION', 
            hijos=[NodoAST(tipo='NUMERO_ENTERO', valor='10')]
        )
    ]
)
```

#### **1.4 Crear archivo de pruebas `tests/casos_sintacticos.txt`**

Crea casos de prueba que incluyan:
- ✅ Código sintácticamente correcto
- ❌ Errores sintácticos diversos

**Ejemplo de contenido:**

```
// ========================================
// CASOS SINTÁCTICOS - ARCHIVO DE PRUEBA
// ========================================

// CASO 1: Correcto - Declaración simple
entero x = 10;

// CASO 2: Error - falta punto y coma
entero y = 20

// CASO 3: Correcto - Declaración con operación
decimal resultado = 3.14 * 2.0;

// CASO 4: Error - paréntesis sin cerrar
si (x > 5 {
    x = x + 1;
}

// CASO 5: Correcto - Función con 2 parámetros
entero suma(entero a, entero b) {
    entero resultado = a + b;
}

// CASO 6: Error - Función con solo 1 parámetro
decimal calcular(decimal n) {
    decimal res = n * 2.0;
}

// CASO 7: Correcto - Estructura si-sino
si (x > 10) {
    x = 0;
} sino {
    x = x + 1;
}

// CASO 8: Error - Falta llave de cierre
mientras (x < 100) {
    x = x + 1;

// CASO 9: Correcto - Estructura mientras
mientras (x < 50) {
    x = x + 5;
}

// CASO 10: Correcto - Estructura hacer
hacer {
    x = x - 1;
}

// CASO 11: Error - Tipo de dato inválido
numero x = 10;

// CASO 12: Error - Falta operador en expresión
entero z = 5 5;

// CASO 13: Correcto - Expresión compleja
entero complejo = (10 + 5) * 2 - 3;

// CASO 14: Error - Comparador inválido
si (x === 10) {
    x = 0;
}

// CASO 15: Correcto - Función con 3 parámetros
decimal promedio(decimal a, decimal b, decimal c) {
    decimal suma = a + b + c;
    decimal prom = suma / 3.0;
}
```

#### **1.5 Actualizar `src/interfaz_grafica.py`**

Modificar el método `analizar_codigo()` para integrar el análisis sintáctico:

```python
def analizar_codigo(self):
    """
    Analiza el código en el editor y muestra los resultados en las tablas.
    Ahora incluye análisis léxico y sintáctico.
    """
    # Limpiar resultados anteriores
    self._limpiar_tablas()
    
    codigo = self.texto_entrada.get("1.0", tk.END)
    
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
    # FASE 2: ANÁLISIS SINTÁCTICO (PARTE DE JORDIN)
    # ============================================
    from analizador_sintactico import AnalizadorSintactico
    
    analizador_sintactico = AnalizadorSintactico(tokens)
    ast, errores_sintacticos = analizador_sintactico.analizar()
    
    if errores_sintacticos:
        self._mostrar_errores(errores_sintacticos, "SINTÁCTICO")
        self._limpiar_tabla_resumen()
        return
    
    # ============================================
    # FASE 3: ANÁLISIS SEMÁNTICO (PARTE DE JAVIER)
    # Esto lo implementará Javier después
    # ============================================
    # from analizador_semantico import AnalizadorSemantico
    # 
    # analizador_semantico = AnalizadorSemantico(ast)
    # errores_semanticos = analizador_semantico.analizar()
    # 
    # if errores_semanticos:
    #     self._mostrar_errores(errores_semanticos, "SEMÁNTICO")
    #     self._limpiar_tabla_resumen()
    #     return
    
    # Si llegamos aquí, el análisis fue exitoso
    self._mostrar_lista_completa_tokens(tokens)
    self._mostrar_resumen_tokens(tokens)
    messagebox.showinfo(
        "Análisis Exitoso", 
        "✅ El código pasó el análisis léxico y sintáctico correctamente."
    )
```

También necesitarás modificar el método `_mostrar_errores` para aceptar el tipo de análisis:

```python
def _mostrar_errores(self, errores, tipo_analisis):
    """
    Muestra los errores encontrados en la tabla principal.
    
    Args:
        errores (list): Lista de errores
        tipo_analisis (str): "LÉXICO", "SINTÁCTICO" o "SEMÁNTICO"
    """
    self.tree_resultados.heading("Tipo", text=f"Error {tipo_analisis}")
    self.tree_resultados.heading("Valor", text="Detalle")
    self.tree_resultados.heading("Linea", text="Línea")
    
    for error in errores:
        if isinstance(error, dict):
            # Formato nuevo (sintáctico/semántico)
            tipo = error.get('tipo', tipo_analisis)
            mensaje = error.get('mensaje', 'Error desconocido')
            linea = error.get('linea', '?')
        else:
            # Formato antiguo (léxico)
            tipo, mensaje, linea = error
        
        self.tree_resultados.insert("", tk.END, values=(tipo, mensaje, linea))
```

#### **1.6 Documentación del código**

- Agrega docstrings detallados a todas las funciones
- Comenta las secciones complejas del parser
- Incluye ejemplos de uso en los comentarios

#### **1.7 Pruebas unitarias (opcional pero recomendado)**

Crear `tests/test_analizador_sintactico.py`:

```python
import unittest
from src.analizador_sintactico import AnalizadorSintactico
from src.analizador_lexico import AnalizadorLexico

class TestAnalizadorSintactico(unittest.TestCase):
    def setUp(self):
        self.analizador_lexico = AnalizadorLexico()
    
    def test_declaracion_variable_correcta(self):
        codigo = "entero x = 10;"
        tokens = self.analizador_lexico.analizar(codigo)
        parser = AnalizadorSintactico(tokens)
        ast, errores = parser.analizar()
        
        self.assertEqual(len(errores), 0)
        self.assertIsNotNone(ast)
    
    def test_error_falta_punto_coma(self):
        codigo = "entero x = 10"
        tokens = self.analizador_lexico.analizar(codigo)
        parser = AnalizadorSintactico(tokens)
        ast, errores = parser.analizar()
        
        self.assertGreater(len(errores), 0)
        self.assertIn("punto y coma", errores[0]['mensaje'].lower())
    
    # Agregar más pruebas...

if __name__ == '__main__':
    unittest.main()
```

---

## 🟢 PARTE 2 - JAVIER (50% del trabajo)

### **Tarea Principal**: Implementar el Analizador Semántico Completo y Finalizar Integración

#### **2.1 Crear el módulo `src/analizador_semantico.py`** (archivo nuevo)

Deberás crear una clase que valide la coherencia semántica del código.

**Estructura del archivo:**

```python
class AnalizadorSemantico:
    def __init__(self, ast):
        """
        Inicializa el analizador semántico.
        
        Args:
            ast: Árbol de sintaxis abstracta del parser
        """
        self.ast = ast
        self.tabla_simbolos = {}  # {nombre: {tipo, ambito, linea, categoria}}
        self.errores = []
        self.ambito_actual = "global"
        self.funciones = {}  # {nombre: {tipo_retorno, parametros}}
        
    def analizar(self):
        """
        Realiza el análisis semántico completo.
        
        Returns:
            list: Lista de errores semánticos encontrados
        """
        self.errores = []
        self._recorrer_ast(self.ast)
        return self.errores
    
    def _recorrer_ast(self, nodo):
        """
        Recorre el AST aplicando las reglas semánticas.
        
        Args:
            nodo: Nodo actual del AST
        """
        if nodo is None:
            return
        
        # Procesar según el tipo de nodo
        if nodo.tipo == 'DECLARACION_VARIABLE':
            self._verificar_declaracion_variable(nodo)
        elif nodo.tipo == 'DECLARACION_FUNCION':
            self._verificar_declaracion_funcion(nodo)
        elif nodo.tipo == 'ASIGNACION':
            self._verificar_asignacion(nodo)
        elif nodo.tipo == 'USO_VARIABLE':
            self._verificar_uso_variable(nodo)
        elif nodo.tipo == 'EXPRESION':
            self._verificar_expresion(nodo)
        
        # Recorrer hijos
        for hijo in nodo.hijos:
            self._recorrer_ast(hijo)
    
    def _verificar_declaracion_variable(self, nodo):
        """
        Verifica que una variable sea declarada correctamente.
        
        Reglas:
        - Variable no debe estar declarada previamente en el mismo ámbito
        - Tipo de dato debe ser válido
        - El valor asignado debe ser compatible con el tipo
        """
        pass
    
    def _verificar_asignacion(self, nodo):
        """
        Verifica compatibilidad de tipos en asignaciones.
        
        Reglas:
        - Variable debe estar declarada antes de usarse
        - Tipo de la expresión debe ser compatible con el tipo de la variable
        """
        pass
    
    def _verificar_uso_variable(self, nodo):
        """
        Verifica que una variable usada exista.
        
        Reglas:
        - Variable debe estar declarada antes de usarse
        """
        pass
    
    def _verificar_declaracion_funcion(self, nodo):
        """
        Verifica declaración de función.
        
        Reglas:
        - Función no debe estar declarada previamente
        - Debe tener mínimo 2 parámetros
        - Los parámetros deben tener nombres únicos
        - El tipo de retorno debe ser válido
        """
        pass
    
    def _verificar_expresion(self, nodo):
        """
        Verifica que una expresión sea semánticamente correcta.
        
        Reglas:
        - Operaciones entre tipos compatibles
        - Variables usadas deben existir
        """
        pass
    
    def _verificar_compatibilidad_tipos(self, tipo1, tipo2, operacion=None):
        """
        Verifica si dos tipos son compatibles para una operación.
        
        Args:
            tipo1: Primer tipo
            tipo2: Segundo tipo
            operacion: Operación a realizar ('+', '-', '*', '/', etc.)
        
        Returns:
            bool: True si son compatibles, False en caso contrario
        """
        # Reglas de compatibilidad:
        # - entero + entero = entero
        # - decimal + decimal = decimal
        # - entero + decimal = decimal
        # - cadena + cadena = cadena (concatenación)
        # - booleano solo con booleano en operaciones lógicas
        pass
    
    def _inferir_tipo_expresion(self, nodo):
        """
        Infiere el tipo de una expresión.
        
        Args:
            nodo: Nodo de tipo EXPRESION
        
        Returns:
            str: Tipo inferido ('entero', 'decimal', 'cadena', 'booleano')
        """
        pass
    
    def _agregar_simbolo(self, nombre, tipo, categoria, linea):
        """
        Agrega un símbolo a la tabla de símbolos.
        
        Args:
            nombre: Nombre del símbolo
            tipo: Tipo del símbolo
            categoria: 'variable' o 'funcion'
            linea: Línea donde se declaró
        """
        clave = f"{self.ambito_actual}:{nombre}"
        
        if clave in self.tabla_simbolos:
            self.errores.append({
                'tipo': 'SEMÁNTICO',
                'mensaje': f"'{nombre}' ya fue declarado anteriormente",
                'linea': linea,
                'detalle': f"Primera declaración en línea {self.tabla_simbolos[clave]['linea']}"
            })
        else:
            self.tabla_simbolos[clave] = {
                'tipo': tipo,
                'categoria': categoria,
                'ambito': self.ambito_actual,
                'linea': linea
            }
    
    def _buscar_simbolo(self, nombre):
        """
        Busca un símbolo en la tabla de símbolos.
        
        Args:
            nombre: Nombre del símbolo a buscar
        
        Returns:
            dict: Información del símbolo o None si no existe
        """
        # Buscar primero en el ámbito actual
        clave = f"{self.ambito_actual}:{nombre}"
        if clave in self.tabla_simbolos:
            return self.tabla_simbolos[clave]
        
        # Buscar en ámbito global
        clave_global = f"global:{nombre}"
        if clave_global in self.tabla_simbolos:
            return self.tabla_simbolos[clave_global]
        
        return None
    
    def _agregar_error(self, mensaje, linea, detalle=""):
        """
        Agrega un error a la lista de errores semánticos.
        
        Args:
            mensaje: Mensaje de error
            linea: Línea donde ocurrió el error
            detalle: Información adicional
        """
        self.errores.append({
            'tipo': 'SEMÁNTICO',
            'mensaje': mensaje,
            'linea': linea,
            'detalle': detalle
        })
```

#### **2.2 Implementar detección de errores semánticos**

Debes detectar y reportar los siguientes errores:

**Errores de declaración:**
- ✗ Variable usada sin declarar
- ✗ Variable declarada múltiples veces en el mismo ámbito
- ✗ Función declarada múltiples veces
- ✗ Parámetros de función con nombres duplicados

**Errores de tipos:**
- ✗ Asignación de tipo incompatible (ej: `entero x = "texto";`)
- ✗ Operaciones entre tipos incompatibles (ej: `entero + cadena`)
- ✗ Comparación entre tipos incompatibles

**Errores de funciones:**
- ✗ Función con menos de 2 parámetros
- ✗ Llamada a función no declarada
- ✗ Número incorrecto de argumentos en llamada

**Matriz de compatibilidad de tipos:**

```python
COMPATIBILIDAD_TIPOS = {
    ('entero', 'entero'): {'+': 'entero', '-': 'entero', '*': 'entero', '/': 'entero', '%': 'entero'},
    ('decimal', 'decimal'): {'+': 'decimal', '-': 'decimal', '*': 'decimal', '/': 'decimal'},
    ('entero', 'decimal'): {'+': 'decimal', '-': 'decimal', '*': 'decimal', '/': 'decimal'},
    ('decimal', 'entero'): {'+': 'decimal', '-': 'decimal', '*': 'decimal', '/': 'decimal'},
    ('cadena', 'cadena'): {'+': 'cadena'},  # Concatenación
    ('booleano', 'booleano'): {}  # Solo comparaciones
}
```

#### **2.3 Crear archivo de pruebas `tests/casos_semanticos.txt`**

```
// ========================================
// CASOS SEMÁNTICOS - ARCHIVO DE PRUEBA
// ========================================

// CASO 1: Error - variable usada sin declarar
x = 10;

// CASO 2: Error - tipos incompatibles en asignación
entero numero = "texto";

// CASO 3: Correcto - declaración y uso normal
entero a = 5;
entero b = a + 10;

// CASO 4: Error - variable declarada dos veces
decimal pi = 3.14;
decimal pi = 3.1416;

// CASO 5: Correcto - diferentes tipos de datos
entero contador = 0;
decimal precio = 99.99;
cadena nombre = "Producto";
booleano activo = verdadero;

// CASO 6: Error - función con menos de 2 parámetros
entero calcular(entero x) {
    entero resultado = x * 2;
}

// CASO 7: Correcto - función con 2 parámetros
entero multiplicar(entero a, entero b) {
    entero resultado = a * b;
}

// CASO 8: Correcto - función con 3 parámetros
decimal promedio(decimal n1, decimal n2, decimal n3) {
    decimal suma = n1 + n2 + n3;
    decimal resultado = suma / 3.0;
}

// CASO 9: Error - operación entre tipos incompatibles
entero num = 10;
cadena texto = "hola";
entero suma = num + texto;

// CASO 10: Error - usar variable de otro tipo en operación numérica
cadena mensaje = "Hola";
entero longitud = mensaje * 2;

// CASO 11: Correcto - mezcla de entero y decimal
entero x = 10;
decimal y = 3.5;
decimal resultado = x + y;

// CASO 12: Error - parámetros con nombres duplicados
entero sumar_mal(entero a, entero a) {
    entero resultado = a + a;
}

// CASO 13: Correcto - uso de variable en estructura de control
entero edad = 18;
si (edad >= 18) {
    booleano adulto = verdadero;
}

// CASO 14: Error - comparación entre tipos incompatibles
entero numero = 5;
cadena texto = "5";
si (numero == texto) {
    numero = 0;
}

// CASO 15: Correcto - operaciones booleanas
booleano activo = verdadero;
booleano inactivo = falso;
si (activo == verdadero) {
    activo = falso;
}
```

#### **2.4 Completar integración en `src/interfaz_grafica.py`**

Descomentar y completar la sección del análisis semántico en el método `analizar_codigo()`:

```python
def analizar_codigo(self):
    """
    Analiza el código en el editor y muestra los resultados en las tablas.
    Incluye análisis léxico, sintáctico y semántico.
    """
    # Limpiar resultados anteriores
    self._limpiar_tablas()
    
    codigo = self.texto_entrada.get("1.0", tk.END)
    
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
    from analizador_sintactico import AnalizadorSintactico
    
    analizador_sintactico = AnalizadorSintactico(tokens)
    ast, errores_sintacticos = analizador_sintactico.analizar()
    
    if errores_sintacticos:
        self._mostrar_errores(errores_sintacticos, "SINTÁCTICO")
        self._limpiar_tabla_resumen()
        return
    
    # ============================================
    # FASE 3: ANÁLISIS SEMÁNTICO (TU PARTE - JAVIER)
    # ============================================
    from analizador_semantico import AnalizadorSemantico
    
    analizador_semantico = AnalizadorSemantico(ast)
    errores_semanticos = analizador_semantico.analizar()
    
    if errores_semanticos:
        self._mostrar_errores(errores_semanticos, "SEMÁNTICO")
        self._limpiar_tabla_resumen()
        return
    
    # ============================================
    # ANÁLISIS EXITOSO
    # ============================================
    self._mostrar_lista_completa_tokens(tokens)
    self._mostrar_resumen_tokens(tokens)
    self._mostrar_tabla_simbolos(analizador_semantico.tabla_simbolos)
    
    messagebox.showinfo(
        "✅ Análisis Completo Exitoso",
        "El código es correcto:\n\n"
        "✓ Análisis Léxico\n"
        "✓ Análisis Sintáctico\n"
        "✓ Análisis Semántico\n\n"
        "No se encontraron errores."
    )
```

#### **2.5 Mejorar visualización de resultados en la interfaz**

Agregar una nueva sección para mostrar la tabla de símbolos:

```python
def _crear_area_resultados(self, parent):
    """
    Crea el área de resultados con las tablas.
    """
    resultados_frame = ttk.Frame(parent)
    resultados_frame.grid(row=0, column=1, sticky="nsew")
    resultados_frame.grid_rowconfigure(0, weight=2)  # Tabla principal
    resultados_frame.grid_rowconfigure(1, weight=1)  # Tabla resumen
    resultados_frame.grid_rowconfigure(2, weight=1)  # Tabla de símbolos (NUEVO)
    resultados_frame.grid_columnconfigure(0, weight=1)

    # Tabla principal de tokens
    self._crear_tabla_principal(resultados_frame)

    # Tabla de resumen
    self._crear_tabla_resumen(resultados_frame)
    
    # Tabla de símbolos (NUEVO)
    self._crear_tabla_simbolos(resultados_frame)

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

    self.tree_simbolos = ttk.Treeview(
        simbolos_frame, 
        columns=("Nombre", "Tipo", "Categoría", "Ámbito", "Línea"), 
        show="headings"
    )
    self.tree_simbolos.heading("Nombre", text="Nombre")
    self.tree_simbolos.heading("Tipo", text="Tipo")
    self.tree_simbolos.heading("Categoría", text="Categoría")
    self.tree_simbolos.heading("Ámbito", text="Ámbito")
    self.tree_simbolos.heading("Línea", text="Línea")

    self.tree_simbolos.column("Nombre", width=100)
    self.tree_simbolos.column("Tipo", width=80)
    self.tree_simbolos.column("Categoría", width=80)
    self.tree_simbolos.column("Ámbito", width=80)
    self.tree_simbolos.column("Línea", width=50, anchor="center")

    # Scrollbar
    scrollbar_simbolos = ttk.Scrollbar(
        simbolos_frame, orient=tk.VERTICAL, command=self.tree_simbolos.yview
    )
    self.tree_simbolos.configure(yscroll=scrollbar_simbolos.set)

    self.tree_simbolos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar_simbolos.pack(side=tk.RIGHT, fill=tk.Y)

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
        partes = clave.split(':', 1)
        nombre = partes[1] if len(partes) > 1 else partes[0]
        
        self.tree_simbolos.insert("", tk.END, values=(
            nombre,
            info['tipo'],
            info['categoria'],
            info['ambito'],
            info['linea']
        ))

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
```

#### **2.6 Crear archivo de prueba integral `tests/programa_completo.txt`**

Un archivo que combine todas las estructuras correctamente y pase los tres análisis:

```
// ========================================
// PROGRAMA COMPLETO - PRUEBA INTEGRAL
// Debe pasar análisis léxico, sintáctico y semántico
// ========================================

// ============================================
// SECCIÓN 1: DECLARACIÓN DE VARIABLES
// ============================================

entero contador = 0;
decimal precio = 99.99;
cadena nombre = "Producto Premium";
cadena descripcion = 'Descripción del producto';
booleano activo = verdadero;
booleano disponible = falso;

// ============================================
// SECCIÓN 2: DECLARACIÓN DE FUNCIONES
// ============================================

// Función con 2 parámetros - suma de enteros
entero sumar(entero a, entero b) {
    entero resultado = a + b;
}

// Función con 2 parámetros - multiplicación de decimales
decimal multiplicar(decimal x, decimal y) {
    decimal resultado = x * y;
}

// Función con 3 parámetros - calcular promedio
decimal calcular_promedio(decimal n1, decimal n2, decimal n3) {
    decimal suma = n1 + n2 + n3;
    decimal promedio = suma / 3.0;
}

// Función con 4 parámetros - operación compleja
entero operacion_compleja(entero a, entero b, entero c, entero d) {
    entero temp1 = a + b;
    entero temp2 = c * d;
    entero resultado = temp1 - temp2;
}

// ============================================
// SECCIÓN 3: ESTRUCTURAS DE CONTROL
// ============================================

// Estructura SI simple
si (contador > 0) {
    contador = contador + 1;
}

// Estructura SI-SINO
si (precio > 100.0) {
    decimal descuento = precio * 0.1;
    precio = precio - descuento;
} sino {
    precio = precio + 5.0;
}

// Estructura MIENTRAS
mientras (contador < 10) {
    contador = contador + 1;
}

// Estructura HACER
hacer {
    activo = falso;
}

// ============================================
// SECCIÓN 4: EXPRESIONES COMPLEJAS
// ============================================

// Operaciones aritméticas
entero a = 10;
entero b = 20;
entero suma = a + b;
entero resta = a - b;
entero multiplicacion = a * b;
entero division = a / b;
entero modulo = a % b;

// Operaciones con paréntesis
entero complejo = (10 + 5) * 2 - 3;
decimal decimal_complejo = (3.14 * 2.0) + (5.5 - 1.5);

// Operaciones mixtas (entero y decimal)
entero entero_val = 10;
decimal decimal_val = 3.5;
decimal resultado_mixto = entero_val + decimal_val;

// Concatenación de cadenas
cadena saludo = "Hola, ";
cadena nombre_usuario = "Usuario";
cadena mensaje = saludo + nombre_usuario;

// ============================================
// SECCIÓN 5: COMPARACIONES
// ============================================

// Comparaciones numéricas
si (a == b) {
    entero igual = 1;
}

si (a != b) {
    entero diferente = 1;
}

si (a < b) {
    entero menor = 1;
}

si (a > b) {
    entero mayor = 1;
}

si (a <= b) {
    entero menor_igual = 1;
}

si (a >= b) {
    entero mayor_igual = 1;
}

// Comparaciones booleanas
si (activo == verdadero) {
    activo = falso;
}

si (disponible == falso) {
    disponible = verdadero;
}

// ============================================
// SECCIÓN 6: ESTRUCTURAS ANIDADAS
// ============================================

si (contador > 5) {
    si (activo == verdadero) {
        contador = 0;
    } sino {
        contador = contador - 1;
    }
}

mientras (contador < 100) {
    si (contador % 2 == 0) {
        contador = contador + 2;
    } sino {
        contador = contador + 1;
    }
}

// ============================================
// FIN DEL PROGRAMA
// ============================================
```

#### **2.7 Actualizar documentación `docs/manual_de_usuario.md`**

Expandir el manual de usuario con la nueva funcionalidad:

```markdown
# Manual de Usuario: Analizador Léxico, Sintáctico y Semántico

## 1. Introducción

Este programa es una herramienta completa de análisis de código que implementa las tres fases principales de un compilador:

1. **Análisis Léxico**: Identifica los tokens (palabras clave, identificadores, operadores, etc.)
2. **Análisis Sintáctico**: Verifica que la estructura del código sea correcta según la gramática del lenguaje
3. **Análisis Semántico**: Valida la coherencia del código (tipos de datos, uso de variables, etc.)

La aplicación cuenta con una interfaz gráfica intuitiva que permite cargar archivos, analizar su contenido y visualizar los resultados de forma clara y organizada, incluyendo la detección y reporte de errores en cualquiera de las tres fases.

## 2. Requisitos del Sistema

- **Sistema Operativo:** Windows, macOS o Linux
- **Python:** Versión 3.6 o superior
- **Librerías:** No se requieren librerías externas (usa la librería estándar de Python)

## 3. Instalación y Ejecución

El programa no requiere un proceso de instalación formal. Solo necesitas tener Python instalado en tu sistema.

Para ejecutar la aplicación:

1. Abre una terminal o línea de comandos
2. Navega hasta el directorio raíz del proyecto
3. Ejecuta el siguiente comando:
   ```bash
   python src/main.py
   ```
4. Se abrirá la ventana principal de la aplicación

## 4. Guía de Uso de la Interfaz Gráfica

La interfaz se divide en varias áreas principales:

### 4.1. Barra de Botones

En la parte superior encontrarás tres botones:

- **Cargar Archivo (.txt):** Abre un explorador de archivos para seleccionar y cargar un archivo de texto
- **Analizar Código:** Inicia el análisis completo del código (léxico, sintáctico y semántico)
- **Limpiar:** Restablece la interfaz a su estado inicial

### 4.2. Área de Código Fuente

Editor de texto donde puedes:
- Escribir código directamente
- Pegar código desde el portapapeles
- Ver el contenido de archivos cargados

### 4.3. Área de Resultados

Compuesta por tres tablas:

#### Tabla 1: Tokens y Errores
- Si el análisis es **exitoso**: Muestra todos los tokens encontrados
- Si hay **errores**: Muestra únicamente los errores detectados con el tipo de análisis donde fallaron

#### Tabla 2: Resumen de Tokens
- Se llena solo si el análisis es completamente exitoso
- Muestra un conteo de cada tipo de token encontrado

#### Tabla 3: Tabla de Símbolos (NUEVO)
- Se llena solo si el análisis es completamente exitoso
- Muestra todas las variables y funciones declaradas con su:
  - Nombre
  - Tipo de dato
  - Categoría (variable o función)
  - Ámbito (global o local)
  - Línea de declaración

## 5. Tipos de Análisis

### 5.1. Análisis Léxico

**Qué detecta:**
- Tokens válidos del lenguaje
- Caracteres no reconocidos
- Errores en la formación de tokens

**Ejemplo de error léxico:**
```
entero x@ = 10;  // Error: '@' no es un carácter válido
```

### 5.2. Análisis Sintáctico (NUEVO)

**Qué detecta:**
- Estructura correcta de declaraciones
- Uso correcto de paréntesis, llaves y punto y coma
- Funciones con el número correcto de parámetros (mínimo 2)
- Estructura correcta de expresiones
- Orden correcto de las instrucciones

**Ejemplos de errores sintácticos:**
```
entero x = 10    // Error: Falta punto y coma

si (x > 5 {      // Error: Falta paréntesis de cierre
}

entero calcular(entero x) {  // Error: Función requiere mínimo 2 parámetros
}
```

### 5.3. Análisis Semántico (NUEVO)

**Qué detecta:**
- Variables usadas sin declarar
- Variables declaradas múltiples veces
- Incompatibilidad de tipos en asignaciones
- Operaciones entre tipos incompatibles
- Funciones declaradas múltiples veces
- Parámetros duplicados en funciones

**Ejemplos de errores semánticos:**
```
x = 10;                    // Error: 'x' no está declarada

entero num = "texto";      // Error: Tipo incompatible

entero a = 5;
cadena b = "hola";
entero c = a + b;          // Error: No se puede sumar entero con cadena

decimal pi = 3.14;
decimal pi = 3.1416;       // Error: 'pi' ya fue declarada
```

## 6. Cómo Probar el Analizador

En la carpeta `tests/` hay varios archivos de prueba:

### Archivos de Prueba Disponibles:

1. **casos_positivos.txt**: Código léxicamente correcto
2. **casos_negativos.txt**: Errores léxicos
3. **casos_sintacticos.txt**: Casos de prueba para análisis sintáctico
4. **casos_semanticos.txt**: Casos de prueba para análisis semántico
5. **programa_completo.txt**: Programa integral que pasa todos los análisis

### Procedimiento de Prueba:

1. Ejecuta el programa
2. Haz clic en **"Cargar Archivo"**
3. Selecciona uno de los archivos de prueba
4. Haz clic en **"Analizar Código"**
5. Observa los resultados en las tablas

## 7. Lenguaje Soportado

### 7.1. Tipos de Datos

- `entero`: Números enteros
- `decimal`: Números con decimales
- `cadena`: Texto entre comillas simples o dobles
- `booleano`: Valores `verdadero` o `falso`

### 7.2. Declaración de Variables

```
TIPO IDENTIFICADOR = EXPRESION;

Ejemplos:
entero edad = 25;
decimal precio = 99.99;
cadena nombre = "Juan";
booleano activo = verdadero;
```

### 7.3. Declaración de Funciones

Las funciones **deben tener mínimo 2 parámetros**:

```
TIPO NOMBRE(TIPO param1, TIPO param2, ...) {
    // cuerpo de la función
}

Ejemplos:
entero sumar(entero a, entero b) {
    entero resultado = a + b;
}

decimal promedio(decimal n1, decimal n2, decimal n3) {
    decimal suma = n1 + n2 + n3;
    decimal prom = suma / 3.0;
}
```

### 7.4. Estructuras de Control

#### Estructura Si-Sino:
```
si (CONDICION) {
    // código
} sino {
    // código alternativo
}
```

#### Estructura Mientras:
```
mientras (CONDICION) {
    // código
}
```

#### Estructura Hacer:
```
hacer {
    // código
}
```

### 7.5. Operadores

**Aritméticos:** `+`, `-`, `*`, `/`, `%`

**Comparación:** `==`, `!=`, `<`, `>`, `<=`, `>=`

**Asignación:** `=`

### 7.6. Reglas de Compatibilidad de Tipos

| Operación | Tipos Permitidos | Resultado |
|-----------|-----------------|-----------|
| `entero + entero` | ✓ | `entero` |
| `decimal + decimal` | ✓ | `decimal` |
| `entero + decimal` | ✓ | `decimal` |
| `cadena + cadena` | ✓ | `cadena` |
| `entero + cadena` | ✗ | Error |
| `booleano + booleano` | ✗ | Error |

## 8. Solución de Problemas

### El programa no inicia
- Verifica que tengas Python 3.6 o superior instalado
- Asegúrate de estar en el directorio correcto del proyecto

### Errores al cargar archivos
- Verifica que el archivo sea de texto plano (.txt)
- Asegúrate de que el archivo tenga codificación UTF-8 o Latin-1

### El análisis no detecta errores obvios
- Verifica que hayas hecho clic en "Analizar Código"
- Revisa que el código esté en el editor de texto

## 9. Contacto y Soporte

Para reportar problemas o sugerencias:
- Jordin: [tu_email]
- Javier: [email_javier]

---

**Última actualización:** Octubre 2024
**Versión:** 2.0 (Análisis Completo)
```

#### **2.8 Crear archivo `docs/documentacion_tecnica.md`**

Documentación técnica para el video explicativo:

```markdown
# Documentación Técnica - Analizador Completo

## Arquitectura del Sistema

El proyecto está dividido en módulos independientes que trabajan en secuencia:

```
┌─────────────────────────┐
│   Código Fuente (.txt)  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Analizador Léxico      │ ← Identifica tokens
│  (analizador_lexico.py) │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Analizador Sintáctico  │ ← Verifica estructura
│  (analizador_sintactico.py)│ → Genera AST
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Analizador Semántico   │ ← Valida coherencia
│  (analizador_semantico.py)│ → Tabla de símbolos
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Interfaz Gráfica       │ ← Muestra resultados
│  (interfaz_grafica.py)  │
└─────────────────────────┘
```

## Componentes del Sistema

### 1. Analizador Léxico (`analizador_lexico.py`)

**Responsabilidad:** Convertir el texto en tokens

**Método principal:**
```python
def analizar(self, codigo) -> List[Tuple[str, str, int]]
```

**Algoritmo:**
1. Utiliza expresiones regulares para identificar patrones
2. Recorre el código carácter por carácter
3. Genera una lista de tuplas (tipo_token, valor, línea)

**Complejidad:** O(n) donde n es la longitud del código

### 2. Analizador Sintáctico (`analizador_sintactico.py`)

**Responsabilidad:** Verificar estructura según gramática

**Método principal:**
```python
def analizar(self) -> Tuple[NodoAST, List[dict]]
```

**Algoritmo:** Parser Descendente Recursivo
1. Comienza desde el símbolo inicial (PROGRAMA)
2. Aplica reglas de la gramática recursivamente
3. Construye un Árbol de Sintaxis Abstracta (AST)
4. Detecta errores estructurales

**Estructura del AST:**
```python
class NodoAST:
    tipo: str      # Tipo de nodo
    valor: Any     # Valor asociado
    hijos: List    # Nodos hijos
    linea: int     # Línea del código
```

**Complejidad:** O(n) donde n es el número de tokens

### 3. Analizador Semántico (`analizador_semantico.py`)

**Responsabilidad:** Validar coherencia del código

**Método principal:**
```python
def analizar(self) -> List[dict]
```

**Algoritmo:** Recorrido del AST con validaciones
1. Recorre el AST usando patrón Visitor
2. Mantiene una tabla de símbolos
3. Verifica reglas semánticas en cada nodo
4. Detecta errores de tipos y declaraciones

**Tabla de Símbolos:**
```python
{
    "ambito:nombre": {
        "tipo": str,
        "categoria": str,  # "variable" o "funcion"
        "ambito": str,
        "linea": int
    }
}
```

**Complejidad:** O(n) donde n es el número de nodos del AST

### 4. Interfaz Gráfica (`interfaz_grafica.py`)

**Responsabilidad:** Interacción con el usuario

**Componentes:**
- Editor de texto (ScrolledText)
- Tabla de tokens y errores (Treeview)
- Tabla de resumen (Treeview)
- Tabla de símbolos (Treeview)

**Flujo de ejecución:**
```python
Usuario carga archivo
    ↓
Usuario hace clic en "Analizar"
    ↓
Análisis Léxico
    ↓
¿Errores léxicos? → Sí → Mostrar errores → FIN
    ↓ No
Análisis Sintáctico
    ↓
¿Errores sintácticos? → Sí → Mostrar errores → FIN
    ↓ No
Análisis Semántico
    ↓
¿Errores semánticos? → Sí → Mostrar errores → FIN
    ↓ No
Mostrar éxito y tabla de símbolos
```

## Gramática del Lenguaje

La gramática completa se encuentra en el archivo del analizador sintáctico.

## Reglas Semánticas

1. **Variables:**
   - Deben declararse antes de usarse
   - No pueden declararse dos veces en el mismo ámbito
   - El tipo de la expresión debe ser compatible

2. **Funciones:**
   - Deben tener mínimo 2 parámetros
   - No pueden declararse dos veces
   - Los parámetros deben tener nombres únicos

3. **Tipos:**
   - Las operaciones deben ser entre tipos compatibles
   - Las asignaciones deben respetar los tipos

## Decisiones de Diseño

1. **Parser Descendente Recursivo:** Elegido por su simplicidad y facilidad de debugging

2. **AST vs Parse Tree:** Se usa AST para eliminar información innecesaria y facilitar el análisis semántico

3. **Tabla de Símbolos:** Estructura de diccionario para búsquedas O(1)

4. **Ámbitos:** Se usa el prefijo "ambito:nombre" para soportar variables locales y globales

## Pruebas

Cada módulo tiene su archivo de pruebas en `tests/`:
- `casos_positivos.txt`
- `casos_negativos.txt`
- `casos_sintacticos.txt`
- `casos_semanticos.txt`
- `programa_completo.txt`

## Mejoras Futuras Posibles

1. Soporte para llamadas a funciones
2. Arreglos y estructuras de datos
3. Más tipos de datos (carácter, etc.)
4. Optimización del AST
5. Generación de código intermedio
```

---

## 📋 Checklist de Entregables

### ✅ Parte de Jordin (Análisis Sintáctico):

- [ ] `src/analizador_sintactico.py` - Clase completa
- [ ] Implementación de todas las reglas gramaticales
- [ ] Clase `NodoAST` para el árbol de sintaxis
- [ ] Detección de errores sintácticos con mensajes claros
- [ ] Generación correcta del AST
- [ ] `tests/casos_sintacticos.txt` - Casos de prueba
- [ ] Integración parcial en `interfaz_grafica.py`
- [ ] Pruebas del analizador sintáctico funcionando
- [ ] Documentación del código con docstrings

### ✅ Parte de Javier (Análisis Semántico e Integración):

- [ ] `src/analizador_semantico.py` - Clase completa
- [ ] Tabla de símbolos funcional
- [ ] Verificación de tipos y compatibilidad
- [ ] Detección de todos los errores semánticos requeridos
- [ ] `tests/casos_semanticos.txt` - Casos de prueba
- [ ] `tests/programa_completo.txt` - Prueba integral
- [ ] Integración completa en `interfaz_grafica.py`
- [ ] Nueva tabla de símbolos en la interfaz
- [ ] Actualización de `docs/manual_de_usuario.md`
- [ ] Creación de `docs/documentacion_tecnica.md`
- [ ] Mejoras visuales en la interfaz
- [ ] Pruebas integrales exitosas

---

## 🎯 Puntos de Coordinación

### Sincronización Requerida:

1. **Después de que Jordin termine el AST:**
   - Javier debe revisar la estructura del AST para diseñar el analizador semántico correctamente
   - Coordinar una reunión para revisar los nombres de los nodos y su estructura

2. **Formato de errores estandarizado:**
   Ambos deben usar este formato:
   ```python
   {
       'tipo': 'SINTÁCTICO' o 'SEMÁNTICO',
       'mensaje': 'Descripción del error',
       'linea': numero_linea,
       'detalle': 'Información adicional (opcional)'
   }
   ```

3. **Reunión intermedia:**
   - Cuando Jordin complete el 70-80% del parser
   - Revisar juntos el AST generado
   - Asegurar compatibilidad con el analizador semántico

4. **Pruebas conjuntas:**
   - Probar con `programa_completo.txt`
   - Verificar que los tres análisis funcionen en secuencia
   - Ajustar detalles finales

---

## ⏰ Cronograma Sugerido

### Semana 1 (7 días):
**Jordin:**
- Días 1-2: Estructura básica del parser y clase NodoAST
- Días 3-4: Implementar reglas de declaración de variables
- Días 5-6: Implementar estructuras de control
- Día 7: Implementar declaración de funciones

**Javier:**
- Días 1-3: Estudiar teoría de análisis semántico y tabla de símbolos
- Días 4-5: Diseñar estructura del analizador semántico
- Días 6-7: Revisar el AST de Jordin y ajustar diseño

### Semana 2 (7 días):
**Jordin:**
- Días 1-2: Implementar análisis de expresiones
- Días 3-4: Generar AST completo
- Días 5-6: Crear `casos_sintacticos.txt` y probar
- Día 7: Integración básica en interfaz gráfica

**Javier:**
- Días 1-2: Implementar tabla de símbolos
- Días 3-4: Implementar verificación de declaraciones
- Días 5-6: Implementar verificación de tipos
- Día 7: Crear `casos_semanticos.txt`

### Semana 3 (7 días):
**Jordin:**
- Días 1-2: Refinamiento del parser
- Días 3-4: Corrección de bugs
- Días 5-7: Documentación del código

**Javier:**
- Días 1-2: Completar verificaciones semánticas
- Días 3-4: Integración completa en interfaz
- Días 5-6: Crear tabla de símbolos en UI
- Día 7: Crear `programa_completo.txt`

### Semana 4 (7 días):
**Ambos (trabajo conjunto):**
- Días 1-2: Pruebas integrales con todos los archivos de prueba
- Días 3-4: Corrección de bugs encontrados
- Día 5: Actualizar documentación completa
- Día 6: Crear video explicativo
- Día 7: Revisión final y preparar entrega

---

## 🚀 Comandos Útiles

### Ejecutar el programa:
```bash
python src/main.py
```

### Ejecutar pruebas unitarias (si las implementan):
```bash
python -m unittest discover tests/
```

### Verificar sintaxis de Python:
```bash
python -m py_compile src/*.py
```

---

## 📞 Comunicación

### Canales recomendados:
- **WhatsApp/Telegram:** Para coordinación diaria
- **GitHub Issues:** Para reportar bugs y discutir funcionalidades
- **GitHub Pull Requests:** Para revisión de código
- **Video llamada:** Para reuniones de sincronización

### Reuniones sugeridas:
1. **Reunión inicial:** Revisar este plan juntos
2. **Reunión intermedia (semana 2):** Revisar AST y compatibilidad
3. **Reunión de integración (semana 3):** Probar todo junto
4. **Reunión final (semana 4):** Preparar entrega

---

## ✨ Consejos Importantes

### Para Jordin (Parser):
1. Comienza con las reglas más simples (declaración de variables)
2. Prueba cada regla gramatical individualmente
3. El AST no tiene que ser perfecto, solo consistente
4. Documenta bien la estructura de cada tipo de nodo
5. Usa `print()` para debugging del AST durante desarrollo
6. No te preocupes si el código es largo, la claridad es más importante
7. Guarda versiones de trabajo en commits frecuentes

### Para Javier (Análisis Semántico):
1. Espera a que el AST de Jordin esté estable antes de avanzar mucho
2. La tabla de símbolos es el corazón del análisis semántico
3. Piensa en todos los casos de error posibles
4. Prueba con casos extremos (variables con nombres similares, etc.)
5. La verificación de tipos puede ser compleja, hazlo paso a paso
6. Documenta las reglas semánticas que implementes
7. La interfaz gráfica es importante, dedícale tiempo

### Para Ambos:
1. **Commits frecuentes:** Hagan commit cada vez que completen una funcionalidad
2. **Mensajes descriptivos:** "Implementado análisis de expresiones" es mejor que "cambios"
3. **No tengan miedo de preguntar:** Si algo no está claro, comuníquense
4. **Prueben constantemente:** No esperen a tener todo listo para probar
5. **Mantengan el código limpio:** Sigan el estilo PEP 8 de Python
6. **Comentarios útiles:** Expliquen el "por qué", no el "qué"
7. **Backup:** Hagan push a GitHub frecuentemente

---

## 🎓 Recursos de Apoyo

### Conceptos teóricos importantes:

1. **Parser Descendente Recursivo:**
   - Cada regla gramatical se convierte en un método
   - Los métodos se llaman recursivamente según la gramática
   - Es fácil de implementar y entender

2. **Árbol de Sintaxis Abstracta (AST):**
   - Representa la estructura del programa
   - Elimina detalles innecesarios (paréntesis, punto y coma, etc.)
   - Facilita el análisis semántico

3. **Tabla de Símbolos:**
   - Almacena información sobre identificadores
   - Permite verificar declaraciones y usos
   - Soporta ámbitos (scopes)

4. **Análisis Semántico:**
   - Verifica reglas que no pueden expresarse con gramática
   - Asegura consistencia de tipos
   - Detecta errores lógicos

### Ejemplo completo de flujo:

**Código fuente:**
```
entero x = 10 + 5;
```

**Después del Análisis Léxico:**
```python
[
    ('PALABRA_RESERVADA', 'entero', 1),
    ('IDENTIFICADOR', 'x', 1),
    ('ASIGNACION', '=', 1),
    ('NUMERO_ENTERO', '10', 1),
    ('OPERADOR', '+', 1),
    ('NUMERO_ENTERO', '5', 1),
    ('PUNTOYCOMA', ';', 1)
]
```

**Después del Análisis Sintáctico (AST):**
```python
NodoAST(
    tipo='DECLARACION_VARIABLE',
    linea=1,
    hijos=[
        NodoAST(tipo='TIPO', valor='entero'),
        NodoAST(tipo='IDENTIFICADOR', valor='x'),
        NodoAST(
            tipo='EXPRESION',
            hijos=[
                NodoAST(tipo='SUMA',
                    hijos=[
                        NodoAST(tipo='NUMERO', valor=10),
                        NodoAST(tipo='NUMERO', valor=5)
                    ]
                )
            ]
        )
    ]
)
```

**Después del Análisis Semántico:**
```python
Tabla de Símbolos:
{
    'global:x': {
        'tipo': 'entero',
        'categoria': 'variable',
        'ambito': 'global',
        'linea': 1
    }
}

Errores: []  # Sin errores
```

---

## 🐛 Problemas Comunes y Soluciones

### Problema 1: El parser entra en recursión infinita
**Causa:** Regla gramatical con recursión a la izquierda
**Solución:** Reescribir la regla eliminando la recursión a la izquierda

### Problema 2: El AST se hace muy grande
**Causa:** Se están guardando demasiados detalles
**Solución:** Simplificar el AST, eliminar nodos innecesarios

### Problema 3: Errores semánticos no se detectan
**Causa:** El recorrido del AST no está visitando todos los nodos
**Solución:** Asegurar que `_recorrer_ast()` visita todos los hijos

### Problema 4: La interfaz se congela
**Causa:** El análisis tarda mucho (archivos muy grandes)
**Solución:** Agregar límite de tamaño o implementar threading

### Problema 5: Mensajes de error poco claros
**Causa:** No se está dando suficiente contexto
**Solución:** Incluir número de línea y sugerencias en los mensajes

---

## 📊 Métricas de Éxito

El proyecto estará completo cuando:

- ✅ Los tres analizadores funcionen correctamente
- ✅ Todos los archivos de prueba pasen o fallen según esperado
- ✅ La interfaz gráfica sea intuitiva y estética
- ✅ El código esté bien documentado
- ✅ El manual de usuario esté completo
- ✅ El video explicativo cubra todos los aspectos
- ✅ No haya bugs críticos conocidos

**Criterios de evaluación del proyecto:**
- Funcionamiento: 6 puntos
- Documentación técnica (Video): 2 puntos
- Manual de usuario: 1 punto
- Diseño de la aplicación: 1 punto
- **Total: 10 puntos**

---

## 🎬 Guion para el Video Explicativo

### Estructura sugerida (10-15 minutos):

**Introducción (1 minuto):**
- Presentación del equipo
- Objetivo del proyecto
- Explicación breve de las tres fases de análisis

**Demostración del programa (3 minutos):**
- Mostrar la interfaz gráfica
- Cargar un archivo de ejemplo
- Ejecutar el análisis
- Mostrar resultados exitosos

**Demostración de detección de errores (3 minutos):**
- Error léxico
- Error sintáctico
- Error semántico
- Mostrar cómo se reportan

**Explicación del código (5-7 minutos):**
- Arquitectura general
- Analizador Léxico (Jordin explica)
- Analizador Sintáctico (Jordin explica)
- Analizador Semántico (Javier explica)
- Integración en la interfaz (Javier explica)

**Conclusión (1 minuto):**
- Resumen de lo aprendido
- Retos enfrentados
- Posibles mejoras futuras

---

## 📝 Plantilla para Commits

### Formato recomendado:

```
[Módulo] Descripción breve

Descripción más detallada si es necesario.

- Cambio 1
- Cambio 2
- Cambio 3
```

### Ejemplos:

```
[Parser] Implementado análisis de declaración de variables

Se agregó el método _declaracion_variable() que maneja la sintaxis:
TIPO IDENTIFICADOR = EXPRESION;

- Validación de tipos de datos válidos
- Generación de nodo AST correspondiente
- Detección de errores de sintaxis
```

```
[Semántico] Agregada verificación de tipos en asignaciones

Implementada la función que verifica que el tipo de la expresión
sea compatible con el tipo de la variable.

- Soporte para conversión implícita entero->decimal
- Mensajes de error descriptivos
- Pruebas con casos_semanticos.txt
```

---

## 🔧 Herramientas Recomendadas

### Para desarrollo:
- **Editor:** VS Code, PyCharm, o Sublime Text
- **Python:** Versión 3.8 o superior recomendada
- **Git:** Para control de versiones
- **GitHub Desktop:** Si prefieren interfaz gráfica para Git

### Para debugging:
- **Python Debugger:** Usar `pdb` o el debugger del IDE
- **Print statements:** Para debugging rápido
- **Logging:** Para debugging más profesional

### Para el video:
- **OBS Studio:** Grabar pantalla (gratis)
- **Loom:** Alternativa online simple
- **Camtasia:** Para edición profesional
- **Audacity:** Para editar audio si es necesario

---

## 💡 Ideas de Mejoras Opcionales

Si terminan antes de tiempo y quieren agregar valor extra:

### Mejoras de interfaz:
1. Syntax highlighting en el editor de código
2. Numeración de líneas en el editor
3. Resaltar la línea con error en el código
4. Modo oscuro / claro
5. Exportar resultados a PDF o HTML

### Mejoras funcionales:
1. Guardar y cargar proyectos
2. Historial de análisis
3. Sugerencias de corrección para errores comunes
4. Estadísticas del código (complejidad, etc.)
5. Visualización gráfica del AST

### Mejoras técnicas:
1. Soporte para comentarios de varias líneas
2. Mejor manejo de errores múltiples
3. Recuperación de errores (continuar después de un error)
4. Optimización del rendimiento
5. Tests automatizados más completos

**Nota:** Estas son opcionales. Enfóquense primero en cumplir todos los requisitos básicos.

---

## 📚 Glosario de Términos

- **Token:** Unidad léxica básica (palabra reservada, identificador, operador, etc.)
- **AST:** Árbol de Sintaxis Abstracta, representa la estructura del programa
- **Parser:** Analizador sintáctico
- **Gramática:** Conjunto de reglas que definen la sintaxis del lenguaje
- **Tabla de Símbolos:** Estructura que almacena información sobre identificadores
- **Ámbito (Scope):** Región del código donde un identificador es válido
- **Tipo de dato:** Clasificación de valores (entero, decimal, cadena, booleano)
- **Análisis léxico:** Primera fase, identifica tokens
- **Análisis sintáctico:** Segunda fase, verifica estructura
- **Análisis semántico:** Tercera fase, verifica coherencia
- **Nodo:** Elemento del AST
- **Expresión:** Combinación de valores y operadores que produce un resultado
- **Declaración:** Instrucción que define una variable o función

---

## 🎯 Checklist Final Antes de Entregar

### Código:
- [ ] Todo el código está comentado apropiadamente
- [ ] No hay código comentado (código muerto)
- [ ] No hay `print()` de debugging olvidados
- [ ] Todos los archivos tienen la estructura correcta
- [ ] El código sigue convenciones de Python (PEP 8)

### Funcionalidad:
- [ ] Análisis léxico funciona correctamente
- [ ] Análisis sintáctico funciona correctamente
- [ ] Análisis semántico funciona correctamente
- [ ] La interfaz gráfica es intuitiva
- [ ] Todos los botones funcionan
- [ ] Los mensajes de error son claros

### Pruebas:
- [ ] casos_positivos.txt pasa sin errores
- [ ] casos_negativos.txt detecta errores léxicos
- [ ] casos_sintacticos.txt detecta errores sintácticos
- [ ] casos_semanticos.txt detecta errores semánticos
- [ ] programa_completo.txt pasa todos los análisis

### Documentación:
- [ ] Manual de usuario completado y actualizado
- [ ] Documentación técnica lista
- [ ] README.md actualizado
- [ ] Comentarios en el código claros y útiles

### Video:
- [ ] Video explicativo grabado
- [ ] Audio claro y sin ruido
- [ ] Demuestra todas las funcionalidades
- [ ] Explica el código adecuadamente
- [ ] Duración apropiada (10-15 minutos)

### Entrega:
- [ ] Repositorio de GitHub actualizado
- [ ] Todos los archivos incluidos
- [ ] .gitignore configurado correctamente
- [ ] Video subido y enlace incluido
- [ ] Fecha de entrega: 30 de Octubre

---

## 🎉 Conclusión

Este plan divide el trabajo equitativamente entre Jordin y Javier:

**Jordin (50%):** Se enfoca en el análisis sintáctico, implementando el parser, generando el AST y detectando errores estructurales.

**Javier (50%):** Se enfoca en el análisis semántico, implementando la tabla de símbolos, verificación de tipos, y completando la integración con mejoras en la interfaz.

Ambos componentes son igual de importantes y complejos. La coordinación entre ustedes será clave para el éxito del proyecto.

**¡Mucho éxito con el proyecto!** 🚀

---

## 📞 Información de Contacto

**Jordin:** [Tu información de contacto]
**Javier:** [Información de contacto de Javier]

**Repositorio:** [URL del repositorio en GitHub]

**Fecha límite:** 30 de Octubre de 2024

---

*Última actualización: Septiembre 2025*
*Versión del plan: 1.0*