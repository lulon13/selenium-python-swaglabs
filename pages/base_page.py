"""Clase base del Page Object Model: esperas y acciones comunes."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.TIMEOUT)

    def abrir(self, ruta=""):
        self.driver.get(f"{config.BASE_URL}/{ruta}")
        return self

    def encontrar(self, localizador):
        return self.wait.until(EC.visibility_of_element_located(localizador))

    def clic(self, localizador):
        self.wait.until(EC.element_to_be_clickable(localizador)).click()

    def escribir(self, localizador, texto):
        campo = self.encontrar(localizador)
        campo.clear()
        campo.send_keys(texto)

    def texto(self, localizador):
        return self.encontrar(localizador).text
