"""4. Interacción con elementos dinámicos (aparecen, cambian o se recrean)."""
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

import config
from pages.login_page import LoginPage


def test_insignia_del_carrito_aparece_y_desaparece(driver):
    LoginPage(driver).abrir().iniciar_sesion(config.USUARIO, config.CLAVE).cargada()
    espera = WebDriverWait(driver, config.TIMEOUT)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    insignia = espera.until(EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    assert insignia.text == "1"
    # El botón cambia: "Add to cart" se reemplaza por "Remove"
    quitar = espera.until(EC.element_to_be_clickable((By.ID, "remove-sauce-labs-backpack")))
    assert quitar.text == "Remove"
    quitar.click()
    # La insignia desaparece del DOM
    espera.until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))


def test_lista_reordenada_y_elementos_obsoletos(driver):
    LoginPage(driver).abrir().iniciar_sesion(config.USUARIO, config.CLAVE).cargada()
    primero = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    Select(driver.find_element(By.CLASS_NAME, "product_sort_container")).select_by_value("hilo")
    # Al reordenar, React vuelve a dibujar la lista: la referencia vieja puede quedar obsoleta.
    try:
        primero.text
    except StaleElementReferenceException:
        print("Referencia obsoleta: se vuelve a localizar el elemento")
    precios = [float(p.text[1:]) for p in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
    assert precios == sorted(precios, reverse=True)


def test_mensaje_de_error_dinamico(driver):
    pagina = LoginPage(driver).abrir()
    pagina.iniciar_sesion(config.USUARIO_BLOQUEADO, config.CLAVE)
    assert "locked out" in pagina.mensaje_error()
    driver.find_element(By.CSS_SELECTOR, "[data-test='error-button']").click()
    WebDriverWait(driver, config.TIMEOUT).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
