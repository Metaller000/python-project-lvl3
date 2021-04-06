install:
	poetry install

update:
	poetry update

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl
	
lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vs tests