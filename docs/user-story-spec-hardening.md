# Agile User Story: Enterprise OpenAPI Schema & Postman Collection Hardening

**Story ID:** `US-SPEC-001`  
**Epic:** `EPIC-002: Tier-1 Enterprise Governance & Schema Hardening`  
**Status:** `Ready for Development`  
**Priority:** `P1 (High)`  
**Standard Compliance:** `INVEST Model & Gherkin BDD Acceptance Criteria`  
**Target Repository:** [`xyo-financial/specs`](https://github.com/xyo-financial/specs)

---

## 1. User Story Statement

> **As an** Enterprise API Architect / Security Engineer at a Tier-1 Global Bank (e.g., HSBC, JPMorgan Chase),  
> **I want** the OpenAPI 3.0 specification (`openapi.yml`) and Postman collection (`postman.json`) to enforce explicit array boundary constraints (`minItems`/`maxItems`), formal rate-limiting response headers, and parameterized mock authentication variables,  
> **So that** enterprise API gateways (Apigee, Kong, AWS API Gateway) reject oversized batch denial-of-service attempts at the network edge, and automated SAST/secret-scanning tools pass with zero false-positive security findings in institutional CI/CD pipelines.

---

## 2. Business Value & Strategic Rationale

- **Gateway-Level Denial-of-Service Defense:** Declaring `minItems: 1` and `maxItems: 50000` in `openapi.yml` enables bank edge proxies and WAFs to reject empty or multi-gigabyte array payloads before reaching core enrichment workloads.
- **Elimination of SAST & Secret Scanner False Positives:** Hardcoded high-entropy mock token strings in `postman.json` trigger automated alerts in enterprise tools (GitGuardian, TruffleHog, GitHub Secret Scanning). Parameterizing tokens with `{{BEARER_TOKEN}}` and `{{XYO_API_KEY}}` ensures clean security scan reports.
- **IETF Rate Limiting & Resilience Alignment:** Formally documenting RFC-compliant `Retry-After`, `RateLimit-Limit`, `RateLimit-Remaining`, and `RateLimit-Reset` headers enables automated client resilience frameworks (Polly, Resilience4j) to dynamically compute backoff schedules without guessing.
- **OpenAPI Governance:** Ensures 100% compliance with Spectral OpenAPI rulesets (`spectral:oas`) and automated repository dispatch across all 8 multi-language SDK codebases.

---

## 3. Technical Requirements & Architectural Scope

### 3.1 OpenAPI Specification (`openapi.yml`)

1. **Batch Array Boundary Constraints:**
   - On `/v1/ai/finance/enrichment/transactions` `requestBody.content.application/json.schema`:
     - Add `minItems: 1` (reject empty batches at schema boundary).
     - Add `maxItems: 50000` (enforce batch size ceiling matching the 50K tar entry limit).
2. **Rate Limit & Observability Response Headers:**
   - Under HTTP `429` Too Many Requests responses:
     - Define `Retry-After` header (`type: integer`, description: "Seconds to wait before retrying request").
     - Define `RateLimit-Limit`, `RateLimit-Remaining`, `RateLimit-Reset` headers.
3. **Multi-Tenant Correlation Header:**
   - Document `X-Correlation-ID` (`type: string`) in response header schemas.

### 3.2 Postman Collection (`postman.json`)

1. **Token Parameterization:**
   - Replace all static, high-entropy mock Bearer strings with standard Postman variable placeholders: `{{BEARER_TOKEN}}` / `{{XYO_API_KEY}}`.
   - Provide clean collection-level variables section.

---

## 4. Acceptance Criteria (Gherkin BDD Format)

```gherkin
Feature: Enterprise OpenAPI Schema and Postman Collection Hardening

  Background:
    Given the XYO Financial API specifications repository `xyo-financial/specs`

  Scenario: Explicit Array Bounds on Batch Enrichment Request Schema
    Given the OpenAPI specification file `openapi.yml`
    When inspecting the `/v1/ai/finance/enrichment/transactions` POST endpoint requestBody schema
    Then the schema must define `type: array`
    And the schema must specify `minItems: 1`
    And the schema must specify `maxItems: 50000`
    And Spectral linting must pass with 0 errors and 0 warnings

  Scenario: Standardized Rate Limit and Error Response Headers
    Given the OpenAPI specification file `openapi.yml`
    When inspecting HTTP 429 Too Many Requests response definitions
    Then the response must document the `Retry-After` header as integer seconds
    And the response must document `RateLimit-Limit`, `RateLimit-Remaining`, and `RateLimit-Reset` headers

  Scenario: Zero Secret Scanner False Positives in Postman Collection
    Given the Postman collection file `postman.json`
    When scanning the collection with automated secret detection tools (GitGuardian / TruffleHog)
    Then no static high-entropy mock token strings must be present in request authorization blocks
    And all Bearer token values must reference the parameterized variable `{{BEARER_TOKEN}}`

  Scenario: Automated Spec Validation & SDK Regeneration Dispatch
    Given a commit to `openapi.yml` on the `main` branch
    When the GitHub Actions `lint.yml` workflow executes
    Then `prettier --check` must pass for all YAML and JSON files
    And `spectral lint --fail-severity=warn` must pass cleanly
```

---

## 5. INVEST Matrix Compliance

| Criteria        | Assessment | Rationale                                                                                          |
| :-------------- | :--------: | :------------------------------------------------------------------------------------------------- |
| **Independent** |     ✅     | Can be implemented and verified directly within `specs` without blocking runtime SDK development.  |
| **Negotiable**  |     ✅     | Header field names and default batch boundaries can be adjusted based on gateway infrastructure.   |
| **Valuable**    |     ✅     | Eliminates enterprise SAST scanner blockers and enables edge WAF array validation in Tier-1 banks. |
| **Estimable**   |     ✅     | Clear scope bounded to `openapi.yml` and `postman.json` updates with automated lint validation.    |
| **Small**       |     ✅     | Focused, atomic changes that can be developed, tested, and reviewed within a single PR.            |
| **Testable**    |     ✅     | Fully verifiable via `spectral lint`, `prettier --check`, and automated Postman schema validators. |

---

## 6. Definition of Done (DoD)

- [ ] `openapi.yml` updated with `minItems: 1`, `maxItems: 50000`, and rate limit response headers.
- [ ] `postman.json` updated with parameterized `{{BEARER_TOKEN}}` variables.
- [ ] `make check` (`spectral lint` + `prettier --check`) passes with 0 warnings/errors.
- [ ] Pull request opened, reviewed, and squash-merged to `main`.
- [ ] GitHub issue created and linked to this User Story.
