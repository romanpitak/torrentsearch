
python = python3

bd = $(shell find . -name '__pycache__' -type d)

.PHONY: test clean

test:
	$(python) setup.py test

clean:
	@rm --recursive --force $(bd)
	@rm --force $(shell find . -type f -name '*.pyc')
	@rm --recursive --force *.egg *.egg-info
