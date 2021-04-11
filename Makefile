install:
	poetry install

update:
	poetry update

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

publish:
	poetry publish --dry-run
		
lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vs tests