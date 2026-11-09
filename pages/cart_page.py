from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from pages.checkout_page import CheckoutPage


class CartPage(BasePage):
    NOMBRES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT = (By.ID, "checkout")

    def productos(self):
        self.encontrar(self.CHECKOUT)
        return [e.text for e in self.driver.find_elements(*self.NOMBRES)]

    def pagar(self):
        self.clic(self.CHECKOUT)
        return CheckoutPage(self.driver)
