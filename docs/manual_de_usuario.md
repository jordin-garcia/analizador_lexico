# Manual de Usuario: Analizador Léxico

## 1. Introducción

Este programa es una herramienta diseñada para procesar archivos de texto o código fuente escrito en un lenguaje de programación simple. Su función principal es realizar un **análisis léxico**, que consiste en descomponer el texto de entrada en una secuencia de componentes con significado propio, llamados **tokens**.

La aplicación cuenta con una interfaz gráfica intuitiva que permite cargar archivos, analizar su contenido y visualizar los resultados de forma clara y organizada, incluyendo la detección y reporte de errores léxicos.

## 2. Requisitos del Sistema

- **Sistema Operativo:** Windows, macOS o Linux.
- **Python:** Versión 3.6 o superior.
- **Librerías:** No se requieren librerías externas, ya que el programa utiliza la librería estándar de Python (`tkinter` para la interfaz gráfica).

## 3. Instalación y Ejecución

El programa no requiere un proceso de instalación formal. Solo necesitas tener Python instalado en tu sistema.

Para ejecutar la aplicación, sigue estos pasos:

1. Abre una terminal o línea de comandos.
2. Navega hasta el directorio raíz del proyecto (`analizador_lexico`).
3. Ejecuta el siguiente comando:
   ```bash
   python src/main.py
   ```
4. Al ejecutar el comando, se abrirá la ventana principal de la aplicación.

## 4. Guía de Uso de la Interfaz Gráfica

La interfaz se divide en tres áreas principales: la barra de botones, el editor de código fuente y el área de resultados.

![Imagen de la interfaz de usuario](https-placeholder-for-image.com) *(Nota: Esto es un marcador de posición para una imagen de la interfaz)*

### 4.1. Barra de Botones

En la parte superior de la ventana encontrarás tres botones principales:

- **Cargar Archivo (.txt):**

  - **Función:** Abre un explorador de archivos para que puedas seleccionar y cargar un archivo de texto (`.txt`).
  - **Uso:** Al hacer clic, selecciona un archivo. Su contenido se mostrará automáticamente en el área de "Código Fuente".
- **Analizar Código:**

  - **Función:** Inicia el análisis léxico del contenido que se encuentra en el editor de "Código Fuente".
  - **Uso:** Después de escribir o cargar tu código, haz clic en este botón para ver los resultados en las tablas de la derecha.
- **Limpiar:**

  - **Función:** Restablece la interfaz a su estado inicial.
  - **Uso:** Borra todo el texto del editor de "Código Fuente" y limpia las tablas de resultados.

### 4.2. Área de Código Fuente

Este es el cuadro de texto grande ubicado a la izquierda. Aquí puedes:

- Escribir código directamente.
- Pegar código desde el portapapeles.
- Ver el contenido de un archivo cargado con el botón "Cargar Archivo".

### 4.3. Área de Resultados

Ubicada a la derecha, esta área se divide en dos tablas que muestran la salida del análisis.

- **Tabla "Tokens y Errores" (Superior):**

  - **Si el análisis es exitoso:** Muestra una lista completa de todos los tokens encontrados en el orden en que aparecen. Las columnas son:
    - `Tipo`: La categoría del token (p. ej., `PALABRA_RESERVADA`, `IDENTIFICADOR`, `NUMERO_ENTERO`).
    - `Token`: El valor exacto del token (p. ej., `si`, `mi_variable`, `123`).
    - `Línea`: El número de línea donde se encontró el token.
  - **Si se encuentran errores:** La tabla cambia para mostrar **únicamente** los errores léxicos detectados. Las columnas son:
    - `Error`: Indica que el token es de tipo `ERROR`.
    - `Detalle`: Describe el error, mostrando el carácter o secuencia no reconocida.
    - `Línea`: El número de línea donde ocurrió el error.
- **Tabla "Resumen de Tokens" (Inferior):**

  - Esta tabla **solo se llena si el análisis es exitoso** (sin errores).
  - Muestra un resumen de cuántas veces aparece cada token en el código, agrupados por tipo. Las columnas son:
    - `Tipo`: La categoría general del token (`Palabra Reservada`, `Identificador`, `Operador`, etc.).
    - `Token`: El valor del token.
    - `Cantidad`: El número total de veces que ese token aparece en el código.

## 5. Cómo Probar el Analizador

Dentro de la carpeta `tests/` del proyecto, hemos incluido dos archivos para que puedas probar el funcionamiento del programa:

- `casos_positivos.txt`: Contiene código escrito correctamente según las reglas del lenguaje.
- `casos_negativos.txt`: Contiene código con varios errores léxicos intencionados.

### 5.1. Probar un Caso Exitoso

1. Ejecuta el programa.
2. Haz clic en **"Cargar Archivo"**.
3. Selecciona el archivo `tests/casos_positivos.txt`.
4. Haz clic en **"Analizar Código"**.
5. **Resultado esperado:**
   - La tabla "Tokens y Errores" se llenará con la lista completa de tokens reconocidos.
   - La tabla "Resumen de Tokens" mostrará el conteo de cada token.

### 5.2. Probar un Caso con Errores

1. Si es necesario, haz clic en **"Limpiar"** para borrar los resultados anteriores.
2. Haz clic en **"Cargar Archivo"**.
3. Selecciona el archivo `tests/casos_negativos.txt`.
4. Haz clic en **"Analizar Código"**.
5. **Resultado esperado:**
   - La tabla "Tokens y Errores" mostrará únicamente las líneas que contienen caracteres inválidos (p. ej., `@`, `$`, `~`, `?`, `#`).
   - La tabla "Resumen de Tokens" permanecerá vacía.

## 6. Lenguaje Soportado (Tokens Reconocidos)

El analizador está configurado para reconocer los siguientes tipos de tokens:

- **Palabras Reservadas:** `entero`, `decimal`, `booleano`, `cadena`, `si`, `sino`, `mientras`, `hacer`, `verdadero`, `falso`.
- **Identificadores:** Nombres de variables que comiencen con una letra o guion bajo, seguidos de letras, números o guiones bajos (p. ej., `mi_var`, `contador1`).
- **Números:** Enteros (`100`) y decimales (`3.14`).
- **Cadenas de Texto:** Texto entre comillas simples (`'hola'`) o dobles (`"mundo"`).
- **Operadores:**
  - Aritméticos: `+`, `-`, `*`, `/`, `%`
  - Asignación: `=`
  - Comparación: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Signos y Delimitadores:** `(`, `)`, `{`, `}`, `;`, `,`, `.`
- **Comentarios:**
  - De una línea: `// Esto es un comentario`
  - De múltiples líneas: `/* ... */`

Cualquier carácter o secuencia que no encaje en estas categorías será reportado como un **`ERROR`**.
