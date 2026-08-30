.PHONY: all check lint format manifest

all: check

check: lint format-check manifest

lint:
	npx -y @stoplight/spectral-cli lint --fail-severity=warn openapi.yml

format-check:
	npx -y prettier --check openapi.yml postman.json README.md

format:
	npx -y prettier --write openapi.yml postman.json README.md

manifest:
	python3 scripts/check_sdk_manifest.py
