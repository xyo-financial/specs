# XYO Financial API Specs

[![Lint and Format](https://github.com/xyo-financial/specs/actions/workflows/lint.yml/badge.svg)](https://github.com/xyo-financial/specs/actions/workflows/lint.yml)
[![Dispatch SDKs](https://github.com/xyo-financial/specs/actions/workflows/dispatch.yml/badge.svg)](https://github.com/xyo-financial/specs/actions/workflows/dispatch.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Central source of truth for the **[XYO Financial](https://xyo.financial)** AI Transaction Enrichment API specifications and machine-readable definitions.

---

## 📋 Available Specifications

| Specification          | Artifact                       | Purpose                                                  |
| :--------------------- | :----------------------------- | :------------------------------------------------------- |
| **OpenAPI v3.0**       | [`openapi.yml`](openapi.yml)   | Multi-language SDK code generation and schema contract   |
| **Postman Collection** | [`postman.json`](postman.json) | Ready-to-import API request suite and testing collection |

---

## 🌐 Official Client SDKs

All official client SDKs are synchronized with this repository. Six generate their client from `openapi.yml` and wrap it by hand. C++ is the single exception, and that exception is under review:

| Language / Runtime       | Repository                                                                | Package / Ecosystem                      | Sync                            |
| :----------------------- | :------------------------------------------------------------------------ | :--------------------------------------- | :------------------------------ |
| **C++**                  | [`xyo-financial/sdk-cpp`](https://github.com/xyo-financial/sdk-cpp)       | CMake / vcpkg                            | Hand-written, verified (review) |
| **Rust**                 | [`xyo-financial/sdk-rust`](https://github.com/xyo-financial/sdk-rust)     | `cargo add xyo-sdk`                      | Generated                       |
| **Go**                   | [`xyo-financial/sdk-go`](https://github.com/xyo-financial/sdk-go)         | `go get github.com/xyo-financial/sdk-go` | Generated                       |
| **Java**                 | [`xyo-financial/sdk-java`](https://github.com/xyo-financial/sdk-java)     | Maven Central / Gradle                   | Generated                       |
| **.NET / C#**            | [`xyo-financial/sdk-dotnet`](https://github.com/xyo-financial/sdk-dotnet) | `dotnet add package Xyo.Sdk`             | Generated                       |
| **Python**               | [`xyo-financial/sdk-python`](https://github.com/xyo-financial/sdk-python) | `pip install xyo-sdk`                    | Generated                       |
| **Node.js & TypeScript** | [`xyo-financial/sdk-node`](https://github.com/xyo-financial/sdk-node)     | `npm install xyo-sdk`                    | Generated                       |

A **generated** SDK regenerates its client from `openapi.yml` on every `spec_tagged` dispatch and opens a pull request with the result. The generated layer is committed exactly as the generator emits it, never hand-edited or reformatted, and a hand-crafted wrapper in front of it supplies the ergonomics the generator does not: idiomatic types, error mapping, streaming and egress controls.

**Generation is the convention.** A new SDK should follow it, and an existing one should not diverge from it without a recorded decision. C++ is currently the only exception, because its generated client pulled in `cpprestsdk` and `Boost` across eight vcpkg triplets including Android cross-compiles; whether it converges is being decided in [`sdk-cpp#29`](https://github.com/xyo-financial/sdk-cpp/issues/29). Meanwhile it consumes the same dispatch and verifies that its client still covers every path the specification declares, raising an issue when a change needs implementing by hand.

---

## 🏛️ API Governance & Contribution

This repository enforces strict OpenAPI schema validation and style governance:

1. **Prettier Formatting:** Ensures consistent YAML/JSON indentation and formatting.
2. **Spectral Linting:** Validates OpenAPI 3.0 semantic accuracy and structural rules via `.spectral.yaml`.
3. **Automated SDK Dispatch:** Pushing a new version tag (e.g. `v2.0.0`) dispatches a `spec_tagged` event to all 7 client SDK repositories, each of which then regenerates or verifies its client according to its own toolchain.

#### Dispatch Contract

`spec_tagged` is the only event this repository emits, and it carries a single field:

```json
{ "tag": "v2.0.0" }
```

Consumers should treat `tag` as a git ref in this repository and check the specification out at that ref. On a tag push it is the pushed tag. On a manual run of the dispatch workflow it is whatever ref the operator supplied, defaulting to the ref the run was started from.

A new SDK should subscribe to `spec_tagged` only. An earlier `spec_updated` event was subscribed to by several SDKs but never emitted; it has been retired rather than implemented, because the generating SDKs do not filter on whether `openapi.yml` actually changed, so emitting on every push to `main` would raise regeneration pull requests across the fleet for unrelated commits.

### Local Verification

```bash
# Verify formatting
npx prettier --check openapi.yml postman.json README.md

# Run Spectral linting
npx @stoplight/spectral-cli lint --fail-severity=warn openapi.yml
```

---

## 📄 License

Copyright &copy; Syniol Limited. Licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
