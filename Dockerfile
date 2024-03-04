FROM python:3.12.2-slim

WORKDIR /gicornachini

COPY ./ /gicornachini

RUN pip install poetry

RUN poetry install

CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:9999", "gicornachini.app:factory", "--worker-class", "aiohttp.GunicornUVLoopWebWorker", "--workers", "4", "--threads", "4"]
