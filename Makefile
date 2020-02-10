.PHONY: test format dist all clean docs upload upload-test

all: format test

test:
	python3 -m unittest discover tests/

format:
	black .

docs:
	sphinx-build docs/ docs/build

dist:
	python3 setup.py sdist bdist_wheel

upload:
	twine upload dist/*

upload-test:
	twine upload dist/* --repository-url https://test.pypi.org/legacy/

clean:
	rm -rf dist build mr_sim.egg-info docs/build
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
