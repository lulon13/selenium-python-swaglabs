"""Crea el WebDriver del navegador pedido (Chrome, Firefox o Edge).

Selenium Manager (incluido desde Selenium 4.6) descarga el driver correcto
automáticamente. Si se definen las variables de entorno CHROMEDRIVER,
GECKODRIVER, CHROME_BIN o FIREFOX_BIN, se usan esas rutas en su lugar.
"""
import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.events import EventFiringWebDriver

from utils.listener import RegistroListener

log = logging.getLogger("driver")


def _ventana(driver):
    """Posición y tamaño de la ventana: SEL_VENTANA="x,y,ancho,alto" (útil para grabar)."""
    rect = os.getenv("SEL_VENTANA")
    if rect:
        x, y, w, h = map(int, rect.split(","))
        driver.set_window_rect(x=x, y=y, width=w, height=h)
    else:
        driver.set_window_size(1280, 900)


def crear_driver(navegador="chrome", headless=False):
    navegador = navegador.lower()
    if navegador == "chrome":
        opciones = webdriver.ChromeOptions()
        if headless:
            opciones.add_argument("--headless=new")
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")
        opciones.add_argument("--disable-search-engine-choice-screen")
        opciones.add_experimental_option("excludeSwitches", ["enable-automation"])
        opciones.add_experimental_option("prefs", {"credentials_enable_service": False,
                                                   "profile.password_manager_leak_detection": False})
        if os.getenv("CHROME_BIN"):
            opciones.binary_location = os.environ["CHROME_BIN"]
        servicio = ChromeService(os.getenv("CHROMEDRIVER")) if os.getenv("CHROMEDRIVER") else ChromeService()
        driver = webdriver.Chrome(options=opciones, service=servicio)

    elif navegador == "firefox":
        opciones = webdriver.FirefoxOptions()
        if headless:
            opciones.add_argument("-headless")
        if os.getenv("FIREFOX_BIN"):
            opciones.binary_location = os.environ["FIREFOX_BIN"]
        servicio = FirefoxService(os.getenv("GECKODRIVER")) if os.getenv("GECKODRIVER") else FirefoxService()
        driver = webdriver.Firefox(options=opciones, service=servicio)

    elif navegador == "edge":
        opciones = webdriver.EdgeOptions()
        if headless:
            opciones.add_argument("--headless=new")
        driver = webdriver.Edge(options=opciones, service=EdgeService())

    else:
        raise ValueError(f"Navegador no soportado: {navegador}")

    _ventana(driver)
    caps = driver.capabilities
    log.info("Navegador iniciado: %s %s", caps.get("browserName"), caps.get("browserVersion"))
    # Envolvemos el driver para registrar cada acción (ver utils/listener.py).
    return EventFiringWebDriver(driver, RegistroListener())
