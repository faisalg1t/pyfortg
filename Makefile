.PHONY: help install install-dev test lint format clean docker-build docker-up docker-down

help:
	@echo "PyForTG Development Commands"
	@echo "============================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          - Install package"
	@echo "  make install-dev      - Install with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test             - Run tests"
	@echo "  make test-cov         - Run tests with coverage"
	@echo "  make lint             - Run linting checks"
	@echo "  make format           - Format code"
	@echo "  make type-check       - Run type checking"
	@echo "  make clean            - Clean up build artifacts"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-up        - Start services with docker-compose"
	@echo "  make docker-down      - Stop services"
	@echo ""

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,all]"

test:
	pytest

test-cov:
	pytest --cov=pyfortg --cov-report=html --cov-report=term

lint:
	flake8 pyfortg/
	isort --check-only pyfortg/
	black --check pyfortg/

format:
	isort pyfortg/
	black pyfortg/

type-check:
	mypy pyfortg/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

docker-build:
	docker build -t pyfortg:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	docker-compose down -v

build:
	python -m build

publish-test:
	python -m twine upload --repository testpypi dist/*

publish:
	python -m twine upload dist/*

version:
	@grep "version" pyproject.toml | head -1
