"""5. Manejo de ventanas, pestañas, alertas y frames."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


def test_cambiar_entre_ventanas(driver):
    driver.get(config.BASE_URL)
    original = driver.current_window_handle
    # Abrimos una pestaña nueva (igual que un enlace con target="_blank")
    driver.execute_script("window.open(arguments[0], '_blank');", f"{config.BASE_URL}/frames/iframe.html")
    WebDriverWait(driver, config.TIMEOUT).until(EC.number_of_windows_to_be(2))
    nueva = [h for h in driver.window_handles if h != original][0]
    driver.switch_to.window(nueva)
    assert driver.title == "Merchant Detail Page"
    driver.close()                                   # cierra solo la pestaña actual
    driver.switch_to.window(original)
    assert driver.title == "Swag Labs"


def test_nueva_ventana_con_switch_to(driver):
    driver.get(config.BASE_URL)
    driver.switch_to.new_window("window")            # Selenium 4: abre y cambia a la ventana nueva
    driver.get(f"{config.BASE_URL}/frames/iframe.html")
    assert len(driver.window_handles) == 2


def test_alertas_emergentes(driver):
    driver.get(config.BASE_URL)
    driver.execute_script("setTimeout(() => alert('Pedido confirmado'), 500);")
    alerta = WebDriverWait(driver, config.TIMEOUT).until(EC.alert_is_present())
    assert alerta.text == "Pedido confirmado"
    alerta.accept()
    driver.execute_script("setTimeout(() => window.r = confirm('¿Vaciar carrito?'), 100);")
    WebDriverWait(driver, config.TIMEOUT).until(EC.alert_is_present()).dismiss()
    assert driver.execute_script("return window.r") is False


def test_frames_anidados(driver):
    driver.get(f"{config.BASE_URL}/frames/iframe.html")
    driver.switch_to.frame("contentFrame")                       # por nombre
    driver.switch_to.frame(driver.find_element(By.ID, "header"))  # por elemento
    assert driver.find_element(By.TAG_NAME, "h1").text == "Welcome to My Website"
    driver.switch_to.parent_frame()                              # sube un nivel
    driver.switch_to.frame("mainFrame")
    assert driver.find_element(By.TAG_NAME, "h1").text == "Merchant Detail"
    driver.switch_to.default_content()                           # vuelve a la página principal
    assert driver.title == "Merchant Detail Page"
