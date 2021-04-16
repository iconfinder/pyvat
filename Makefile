PY_SRC := pyvat tests setup.py

all:

check:
	@flake8 $(PY_SRC)

docs:
	pip install sphinx sphinx_rtd_theme
	@make -C docs html

publish:
	@python setup.py sdist upload

test_publish:
	twine upload --repository testpypi dist/*

test:
	@nosetests
	@flake8 $(PY_SRC)



.PHONY: check docs publish test
