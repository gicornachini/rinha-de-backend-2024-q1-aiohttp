import logging

from aiohttp import web
from aiohttp.web import Application, normalize_path_middleware

from gicornachini.handlers import transaction, statement
from gicornachini.db import setup_db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def _set_routes(app):
    app.router.add_post("/clientes/{id}/transacoes", transaction)
    app.router.add_get("/clientes/{id}/extrato", statement)


def _get_middlewares():
    return (
        normalize_path_middleware(append_slash=True),
    )


async def factory():
    middlewares = _get_middlewares()
    app = Application(
        middlewares=middlewares,
        logger=logger)
    _set_routes(app)
    app.cleanup_ctx.append(setup_db)
    return app
