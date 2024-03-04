run: ## Run spyder.
	poetry run gunicorn -b 0.0.0.0:9999 gicornachini.app:factory --worker-class aiohttp.GunicornUVLoopWebWorker --reload --access-logfile '-' --workers 6

run-dev: ## Run spyder.
	poetry run gunicorn -b 0.0.0.0:8000 gicornachini.app:factory --worker-class aiohttp.GunicornUVLoopWebWorker --reload --access-logfile '-' --workers 2
