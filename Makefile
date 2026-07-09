VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(PYTHON) -m pip

.PHONY: install dev-install test run clean

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

dev-install:
	$(PIP) install -e '.[dev]'

test:
	$(PYTHON) -m pytest tests/test_import.py

run:
	$(PYTHON) main.py

clean:
	rm -rf __pycache__
	rm -rf darkgpt/__pycache__
	rm -rf *.egg-info
	rm -rf build dist
	rm -rf .eggs
