"""2. Estrategias para identificar elementos (By.*)."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config

LOGIN = [
    ("ID", (By.ID, "user-name")),
    ("NAME", (By.NAME, "password")),
    ("CLASS_NAME", (By.CLASS_NAME, "submit-button")),
    ("TAG_NAME", (By.TAG_NAME, "form")),
    ("CSS_SELECTOR", (By.CSS_SELECTOR, "input[data-test='username']")),
    ("XPATH", (By.XPATH, "//input[@type='submit' and @value='Login']")),
]


@pytest.mark.parametrize("estrategia, localizador", LOGIN, ids=[e for e, _ in LOGIN])
def test_localizar_en_login(driver, estrategia, localizador):
    driver.get(config.BASE_URL)
    elemento = driver.find_element(*localizador)
    assert elemento.is_displayed()


def test_localizar_en_catalogo(driver):
    driver.get(config.BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys(config.USUARIO)
    driver.find_element(By.ID, "password").send_keys(config.CLAVE)
    driver.find_element(By.ID, "login-button").click()
    WebDriverWait(driver, config.TIMEOUT).until(EC.url_contains("inventory.html"))

    # find_elements devuelve una lista: los 6 productos
    assert len(driver.find_elements(By.CLASS_NAME, "inventory_item")) == 6
    # XPath relativo: el precio del producto cuyo nombre es "Sauce Labs Backpack"
    precio = driver.find_element(
        By.XPATH, "//div[text()='Sauce Labs Backpack']/ancestor::div[@class='inventory_item']"
                  "//div[@class='inventory_item_price']")
    assert precio.text == "$29.99"
    # CSS con atributo que empieza por...
    assert len(driver.find_elements(By.CSS_SELECTOR, "button[id^='add-to-cart']")) == 6
    # LINK_TEXT y PARTIAL_LINK_TEXT (enlaces del pie de página)
    assert driver.find_element(By.LINK_TEXT, "LinkedIn").get_attribute("href").startswith("https://www.linkedin.com")
    assert driver.find_element(By.PARTIAL_LINK_TEXT, "Face").is_displayed()
