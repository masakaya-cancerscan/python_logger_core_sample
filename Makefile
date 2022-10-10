
.PHONY: test
test:
	export PYTHONPATH="$(pwd):$PYTHONPATH"
	poetry run pytest


.PHONY: test-report-term
test-report-term:
	export PYTHONPATH="$(pwd):$PYTHONPATH"
	poetry run pytest --cov=cs --cov-branch -v ./tests/* --cov-report=term


.PHONY: test-report-html
test-report-html:
	export PYTHONPATH="$(pwd):$PYTHONPATH"
	poetry run pytest --cov=cs --cov-branch -v ./tests/* --cov-report=html


