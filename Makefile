install:
	poetry install

dev:
	poetry run flask --app page_analyzer.app run --debug

start:
	poetry run gunicorn -w 4 -b 0.0.0:$(PORT) page_analyzer.app:app

lint:
	poetry run flake8 page_analyzer
