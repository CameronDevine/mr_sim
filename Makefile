.PHONY: test format dist all clean docs

all: format test

test:
	python3 -m unittest discover tests/

format:
	black .

docs:
	sphinx-build docs/ docs/build

dist:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf dist build mr_sim.egg-info docs/build
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
