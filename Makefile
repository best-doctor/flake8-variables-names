check:
	flake8 .
	mypy .
	python -m pytest --cov=flake8_variables_names --cov-report=xml
