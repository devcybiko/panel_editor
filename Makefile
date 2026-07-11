.PHONY: help venv install install-dev update-glslib run test lint format clean build all

VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/python -m pip

help:
	@echo "Available targets:"
	@echo "  venv          - Create virtual environment"
	@echo "  install       - Install the package and dependencies"
	@echo "  install-dev   - Install with development dependencies"
	@echo "  run           - Run the panel editor application"
	@echo "  test          - Run unit tests"
	@echo "  lint          - Run linting checks"
	@echo "  format        - Format code with black"
	@echo "  build         - Build distribution package"
	@echo "  clean         - Remove build artifacts and cache"
	@echo "  all           - Create venv and install everything"

venv:
	@if [ ! -d $(VENV_DIR) ]; then \
		python3.13 -m venv $(VENV_DIR); \
		$(PYTHON) -m pip install --upgrade pip; \
		echo "✓ Virtual environment created"; \
	else \
		echo "✓ Virtual environment already exists"; \
	fi

install: venv
	$(PIP) install -e .
	$(PIP) install --force-reinstall --no-cache-dir "git+https://github.com/devcybiko/glslib.git"
	@echo "✓ Installation complete"

install-dev: venv
	$(PIP) install -e ".[dev]"
	$(PIP) install build
	@echo "✓ Development installation complete"

run: install
	./scripts/run.sh

test: install-dev
	$(PYTHON) -m pytest tests/ -v || $(PYTHON) -m unittest discover tests/ -v

lint: install-dev
	$(PYTHON) -m flake8 src/ --max-line-length=100 || true

format: install-dev
	$(PYTHON) -m black src/ tests/

build: clean install-dev
	$(PYTHON) -m build
	@echo "✓ Build complete - check dist/ folder"

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned"

all: venv install-dev
	@echo "✓ Environment ready!"
	@echo ""
	@echo "Next steps:"
	@echo "  make run       - Start the application"
	@echo "  make test      - Run tests"
	@echo "  source .venv/bin/activate  - Activate venv"
