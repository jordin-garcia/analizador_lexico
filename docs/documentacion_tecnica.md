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
│  (analizador_lexico.py) │   Salida: Lista de tuplas (tipo, valor, línea)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Analizador Sintáctico  │ ← Verifica estructura
│  (analizador_sintactico │   Salida: AST (Árbol de Sintaxis Abstracta)
│         .py)            │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Analizador Semántico   │ ← Valida coherencia
│  (analizador_semantico  │   Salida: Tabla de símbolos + errores
│         .py)            │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Interfaz Gráfica       │ ← Muestra resultados
│  (interfaz_grafica.py)  │   Salida: Visualización en GUI
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
2. Recorre el código carácter por carácter usando `re.finditer()`
3. Genera una lista de tuplas (tipo_token, valor, línea)
4. Clasifica tokens especiales:
   - Identifica palabras reservadas
   - Distingue entre comentarios de línea y bloque
   - Diferencia números enteros y decimales
   - Reconoce cadenas con comillas simples y dobles

**Tokens reconocidos:**
- Comentarios (de línea y bloque)
- Números (enteros y decimales)
- Cadenas (simples y dobles)
- Identificadores y palabras reservadas
- Operadores (+, -, *, /, %, =, ==, !=, <, >, <=, >=)
- Delimitadores ((, ), {, }, ;, ,, .)

**Complejidad:** O(n) donde n es la longitud del código

**Manejo de errores:**
- Cualquier carácter no reconocido genera un token ERROR
- Los errores no detienen el análisis, se reportan todos

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
5. Valida requisitos específicos (ej: funciones con mínimo 2 parámetros)

**Gramática del Lenguaje:**

```
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

**Estructura del AST:**
```python
class NodoAST:
    tipo: str      # Tipo de nodo: 'PROGRAMA', 'DECLARACION_VARIABLE', etc.
    valor: Any     # Valor asociado (nombre de variable, operador, literal)
    hijos: List    # Nodos hijos
    linea: int     # Línea del código fuente
```

**Ejemplo de AST para `entero x = 10;`:**
```python
NodoAST(
    tipo='DECLARACION_VARIABLE',
    linea=1,
    hijos=[
        NodoAST(tipo='TIPO', valor='entero', linea=1),
        NodoAST(tipo='IDENTIFICADOR', valor='x', linea=1),
        NodoAST(tipo='NUMERO_ENTERO', valor='10', linea=1)
    ]
)
```

**Complejidad:** O(n) donde n es el número de tokens

**Manejo de errores:**
- Detecta errores de sintaxis específicos
- Reporta línea exacta del error
- Proporciona contexto del error
- Detiene el análisis al encontrar el primer error

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
5. Valida ámbitos (scope) de variables y funciones

**Tabla de Símbolos:**
```python
{
    "ambito:nombre": {
        "tipo": str,           # 'entero', 'decimal', 'cadena', 'booleano'
        "categoria": str,      # 'variable', 'funcion', 'parametro'
        "ambito": str,         # 'global' o nombre de función
        "linea": int          # Línea de declaración
    }
}
```

**Ejemplo:**
```python
{
    "global:x": {
        "tipo": "entero",
        "categoria": "variable",
        "ambito": "global",
        "linea": 1
    },
    "sumar:a": {
        "tipo": "entero",
        "categoria": "parametro",
        "ambito": "sumar",
        "linea": 5
    }
}
```

**Reglas Semánticas Implementadas:**

1. **Variables:**
   - Deben declararse antes de usarse
   - No pueden declararse dos veces en el mismo ámbito
   - El tipo de la expresión debe ser compatible con el tipo declarado

2. **Funciones:**
   - Deben tener mínimo 2 parámetros (requisito del proyecto)
   - No pueden declararse dos veces
   - Los parámetros deben tener nombres únicos

3. **Tipos:**
   - Las operaciones deben ser entre tipos compatibles
   - Las asignaciones deben respetar los tipos
   - Conversión implícita permitida: entero → decimal

**Matriz de Compatibilidad de Tipos:**
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

**Complejidad:** O(n) donde n es el número de nodos del AST

**Manejo de errores:**
- Detecta todos los errores semánticos (no se detiene en el primero)
- Reporta línea y contexto detallado
- Proporciona sugerencias cuando es posible

### 4. Interfaz Gráfica (`interfaz_grafica.py`)

**Responsabilidad:** Interacción con el usuario

**Componentes principales:**
- Editor de texto (ScrolledText)
- Tabla de tokens y errores (Treeview)
- Tabla de resumen (Treeview)
- Tabla de símbolos (Treeview)
- Botones de control (Cargar, Analizar, Limpiar)

**Flujo de ejecución:**
```
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
Mostrar éxito + tokens + resumen + tabla de símbolos
```

**Características de la interfaz:**
- Ventana de 1200x800 píxeles
- Diseño responsivo con grid layout
- Tres tablas con scrollbars independientes
- Manejo de excepciones con mensajes de error claros
- Soporte para codificación UTF-8 y Latin-1

## Decisiones de Diseño

### 1. Parser Descendente Recursivo

**Por qué:**
- Simplicidad de implementación
- Fácil de entender y mantener
- Correspondencia directa con la gramática
- Excelente para debugging
- Mensajes de error claros

**Alternativas consideradas:**
- Parser generado por herramientas (PLY, ANTLR): Más complejo para el alcance del proyecto
- Parser de tabla (LR): Más difícil de entender y debuggear

### 2. AST en vez de Parse Tree

**Por qué:**
- Elimina información innecesaria (paréntesis, punto y coma, etc.)
- Más eficiente en memoria
- Facilita el análisis semántico
- Más fácil de recorrer

**Qué se elimina:**
- Tokens de puntuación que ya cumplieron su función sintáctica
- Nodos intermedios que solo agrupan

**Qué se mantiene:**
- Estructura lógica del programa
- Información de tipos y operadores
- Números de línea para errores

### 3. Estructura de Tabla de Símbolos

**Por qué usar diccionario con clave "ambito:nombre":**
- Búsquedas O(1) muy eficientes
- Fácil separación de ámbitos
- No requiere estructuras de datos complejas
- Sencillo de implementar y entender

**Alternativas consideradas:**
- Árbol de ámbitos: Más complejo, innecesario para este lenguaje
- Listas anidadas: Búsquedas O(n), menos eficiente

### 4. Manejo de Ámbitos

**Estrategia implementada:**
- Ámbito global para variables y funciones de nivel superior
- Ámbito local por cada función
- Los parámetros viven en el ámbito de su función
- Búsqueda primero en ámbito local, luego global

**Simplificaciones:**
- No hay ámbitos anidados dentro de funciones
- Las estructuras de control no crean nuevos ámbitos
- No hay variables locales a bloques dentro de funciones

## Archivos de Prueba

### 1. `casos_positivos.txt`
- Propósito: Verificar tokens reconocidos correctamente
- Contenido: Código léxicamente válido
- Resultado esperado: Lista completa de tokens

### 2. `casos_negativos.txt`
- Propósito: Detectar errores léxicos
- Contenido: Caracteres inválidos (@, $, ?, etc.)
- Resultado esperado: Errores léxicos reportados

### 3. `casos_sintacticos.txt`
- Propósito: Verificar detección de errores sintácticos
- Contenido: 20 casos (correctos e incorrectos)
- Errores incluidos: Punto y coma faltante, paréntesis sin cerrar, funciones con 1 parámetro, etc.
- Resultado esperado: Errores sintácticos específicos reportados

### 4. `casos_semanticos.txt`
- Propósito: Verificar detección de errores semánticos
- Contenido: 20 casos (correctos e incorrectos)
- Errores incluidos: Variables no declaradas, tipos incompatibles, funciones duplicadas, etc.
- Resultado esperado: Errores semánticos específicos reportados

### 5. `programa_completo.txt`
- Propósito: Demostrar programa completo sin errores
- Contenido: Todas las características del lenguaje
- Secciones: Variables, funciones, estructuras de control, expresiones, comparaciones, anidamiento
- Resultado esperado: Análisis exitoso completo con tabla de símbolos poblada

## Posibles Mejoras Futuras

### Funcionalidades:
1. Soporte para llamadas a funciones
2. Arreglos y estructuras de datos
3. Más tipos de datos (carácter, etc.)
4. Operadores lógicos (&&, ||, !)
5. Estructuras de control adicionales (para, repetir-hasta)
6. Return statements
7. Alcance de bloque (block scope)

### Interfaz:
1. Syntax highlighting en el editor
2. Numeración de líneas
3. Resaltado de líneas con error
4. Modo oscuro / claro
5. Exportar resultados a PDF o HTML
6. Visualización gráfica del AST

### Técnicas:
1. Recuperación de errores (continuar después de un error)
2. Mejor manejo de errores múltiples
3. Optimización del rendimiento
4. Tests automatizados más completos
5. Generación de código intermedio
6. Optimizaciones del compilador

## Métricas del Proyecto

### Líneas de Código:
- `analizador_lexico.py`: ~168 líneas
- `analizador_sintactico.py`: ~650 líneas
- `analizador_semantico.py`: ~450 líneas
- `interfaz_grafica.py`: ~450 líneas
- **Total código fuente**: ~1718 líneas

### Archivos de Prueba:
- 5 archivos de prueba
- ~350 líneas de casos de prueba
- 55+ casos de prueba distintos

### Documentación:
- Manual de usuario: ~310 líneas
- Documentación técnica: Este documento
- README actualizado
- **Total documentación**: ~650+ líneas

### Complejidad del Parser:
- 15 métodos principales
- Soporta 4 tipos de datos
- Reconoce 3 estructuras de control
- Valida ~20 reglas semánticas

## Conclusión

Este proyecto implementa un compilador completo (frontend) para un lenguaje de programación simple. Las tres fases (léxica, sintáctica y semántica) trabajan en conjunto para proporcionar análisis exhaustivo del código fuente, detectando errores en cada nivel y proporcionando retroalimentación clara al usuario a través de una interfaz gráfica intuitiva.

---

**Autores:** Jordin y Javier  
**Fecha:** Octubre 2024  
**Versión:** 2.0

