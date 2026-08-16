# XYO Financial API Specs

[![Lint and Format](https://github.com/xyo-financial/specs/actions/workflows/lint.yml/badge.svg)](https://github.com/xyo-financial/specs/actions/workflows/lint.yml)
[![Dispatch SDKs](https://github.com/xyo-financial/specs/actions/workflows/dispatch.yml/badge.svg)](https://github.com/xyo-financial/specs/actions/workflows/dispatch.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Central source of truth for the **[XYO Financial](https://xyo.financial)** AI Transaction Enrichment API specifications and machine-readable definitions.

---

## 📋 Available Specifications

- **OpenAPI v3.0 Specification:** [`openapi.yml`](openapi.yml) — Standard OpenAPI definition utilized for automated multi-language SDK code generation.
- **Postman Collection:** [`postman.json`](postman.json) — Ready-to-import API test suite and request collection.

---

## 🌐 Official Client SDKs

All official client SDKs are deterministically generated and synchronized with this repository:

| Language / Runtime       | Repository                                                                | Package / Ecosystem                      |
| :----------------------- | :------------------------------------------------------------------------ | :--------------------------------------- |
| **Go**                   | [`xyo-financial/sdk-go`](https://github.com/xyo-financial/sdk-go)         | `go get github.com/xyo-financial/sdk-go` |
| **Node.js & TypeScript** | [`xyo-financial/sdk-node`](https://github.com/xyo-financial/sdk-node)     | `npm install @xyo-financial/sdk`         |
| **Python**               | [`xyo-financial/sdk-python`](https://github.com/xyo-financial/sdk-python) | `pip install xyo-sdk`                    |
| **.NET / C#**            | [`xyo-financial/sdk-dotnet`](https://github.com/xyo-financial/sdk-dotnet) | `dotnet add package Xyo.Sdk`             |
| **Java**                 | [`xyo-financial/sdk-java`](https://github.com/xyo-financial/sdk-java)     | Maven Central / Gradle                   |
| **Rust**                 | [`xyo-financial/sdk-rust`](https://github.com/xyo-financial/sdk-rust)     | `cargo add xyo`                          |
| **PHP**                  | [`xyo-financial/sdk-php`](https://github.com/xyo-financial/sdk-php)       | `composer require xyo/sdk`               |
| **C++**                  | [`xyo-financial/sdk-cpp`](https://github.com/xyo-financial/sdk-cpp)       | CMake / vcpkg                            |

---

## 🏛️ API Governance & Contribution

This repository enforces strict OpenAPI schema validation and style governance:

1. **Prettier Formatting:** Ensures consistent YAML/JSON indentation and formatting.
2. **Spectral Linting:** Validates OpenAPI 3.0 semantic accuracy and structural rules via `.spectral.yaml`.
3. **Automated SDK Dispatch:** Pushing a new version tag (e.g. `v2.0.0`) automatically dispatches a `spec_tagged` webhook to all 8 client SDK repositories to trigger automated regeneration and test validation.

### Local Verification

```bash
# Verify formatting
npx prettier --check openapi.yml postman.json

# Run Spectral linting
npx @stoplight/spectral-cli lint --fail-severity=warn openapi.yml
```

---

## 📄 License

Copyright &copy; Syniol Limited. Licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
