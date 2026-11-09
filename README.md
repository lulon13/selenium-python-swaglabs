# Automatización de pruebas con Selenium WebDriver y Python · Swag Labs

**Asignatura:** TI3-312 Aseguramiento de la Calidad del Software (UNIBE)
**Estudiante:** Bryan José Peguero Camilo · 25-1585
**Actividad:** Explorando las capacidades de automatización de pruebas con Selenium en Python

Pruebas automatizadas sobre [Swag Labs](https://www.saucedemo.com) con Selenium 4, pytest y el patrón Page Object Model. Cada archivo de `tests/` corresponde a un tema de la actividad.

| Tema | Archivo |
|---|---|
| Primeros pasos: abrir/cerrar el navegador, `find_element`, `click`, `send_keys` | `ejemplos/abrir_y_cerrar.py`, `tests/test_01_primeros_pasos.py` |
| Identificación de elementos (ID, NAME, CLASS_NAME, TAG_NAME, CSS, XPath, LINK_TEXT) | `tests/test_02_localizadores.py` |
| Esperas implícitas, explícitas y fluidas | `tests/test_03_esperas.py` |
| Elementos dinámicos | `tests/test_04_dinamicos.py` |
| Ventanas, pestañas, alertas y frames | `tests/test_05_ventanas_frames.py` |
| Cookies, JavaScript, ActionChains y capturas | `tests/test_06_avanzado.py` |
| Page Object Model | `pages/`, `tests/test_07_pom.py` |
| Varios navegadores | `conftest.py` (`--browser`), `utils/driver_factory.py` |
| Informes y registro | `pytest.ini`, `utils/listener.py`, `conftest.py` |

## Configuración del entorno

1. Instalar **Python 3.10+** (python.org) y al menos un navegador: Google Chrome y/o Mozilla Firefox.
2. Crear y activar un entorno virtual:

```bash
python -m venv .venv
# Windows:        .venv\Scripts\activate
# macOS / Linux:  source .venv/bin/activate
```

3. Instalar las dependencias (Selenium, pytest, pytest-html y allure-pytest):

```bash
pip install -r requirements.txt
```

No hace falta descargar ChromeDriver ni GeckoDriver: **Selenium Manager** (incluido desde Selenium 4.6) detecta el navegador y descarga el driver correcto la primera vez. Si se prefiere usar drivers propios, se indican con las variables `CHROMEDRIVER`, `GECKODRIVER`, `CHROME_BIN` o `FIREFOX_BIN`.

## Ejecución

```bash
pytest                                        # todas las pruebas en Chrome
pytest --browser=firefox                      # en Firefox
pytest --browser=chrome --browser=firefox     # las mismas pruebas en los dos navegadores
pytest --headless                             # sin ventana visible (por ejemplo, en CI)
pytest tests/test_03_esperas.py               # un solo tema
pytest -m humo                                # solo las pruebas marcadas como humo
```

Variables opcionales:

- `BASE_URL`: URL de la aplicación (por defecto `https://www.saucedemo.com`).
- `SEL_PAUSA`: segundos de pausa después de cada acción, para ver la prueba con calma.
- `SEL_VENTANA="x,y,ancho,alto"`: posición y tamaño de la ventana del navegador.

## Informes y registro

Cada ejecución genera en `reportes/`:

- `reporte.html`: informe de **pytest-html** con el resultado de cada prueba y su captura de pantalla.
- `allure-results/`: datos para **Allure**. El informe se genera con `allure serve reportes/allure-results` (requiere la línea de comandos de Allure, por ejemplo `npm install -g allure-commandline`).
- `ejecucion.log`: registro detallado de cada acción de WebDriver (navegación, clics, texto escrito), producido por el `RegistroListener` de `utils/listener.py`.
- `capturas/`: una captura por prueba.

Resultado de referencia: **48 passed** (24 pruebas × Chrome y Firefox).
