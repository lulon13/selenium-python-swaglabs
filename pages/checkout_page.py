from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    NOMBRE = (By.ID, "first-name")
    APELLIDO = (By.ID, "last-name")
    POSTAL = (By.ID, "postal-code")
    CONTINUAR = (By.ID, "continue")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINALIZAR = (By.ID, "finish")
    CONFIRMACION = (By.CLASS_NAME, "complete-header")

    def llenar_datos(self, nombre, apellido, postal):
        self.escribir(self.NOMBRE, nombre)
        self.escribir(self.APELLIDO, apellido)
        self.escribir(self.POSTAL, postal)
        self.clic(self.CONTINUAR)
        return self

    def total(self):
        return self.texto(self.TOTAL)

    def finalizar(self):
        self.clic(self.FINALIZAR)
        return self.texto(self.CONFIRMACION)
