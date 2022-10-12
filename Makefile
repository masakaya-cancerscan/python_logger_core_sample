export PYTHONPATH = $(shell echo $$PYTHONPATH):$(PWD)


.PHONY: test
test:
	poetry run pytest

.PHONY: test-report-term
test-report-term:
	poetry run pytest --cov=cs --cov-branch -v ./tests/* --cov-report=term


.PHONY: test-report-html
test-report-html:
	poetry run pytest --cov=cs --cov-branch -v ./tests/* --cov-report=html


