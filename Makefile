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
