"""Ejemplo mínimo: abrir y cerrar un navegador con Selenium WebDriver."""
from selenium import webdriver

driver = webdriver.Chrome()            # Selenium Manager descarga el driver si hace falta
driver.get("https://www.saucedemo.com")
print("Título:", driver.title)
driver.quit()                          # cierra todas las ventanas y termina el driver
