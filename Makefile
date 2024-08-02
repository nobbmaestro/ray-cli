.PHONY: all clean

all: install

build:
	@echo "Building..."
	poetry build

install: build
	@echo "Installing..."
	pip install dist/*.whl

publish: build
	@echo "Publishing..."

clean:
	@echo "Cleaning up..."
	rm -r dist
	pip uninstall -y ray-cli
