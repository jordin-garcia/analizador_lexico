# Analizador Léxico, Sintáctico y Semántico

Frontend completo de compilador para un lenguaje académico sencillo. Está desarrollado en Python y ofrece una interfaz gráfica moderna basada en `tkinter` para ejecutar, visualizar y depurar las tres fases clásicas de análisis.

## 📋 Descripción general

El proyecto encapsula:

- **Análisis léxico**: tokeniza el código; detecta comentarios y cadenas sin cerrar, caracteres inválidos y clasifica palabras reservadas, identificadores, números, operadores y delimitadores.
- **Análisis sintáctico**: parser descendente recursivo que construye un AST y valida la gramática (declaraciones, funciones, estructuras de control, expresiones con precedencia, bloques).
- **Análisis semántico**: recorre el AST, mantiene tabla de símbolos y comprueba tipos, ámbitos, redeclaraciones, número mínimo de parámetros en funciones y operaciones incompatibles.
- **Interfaz gráfica**: editor con numeración de líneas, tablas para tokens, resumen estadístico y símbolos, mensajes de error detallados y utilidades para cargar/guardar limpiamente.

## ✨ Principales características

- Cadena de análisis completa en un clic; se detiene en la primera fase que detecta errores.
- Mensajes explicativos con línea y detalle tanto para errores léxicos como sintácticos y semánticos.
- Tabla de símbolos visual con tipo, categoría y ámbito.
- Resumen agrupado de tokens para facilitar reportes.
- Temática oscura, soporte de scroll sincronizado y contadores de línea en el editor.
- Archivos de prueba que ejercitan cada componente por separado y en conjunto.

## 🖥️ Requisitos

- Python 3.6 o superior.
- Sistema operativo: Windows, macOS o Linux.
- No requiere paquetes externos (solo biblioteca estándar).

## 🚀 Puesta en marcha

```bash
git clone <url-del-repositorio>
cd analizador_lexico
python src/main.py
```

La ventana principal se abrirá inmediatamente.

## 📖 Uso rápido

1. Ejecuta `python src/main.py`.
2. Escribe código en el editor o pulsa **Cargar Archivo (.txt)** para importar un archivo.
3. Haz clic en **Analizar Código**.
4. Revisa los resultados:
   - Tabla superior: tokens o errores (según el resultado de la fase actual).
   - Tabla intermedia: resumen de tokens (solo si las tres fases son exitosas).
   - Tabla inferior: tabla de símbolos (solo en análisis exitoso).
5. Usa **Guardar Documento** para exportar el código, y **Limpiar** para reiniciar el entorno.

## 📁 Estructura del repositorio

```
analizador_lexico/
├── src/
│   ├── main.py
│   ├── analizador_lexico.py
│   ├── analizador_sintactico.py
│   ├── analizador_semantico.py
│   └── interfaz_grafica.py
├── tests/
│   ├── casos_lexicos.txt
│   ├── casos_sintacticos.txt
│   ├── casos_semanticos.txt
│   ├── casos_mixtos.txt
│   └── programa_correcto.txt
├── docs/
│   ├── manual_de_usuario.md
│   └── documentacion_tecnica.md
├── plan_desarrollo_analizador.md
└── README.md
```

## 🧪 Archivos de prueba incluidos

| Archivo | Objetivo | Resultado esperado |
|---------|----------|--------------------|
| `casos_lexicos.txt` | Escenarios que el lexer debe rechazar (cadenas/comentarios sin cerrar, caracteres ilegales) | Error en fase léxica |
| `casos_sintacticos.txt` | Programas léxicamente válidos con fallos gramaticales | Error en fase sintáctica |
| `casos_semanticos.txt` | Programas que violan reglas de tipos o ámbitos | Error en fase semántica |
| `casos_mixtos.txt` | Mezcla de casos correctos e incorrectos en las tres fases | El análisis se detiene según el primer error encontrado en cada fragmento |
| `programa_correcto.txt` | Programa completo válido | Éxito en las tres fases |

## 🔤 Lenguaje soportado

- **Palabras reservadas**: `entero`, `decimal`, `booleano`, `cadena`, `si`, `sino`, `mientras`, `hacer`, `verdadero`, `falso`.
- **Identificadores**: letra o `_` inicial seguida de letras/dígitos/`_` (solo ASCII, sin tildes ni caracteres especiales).
- **Números**: enteros (`123`) y decimales (`3.14`).
- **Cadenas**: entre comillas simples o dobles con soporte de caracteres escapados.
- **Operadores**: `+`, `-`, `*`, `/`, `%`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`.
- **Delimitadores**: `(` `)` `{` `}` `;` `,` `.`
- **Comentarios**: de línea `//` y de bloque `/* ... */`.

Restricciones relevantes:

- Las funciones deben declararse con al menos dos parámetros.
- Se permite conversión implícita de `entero` a `decimal`; otros cruces de tipos generan error semántico.
- Los casos como `entero 9variable = 10;` o `decimal x = 12.3.4;` son detectados en la fase sintáctica tras tokenizarse correctamente.

## 📚 Documentación adicional

- [`docs/manual_de_usuario.md`](docs/manual_de_usuario.md): guía paso a paso para la interfaz.
- [`docs/documentacion_tecnica.md`](docs/documentacion_tecnica.md): arquitectura interna y detalles de implementación.
- [`plan_desarrollo_analizador.md`](plan_desarrollo_analizador.md): plan de trabajo y bitácora.

## 🐛 Solución de problemas

- **La ventana no abre**: asegúrate de ejecutar el comando desde la carpeta raíz y que tu instalación de Python incluya `tkinter`.
- **Errores al cargar archivos**: utiliza archivos `.txt` codificados en UTF-8; la aplicación intenta Latin-1 como alternativa.
- **No veo errores sintácticos/semánticos**: corrige primero cualquier error léxico; el pipeline se detiene en la primera fase fallida.
- **La interfaz parece congelada**: evita ejecutar nuevamente “Analizar Código” hasta que termine el análisis activo; usa “Limpiar” antes de volver a probar.

## 👥 Créditos

- **Jordin** – Analizador sintáctico.
- **Javier** – Analizador semántico e integración general.

## 📝 Licencia y versión

Proyecto académico para la Universidad Rafael Landívar, curso Lenguajes Formales y Autómatas.

- **Versión vigente**: 2.1 (noviembre 2025) – Incluye interfaz con análisis completo y manual actualizado.
- Historial:
  - 2.0 (octubre 2024): incorporación de análisis sintáctico y semántico.
  - 1.0 (septiembre 2024): prototipo de análisis léxico.

---

Universidad Rafael Landívar · Lenguajes Formales y Autómatas
