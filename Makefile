install:
	poetry install

build:
	./build.sh

publish:
	poetry publish --dry-run

package-install:
	python -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_analyzer

dev:
	poetry run flask --debug --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
