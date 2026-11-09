"""6. Funciones avanzadas: cookies, JavaScript, acciones y capturas."""
import os

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


def test_cookies_de_sesion(driver):
    driver.get(config.BASE_URL)
    assert driver.get_cookie("session-username") is None
    # Crear la cookie de sesión permite entrar sin pasar por el formulario
    driver.add_cookie({"name": "session-username", "value": config.USUARIO})
    driver.get(f"{config.BASE_URL}/inventory.html")
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"
    # Borrar las cookies cierra la sesión
    driver.delete_all_cookies()
    driver.get(f"{config.BASE_URL}/inventory.html")
    WebDriverWait(driver, config.TIMEOUT).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))


def test_ejecutar_javascript(driver):
    driver.get(config.BASE_URL)
    driver.add_cookie({"name": "session-username", "value": config.USUARIO})
    driver.get(f"{config.BASE_URL}/inventory.html")
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    # Leer el carrito guardado por la aplicación en localStorage
    carrito = driver.execute_script("return JSON.parse(localStorage.getItem('cart-contents'))")
    assert carrito == [0]
    # Desplazarse hasta el pie de página y leer un valor calculado
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    assert driver.execute_script("return window.scrollY") > 0


def test_acciones_y_capturas(driver):
    driver.get(config.BASE_URL)
    usuario = driver.find_element(By.ID, "user-name")
    real = getattr(driver, "wrapped_driver", driver)
    # ActionChains: secuencias de teclado y ratón
    ActionChains(real).move_to_element(usuario).click().send_keys(config.USUARIO).perform()
    assert usuario.get_attribute("value") == config.USUARIO
    os.makedirs("reportes/capturas", exist_ok=True)
    usuario.screenshot("reportes/capturas/campo_usuario.png")     # captura de un solo elemento
