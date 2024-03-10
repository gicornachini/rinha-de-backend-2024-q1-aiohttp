run-dev:
	gunicorn -b 0.0.0.0:8000 gicornachini.app:factory --worker-class aiohttp.GunicornUVLoopWebWorker --reload --access-logfile '-' --workers 2
