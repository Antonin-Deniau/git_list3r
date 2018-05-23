PIP=pip
PYTHON=python
TWINE=twine

.PHONY: install publish clean

install:
	$(PIP) install -e .
publish:
	$(PIP) install twine wheel
	$(PYTHON) setup.py sdist bdist_wheel
	$(TWINE) upload dist/*

clean:
	rm -fr build dist .egg requests.egg-info