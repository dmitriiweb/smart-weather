.PHONY format:
format:
	ruff format smart_weather
	ruff check smart_weather --select I --fix

.PHONY lint:
lint:
	ruff check smart_weather
	mypy smart_weather
