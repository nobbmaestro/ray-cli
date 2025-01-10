.PHONY: all clean

all: install

build:
	@echo "Building..."
	poetry build

install: build
	@echo "Installing..."
	pipx install --force dist/*.whl

test:
	@echo "Running tests with tox..."
	tox

publish: test build
	@echo "Publishing..."
	poetry publish

clean:
	@echo "Cleaning up..."
	pipx uninstall ray-cli
	rm -r dist
