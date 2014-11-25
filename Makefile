PY_SRC := pyvat tests setup.py

all:

test:
	@nosetests
	@flake8 $(PY_SRC)

check:
	@flake8 $(PY_SRC)

publish:
	@python setup.py sdist upload
