"""Fixtures compartidas: driver por navegador, capturas y adjuntos para los reportes."""
import logging
import os

import allure
import pytest

from utils.driver_factory import crear_driver

log = logging.getLogger("conftest")


def pytest_configure(config):
    # Solo nos interesan las acciones de la prueba, no el detalle HTTP interno de Selenium.
    for nombre in ("selenium.webdriver.remote", "selenium.webdriver.common", "urllib3"):
        logging.getLogger(nombre).setLevel(logging.WARNING)


def pytest_addoption(parser):
    parser.addoption("--browser", action="append", default=[],
                     help="Navegador: chrome, firefox o edge. Se puede repetir para varios.")
    parser.addoption("--headless", action="store_true", help="Ejecutar sin ventana visible.")


def pytest_generate_tests(metafunc):
    # Cada prueba que usa el fixture "driver" se ejecuta una vez por navegador.
    if "driver" in metafunc.fixturenames:
        navegadores = metafunc.config.getoption("--browser") or ["chrome"]
        metafunc.parametrize("navegador", navegadores, scope="function")


@pytest.fixture
def driver(navegador, request):
    d = crear_driver(navegador, headless=request.config.getoption("--headless"))
    yield d
    d.quit()
    log.info("Navegador cerrado")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Al terminar cada prueba, adjunta una captura de pantalla al reporte."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when != "call" or "driver" not in item.fixturenames:
        return
    d = item.funcargs["driver"]
    os.makedirs("reportes/capturas", exist_ok=True)
    nombre = item.name.replace("[", "_").replace("]", "")
    ruta = f"reportes/capturas/{nombre}.png"
    d.save_screenshot(ruta)
    allure.attach.file(ruta, name="captura", attachment_type=allure.attachment_type.PNG)
    html = item.config.pluginmanager.getplugin("html")
    if html:
        extras = getattr(rep, "extras", [])
        extras.append(html.extras.png(d.get_screenshot_as_base64()))
        rep.extras = extras
    if rep.failed:
        log.error("Falló %s; captura en %s", item.name, ruta)
