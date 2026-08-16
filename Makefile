.PHONY: all check lint format

all: check

check: lint format-check

lint:
	npx -y @stoplight/spectral-cli lint --fail-severity=warn openapi.yml

format-check:
	npx -y prettier --check openapi.yml postman.json README.md

format:
	npx -y prettier --write openapi.yml postman.json README.md
