test:
	pytest -rA --cov-report term-missing --cov=src --cov-report=xml --junitxml=junit.xml

lint:
	pre-commit install
	pre-commit run --all-files

mypy:
	mypy .
