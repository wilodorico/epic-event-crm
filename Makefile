PYTHON=python
PIP=$(PYTHON) -m pip
VENV=venv
ACTIVATE=. $(VENV)/Scripts/activate

SRC_DIR=src
TEST_DIR=collaborators/tests

.PHONY: help venv install activate test integration e2e all

help:
	@echo "Commandes disponibles :"
	@echo "  make test         		-> Lance les tests unitaires (sans SQLAlchemy repo)"
	@echo "  make integration  		-> Lance les tests d'integration (USE_SQLALCHEMY_REPO=1)"
	@echo "  make e2e          		-> Lance les tests end-to-end (USE_SQLALCHEMY_REPO=1)"
	@echo "  make all          		-> Lance tous les tests avec USE_SQLALCHEMY_REPO=1"


test:
	cd $(SRC_DIR) && pytest

integration:
	cd $(SRC_DIR) && USE_SQLALCHEMY_REPO=1 pytest $(TEST_DIR)/usecases

e2e:
	cd $(SRC_DIR) && USE_SQLALCHEMY_REPO=1 pytest $(TEST_DIR)/e2e

all:
	cd $(SRC_DIR) && USE_SQLALCHEMY_REPO=1 pytest -vvv $(TEST_DIR)
