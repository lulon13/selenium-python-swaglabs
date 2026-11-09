"""Registro (logging) de cada acción de WebDriver con un AbstractEventListener.

Si se define SEL_PAUSA (segundos), se hace una pausa después de cada acción:
sirve para ver la prueba con calma en una demostración o en un video.
"""
import logging
import os
import time

from selenium.webdriver.support.events import AbstractEventListener

log = logging.getLogger("selenium.acciones")
PAUSA = float(os.getenv("SEL_PAUSA", "0"))


def _desc(elemento):
    try:
        return (elemento.get_attribute("data-test") or elemento.get_attribute("id")
                or elemento.tag_name)
    except Exception:
        return "elemento"


class RegistroListener(AbstractEventListener):
    def _pausa(self):
        if PAUSA:
            time.sleep(PAUSA)

    def after_navigate_to(self, url, driver):
        log.info("Navegó a %s", url)
        self._pausa()

    def before_click(self, element, driver):
        log.info("Clic en [%s]", _desc(element))

    def after_click(self, element, driver):
        self._pausa()

    def after_change_value_of(self, element, driver):
        log.info("Escribió en [%s]", _desc(element))
        self._pausa()

    def after_execute_script(self, script, driver):
        log.debug("Ejecutó JavaScript: %s", script[:80])

    def on_exception(self, exception, driver):
        log.debug("Excepción de WebDriver: %s", type(exception).__name__)
