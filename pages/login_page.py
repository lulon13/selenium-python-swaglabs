from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    USUARIO = (By.ID, "user-name")
    CLAVE = (By.ID, "password")
    BOTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def iniciar_sesion(self, usuario, clave):
        self.escribir(self.USUARIO, usuario)
        self.escribir(self.CLAVE, clave)
        self.clic(self.BOTON)
        return InventoryPage(self.driver)

    def mensaje_error(self):
        return self.texto(self.ERROR)
