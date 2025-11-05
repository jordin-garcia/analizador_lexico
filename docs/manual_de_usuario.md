# Manual de Usuario · Analizador Léxico, Sintáctico y Semántico

## 1. Introducción

Esta aplicación permite estudiar un lenguaje de programación académico a través de las tres fases clásicas del front-end de un compilador:

1. **Análisis Léxico**: transforma el texto en una secuencia de tokens.
2. **Análisis Sintáctico**: verifica que la secuencia de tokens respete la gramática del lenguaje y construye un Árbol de Sintaxis Abstracta (AST).
3. **Análisis Semántico**: valida reglas de significado (tipos, ámbitos, redeclaraciones, etc.) sobre el AST.

El flujo es completamente automatizado desde una interfaz gráfica: al presionar “Analizar Código” la aplicación ejecuta cada fase en orden y detiene el proceso en cuanto se detecta un error, mostrando información detallada al usuario.

## 2. Requisitos del Sistema

- **Sistema operativo**: Windows, macOS o Linux.
- **Python**: versión 3.6 o posterior.
- **Dependencias**: únicamente la biblioteca estándar de Python (`tkinter`), ya incluida en instalaciones oficiales.

## 3. Instalación y Ejecución

1. Asegúrate de tener Python instalado y disponible en la variable de entorno `PATH`.
2. Descarga o clona el repositorio del proyecto.
3. Abre una terminal y sitúate en la carpeta raíz `analizador_lexico`.
4. Ejecuta:
   ```bash
   python src/main.py
   ```
5. Se abrirá la ventana principal con la interfaz gráfica.

## 4. Guía de Uso de la Interfaz Gráfica

La ventana está dividida en tres zonas: barra de botones, editor de código (izquierda) y área de resultados (derecha). Los widgets utilizan un tema oscuro para mejorar la legibilidad.

### 4.1 Barra de botones

- **Cargar Archivo (.txt)**: abre un diálogo para seleccionar archivos de texto. El contenido se carga en el editor usando UTF-8; si falla, se intenta con Latin-1.
- **Analizar Código**: lanza la cadena de análisis. Si existe algún error en una etapa, se interrumpe el proceso y el error se muestra en la tabla principal con su línea.
- **Limpiar**: borra el contenido del editor y vacía todas las tablas de resultados, restaurando los encabezados predeterminados.
- **Guardar Documento**: exporta el contenido del editor a un archivo `.txt` elegido por el usuario.

### 4.2 Editor de código fuente

- Editor multilinea con fuente monoespaciada y numeración de líneas sincronizada.
- Permite escribir o pegar código directamente.
- Cuenta con desplazamiento horizontal y vertical independiente.

### 4.3 Área de resultados

Se compone de tres `Treeview` (tablas):

1. **Tokens y Errores**
   - En análisis exitoso muestra todos los tokens en orden (tipo, lexema y línea).
   - En caso de error, los encabezados cambian dinámicamente para listar tipo de error, detalle y línea.
2. **Resumen de Tokens**
   - Solo se rellena si las tres fases se completan sin errores.
   - Agrupa tokens por categoría de alto nivel (Operador, Signo, Identificador, etc.) y muestra la cantidad de apariciones de cada lexema.
3. **Tabla de Símbolos**
   - Disponible únicamente tras un análisis exitoso.
   - Incluye nombre, tipo, categoría (variable, función, parámetro), ámbito y línea de declaración.

Al finalizar un análisis sin errores se muestra un cuadro de diálogo confirmando el éxito de las tres fases.

## 5. Descripción de las Fases de Análisis

### 5.1 Análisis Léxico

- Reconoce comentarios (`//`, `/* ... */`), números enteros y decimales, cadenas entre comillas simples o dobles, identificadores (letra o guion bajo inicial seguido de letras/dígitos/guion bajo), operadores (`+`, `-`, `*`, `/`, `%`, `==`, `!=`, `<=`, `>=`, `<`, `>`), delimitadores (`(`, `)`, `{`, `}`, `;`, `,`, `.`) y espacios en blanco.
- Detecta previamente comentarios de bloque y cadenas sin cerrar y reporta un error específico si faltan los delimitadores de cierre.
- Cualquier carácter fuera del conjunto aceptado (ej. `@`, `#`, letras con tilde, emojis) genera un token `ERROR` con el detalle “Token inesperado”.
- Algunos patrones aparentemente “léxicos” (como `entero 9variable = 10;` o `decimal x = 12.3.4;`) se fraccionan en tokens válidos, por lo que su invalidación ocurre en la fase sintáctica. Este comportamiento es intencional y mantiene simple la especificación léxica.

**Ejemplo de error léxico:**
```
entero valor@ = 10;   // '@' no pertenece al alfabeto del lenguaje
```

### 5.2 Análisis Sintáctico

- Implementa un parser descendente recursivo que construye un AST.
- Reglas cubiertas: declaraciones de variables (`TIPO id = expresión;`), funciones (`TIPO id ( parámetros ) { bloque }`), estructuras `si/sino`, `mientras`, `hacer ... mientras`, asignaciones y expresiones con precedencia (`+/-` sobre `*//%`).
- Reporta errores con línea y detalle, por ejemplo: falta de `;`, llaves o paréntesis, tipos no reconocidos, operadores duplicados, comparadores inválidos (`===`), funciones con formato incorrecto o bloques sin cerrar.

**Ejemplo de error sintáctico:**
```
entero x = 10        // Falta ';'
si (x > 5 {          // Falta ')'
decimal y = 12.3.4;  // El parser detecta un '.' en posición inesperada
```

### 5.3 Análisis Semántico

- Recorre el AST con una tabla de símbolos y maneja ámbitos anidados para funciones.
- Validaciones principales:
  - Tipos declarados válidos (`entero`, `decimal`, `cadena`, `booleano`).
  - Variables no redeclaradas en el mismo ámbito y no utilizadas sin declarar.
  - Asignaciones con tipos compatibles (permite conversión implícita de `entero` a `decimal`).
  - Operaciones binarias compatibles según una matriz de tipos (suma, resta, multiplicación, división, módulo, concatenación de cadenas).
  - Funciones con mínimo dos parámetros, sin nombres duplicados y sin redeclaraciones.
  - Comparaciones con tipos compatibles (más la excepción entero/decimal).

**Ejemplo de error semántico:**
```
entero numero = 10;
cadena texto = "hola";
entero resultado = numero + texto;  // Tipos incompatibles en la operación
```

## 6. Archivos de Prueba

Dentro de `tests/` se incluyen casos preparados para ejercitar cada fase:

- `casos_lexicos.txt`: únicamente ejemplos que el analizador léxico rechaza (cadenas/comentarios sin cerrar, caracteres ilegales).
- `casos_sintacticos.txt`: combinaciones que pasan la fase léxica pero violan reglas gramaticales.
- `casos_semanticos.txt`: programas que superan léxico y sintaxis pero incumplen reglas semánticas.
- `casos_mixtos.txt`: mezcla de fragmentos correctos y errores distribuidos en las tres fases para comprobar el flujo completo.

**Pasos sugeridos para probar:**

1. Inicia la aplicación (`python src/main.py`).
2. Pulsa **Cargar Archivo** y selecciona uno de los archivos anteriores.
3. Presiona **Analizar Código**.
4. Observa los resultados: si se encuentra un error, solo la tabla superior mostrará la descripción; si todo es correcto, verás tokens, resumen y tabla de símbolos.

## 7. Lenguaje Soportado

### 7.1 Tokens y alfabeto

- **Palabras reservadas**: `entero`, `decimal`, `booleano`, `cadena`, `si`, `sino`, `mientras`, `hacer`, `verdadero`, `falso`.
- **Identificadores**: deben iniciar con letra (A-Z, a-z) o guion bajo `_` y continuar con letras, dígitos o guion bajo. Caracteres acentuados o especiales no están permitidos.
- **Números**: `NUMERO_ENTERO` (`0`, `42`, `123`) y `NUMERO_DECIMAL` (`3.14`, `0.5`).
- **Cadenas**: entre `'` o `"`, admiten secuencias escapadas (`\"`, `\\`, etc.).
- **Operadores**: `+ - * / % = == != < > <= >=`.
- **Delimitadores**: `(` `)` `{` `}` `;` `,` `.`
- **Comentarios**: `//` hasta el fin de la línea y `/* ... */` multilínea.
- Caracteres fuera de este conjunto generan `ERROR` léxico.

### 7.2 Declaraciones y estructuras

```
entero edad = 25;
decimal precio = 99.99;
cadena nombre = "Juan";
booleano activo = verdadero;

entero sumar(entero a, entero b) {
    entero resultado = a + b;
}

si (edad >= 18) {
    activo = verdadero;
} sino {
    activo = falso;
}

mientras (contador < 100) {
    contador = contador + 1;
}

hacer {
    contador = contador - 1;
} mientras (contador > 0)
```

### 7.3 Compatibilidad de tipos (resumen)

| Operación | Tipos compatibles | Resultado |
|-----------|-------------------|-----------|
| `+`, `-`, `*`, `/`, `%` | `entero` ↔ `entero` | `entero` |
| `+`, `-`, `*`, `/` | `decimal` ↔ `decimal` | `decimal` |
| `+`, `-`, `*`, `/` | `entero` ↔ `decimal` | `decimal` |
| `+` | `cadena` ↔ `cadena` | `cadena` (concatenación) |

- La asignación permite `decimal variable = entero_expr;` como conversión implícita.
- No se permiten otras conversiones ni operaciones mixtas (ej. `entero + cadena`).
- Las comparaciones requieren tipos compatibles; se admite `entero` con `decimal`.

## 8. Solución de Problemas

- **La ventana no abre**: confirma que estás ejecutando `python src/main.py` desde la carpeta del proyecto y que tu instalación de Python incluye `tkinter`.
- **No puedo cargar un archivo**: verifica que sea `.txt` y que su codificación sea UTF-8 o Latin-1. El programa intenta ambas automáticamente.
- **Errores inesperados del analizador**:
  - Recuerda que el proceso se detiene en la primera fase con fallos. Si aparece un error léxico, corrígelo antes de esperar diagnósticos sintácticos o semánticos.
  - Revisa la línea reportada; la numeración del editor y de los mensajes coincide.
- **Resultados vacíos tras varios análisis**: utiliza el botón **Limpiar** para reiniciar la interfaz antes de una nueva prueba.

---

**Última actualización:** noviembre 2025  
**Versión:** 2.1 (GUI con análisis completo)
