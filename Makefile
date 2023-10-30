APP = delivery_api

type-check:
	mypy $(APP)

lint:
	flake8 $(APP)
	pylint $(APP)

unit-test:
	pytest tests