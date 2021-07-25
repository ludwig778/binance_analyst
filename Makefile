ARGS = $(filter-out $@,$(MAKECMDGOALS))

TEST_ARGS =


default: py

py:
	python3 ${ARGS}

sh:
	bash

lint:
	python3 -m flake8 .

isort:
	python3 -m isort .

piprot:
	piprot

black:
	black --line-length 104 .

sure: lint isort piprot black

tests:
	pytest ${TEST_ARGS}
.PHONY: tests

cov:
	pytest ${TEST_ARGS} --cov=backend

cov_html:
	pytest ${TEST_ARGS} --cov=backend --cov-append --cov-report html:coverage_html

clean:
	rm -rf coverage_html
	find . -name "*.pyc" -o -name "__pycache__"|xargs rm -rf
