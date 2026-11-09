"""7. Page Object Model: las pruebas hablan el idioma del negocio."""
import pytest

import config
from pages.login_page import LoginPage


@pytest.mark.humo
def test_compra_completa(driver):
    catalogo = LoginPage(driver).abrir().iniciar_sesion(config.USUARIO, config.CLAVE)
    assert catalogo.cargada()
    catalogo.agregar("sauce-labs-backpack").agregar("sauce-labs-bike-light")
    assert catalogo.cantidad_en_carrito() == 2
    carrito = catalogo.ir_al_carrito()
    assert carrito.productos() == ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    pago = carrito.pagar().llenar_datos("Bryan", "Peguero", "10101")
    assert pago.total() == "Total: $43.18"
    assert pago.finalizar() == "Thank you for your order!"


@pytest.mark.humo
def test_usuario_bloqueado(driver):
    pagina = LoginPage(driver).abrir()
    pagina.iniciar_sesion(config.USUARIO_BLOQUEADO, config.CLAVE)
    assert pagina.mensaje_error() == "Epic sadface: Sorry, this user has been locked out."
