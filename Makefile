.PHONY: test format dist all clean

all: format test

test:
	python3 -m unittest discover tests/

format:
	black .

dist:
	python3 setup.py sdist bdist_wheel
	python2 setup.py bdist_wheel

clean:
	rm -rf dist build mr_sim.egg-info
