
python = python3.4

bd = $(shell find . -name '__pycache__' -type d)

.PHONY: clean

clean:
	@rm --recursive --force $(bd)
	@rm --force $(shell find . -type f -name '*.pyc')
	@rm --recursive --force *.egg *.egg-info
