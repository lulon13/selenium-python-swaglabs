"""3. Manejo de esperas: implícita, explícita y fluida."""
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import config


def _login(driver, usuario):
    driver.get(config.BASE_URL)
    driver.find_element(By.ID, "user-name").send_keys(usuario)
    driver.find_element(By.ID, "password").send_keys(config.CLAVE)
    driver.find_element(By.ID, "login-button").click()


def test_espera_implicita(driver):
    # Se aplica a TODOS los find_element: reintenta hasta 10 s antes de fallar.
    driver.implicitly_wait(10)
    _login(driver, config.USUARIO_LENTO)          # este usuario tarda ~5 s en entrar
    assert driver.find_element(By.CLASS_NAME, "inventory_list").is_displayed()
    driver.implicitly_wait(0)                       # se desactiva para no mezclarla con las explícitas


def test_espera_explicita_con_usuario_lento(driver):
    _login(driver, config.USUARIO_LENTO)
    inicio = time.time()
    # Espera explícita: una condición concreta, con un tiempo máximo.
    WebDriverWait(driver, 10).until(EC.url_contains("inventory.html"))
    lista = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list")))
    print(f"El catálogo apareció tras {time.time() - inicio:.1f} s")
    assert lista.is_displayed()


def test_espera_fluida_con_sondeo(driver):
    _login(driver, config.USUARIO_LENTO)
    espera = WebDriverWait(driver, timeout=10, poll_frequency=0.5,
                           ignored_exceptions=[NoSuchElementException])
    titulo = espera.until(lambda d: d.find_element(By.CLASS_NAME, "title"))
    assert titulo.text == "Products"
