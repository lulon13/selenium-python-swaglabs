"""1. Primeros pasos: abrir el navegador y usar las funciones básicas."""
from selenium.webdriver.common.by import By

import config


def test_abrir_pagina_y_leer_titulo(driver):
    driver.get(config.BASE_URL)
    assert driver.title == "Swag Labs"


def test_funciones_basicas_find_element_send_keys_click(driver):
    driver.get(config.BASE_URL)
    usuario = driver.find_element(By.ID, "user-name")        # find_element
    usuario.send_keys("texto de prueba")                       # send_keys
    usuario.clear()                                            # clear
    usuario.send_keys(config.USUARIO)
    driver.find_element(By.ID, "password").send_keys(config.CLAVE)
    boton = driver.find_element(By.ID, "login-button")
    assert boton.get_attribute("value") == "Login"            # get_attribute
    assert boton.is_displayed() and boton.is_enabled()         # estado del elemento
    boton.click()                                              # click
    titulo = driver.find_element(By.CLASS_NAME, "title")
    assert titulo.text == "Products"                           # .text
    assert "inventory.html" in driver.current_url
