from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITULO = (By.CSS_SELECTOR, "[data-test='title']")
    PRODUCTOS = (By.CLASS_NAME, "inventory_item")
    INSIGNIA = (By.CLASS_NAME, "shopping_cart_badge")
    CARRITO = (By.CLASS_NAME, "shopping_cart_link")

    def cargada(self):
        self.wait.until(EC.url_contains("inventory.html"))
        return self.texto(self.TITULO) == "Products"

    def agregar(self, slug):
        self.clic((By.ID, f"add-to-cart-{slug}"))
        return self

    def cantidad_en_carrito(self):
        badges = self.driver.find_elements(*self.INSIGNIA)
        return int(badges[0].text) if badges else 0

    def ir_al_carrito(self):
        from pages.cart_page import CartPage
        self.clic(self.CARRITO)
        return CartPage(self.driver)
