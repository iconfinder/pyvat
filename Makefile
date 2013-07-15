all:

test:
	@nosetests
	@pep8 pyvat tests setup.py
	@pyflakes pyvat tests setup.py

pep8:
	@pep8 pyvat tests setup.py

publish:
	@python setup.py sdist upload
