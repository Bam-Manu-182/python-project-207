install:
	uv sync

build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0:$(PORT) page_analyzer:app
