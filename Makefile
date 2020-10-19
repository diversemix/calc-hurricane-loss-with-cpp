ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
VERSION=$(shell grep __version__ gethurricaneloss/__init__.py)
REQUIREMENTS=requirements-dev.txt


# Only used to create our venv.
SYSTEM_PYTHON=python3

VENV_ROOT=venv
VENV_BIN=$(VENV_ROOT)/bin
VENV_PIP=$(VENV_BIN)/pip
VENV_PYTHON=$(VENV_BIN)/python
UID := $(shell id -u)
GID := $(shell id -g)

.PHONY: export all install clean venv test test-all test-dist test-sdist test-bdist-wheel


export PATH := $(VENV_BIN):$(PATH)


all: venv requirements uninstall-gethurricaneloss install test

requirements:
	$(SYSTEM_PYTHON) -c "import dataclasses"
	@echo
	@echo If this fails try:
	@echo "    sudo apt install python3.7 python3.7-venv python3.7-dev"
	@echo
	$(SYSTEM_PYTHON) --version
	@echo OK!
	@echo


install: requirements venv
	@echo Installing dev requirements...
	./$(VENV_PIP) install --upgrade -r $(REQUIREMENTS)

	@echo Installing gethurricaneloss...
	$(VENV_PIP) install --upgrade --editable .

	@echo

clean:
	@echo Cleaning up...
	rm -rf $(VENV_ROOT)
	# Remove symlink for virtualenvwrapper, if we’ve created one.
	[ -n "$(WORKON_HOME)" -a -L "$(WORKON_HOME)/gethurricaneloss" -a -f "$(WORKON_HOME)/gethurricaneloss" ] && rm $(WORKON_HOME)/gethurricaneloss || true
	rm -rf .tox *.egg dist build .coverage .cache .pytest_cache gethurricaneloss.egg-info
	find . -name '__pycache__' -delete -o -name '*.pyc' -delete
	@echo


venv:
	@echo Creating a Python environment $(VENV_ROOT)

	virtualenv --python=/usr/bin/python3 --prompt gethurricaneloss $(VENV_ROOT)

	@echo
	@echo done.
	@echo
	@echo To active it manually, run:
	@echo
	@echo "    source $(VENV_BIN)/activate"
	@echo
	@echo '(learn more: https://docs.python.org/3/library/venv.html)'
	@echo
	@if [ -n "$(WORKON_HOME)" ]; then \
		echo $(ROOT_DIR) >  $(VENV_ROOT)/.project; \
		if [ ! -d $(WORKON_HOME)/gethurricaneloss -a ! -L $(WORKON_HOME)/gethurricaneloss ]; then \
			ln -s $(ROOT_DIR)/$(VENV_ROOT) $(WORKON_HOME)/gethurricaneloss ; \
			echo ''; \
			echo 'Since you use virtualenvwrapper, we created a symlink'; \
			echo 'so you can also use "workon gethurricaneloss" to activate the venv.'; \
			echo ''; \
		fi; \
	fi

docker: clean
	docker build . -t ghl-dev-tester
	docker run --rm -it -v $(PWD):/app --user $(UID):$(GID) ghl-dev-tester

###############################################################################
# Testing
###############################################################################

lint: install
	@echo Linting...
	$(VENV_BIN)/mypy ./gethurricaneloss ./tests/gethurricaneloss
	$(VENV_BIN)/flake8  --ignore=E501 ./gethurricaneloss ./tests/gethurricaneloss
	@echo

test: lint
	@echo Running tests...
	$(VENV_BIN)/py.test --cov=./gethurricaneloss ./tests/gethurricaneloss
	@echo


# test-all is meant to test everything — even this Makefile
test-all: clean install test test-tox test-dist
	@echo


test-dist: test-sdist test-bdist-wheel
	@echo


test-sdist: clean venv
	@echo Testing sdist build an installation...
	$(VENV_PYTHON) setup.py sdist
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.gz
	$(VENV_BIN)/gethurricaneloss --version
	@echo


test-bdist-wheel: clean venv
	@echo Testing wheel build an installation...
	$(VENV_PIP) install wheel
	$(VENV_PYTHON) setup.py bdist_wheel
	$(VENV_PIP) install --force-reinstall --upgrade dist/*.whl
	$(VENV_BIN)/gethurricaneloss --version
	@echo


###############################################################################
# Uninstalling
###############################################################################

uninstall-gethurricaneloss:
	@echo Uninstalling gethurricaneloss...
	- $(VENV_PIP) uninstall --yes gethurricaneloss &2>/dev/null

	@echo "Verifying…"
	cd .. && ! $(VENV_PYTHON) -m gethurricaneloss --version &2>/dev/null

	@echo "Done"
	@echo

