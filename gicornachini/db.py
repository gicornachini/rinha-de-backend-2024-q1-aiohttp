import logging

import aiopg

logger = logging.getLogger(__name__)

dsn = 'dbname=rinha user=admin password=123 host=db'

async def setup_db(app) -> None:
    logger.info('initializing postgresql')
    app['db_pool'] = await aiopg.create_pool(dsn=dsn, minsize=1, maxsize=0)
    yield
    logger.info('closing postgresql')
    app['db_pool'].terminate()
    await app['db_pool'].wait_closed()

