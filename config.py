"""Configuración general del proyecto."""
import os

# URL de la aplicación bajo prueba. Por defecto, el sitio público de Swag Labs.
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com").rstrip("/")

USUARIO = "standard_user"
USUARIO_BLOQUEADO = "locked_out_user"
USUARIO_LENTO = "performance_glitch_user"
CLAVE = "secret_sauce"

# Tiempo máximo (segundos) de las esperas explícitas.
TIMEOUT = int(os.getenv("TIMEOUT", "10"))
