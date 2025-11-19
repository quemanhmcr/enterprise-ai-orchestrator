.PHONY: install test lint format clean run docker-build docker-run

install:
	pip install -r requirements.txt
	pip install -e .[dev]
	pre-commit install

test:
	pytest

lint:
	ruff check .
	black --check .

format:
	black .
	ruff check . --fix

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

run:
	python main.py --orchestrate

docker-build:
	docker build -t enterprise-business-system .

docker-run:
	docker run --env-file .env enterprise-business-system
