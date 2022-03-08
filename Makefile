
unittest:
	pytest --cov=ghs tests -vv

tox:
	tox

lint:
	@echo "Linting with black"
	black --check ghs/
	@echo "Linting with isort"
	isort --check --profile=black ghs
	@echo "Linting with flake8"
	flake8 --max-line-length=88 ghs
