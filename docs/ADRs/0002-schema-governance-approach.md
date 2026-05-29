# ADR 0002: Schema Governance Approach

## Status
**Accepted**

## Context
The project manages ontology and schema definitions across multiple modules. We need a clear governance model that:
- Prevents breaking changes
- Enables collaborative schema evolution
- Maintains audit trail for compliance
- Supports versioning and rollback

**Problem:**
- Uncontrolled schema changes can break downstream consumers
- Lack of ownership leads to abandoned schemas
- No mechanism to track schema lifecycle or compliance impact

## Decision
Implement a **schema governance model** with these components:

1. **Schema Registry** (centralized in `agent_a` module)
   - Single source of truth for all schema definitions
   - HTTP API for CRUD operations
   - Semantic versioning (MAJOR.MINOR.PATCH)

2. **Schema Change Process**
   - All schema changes require PR review (enforced by CODEOWNERS)
   - Contract tests must pass (schema compatibility checks)
   - Change author documents rationale in PR description

3. **Module Charters**
   - Define data contracts per module (inputs, outputs, dependencies)
   - Published in `docs/module-charters/` (one page per module)
   - Updated annually or on major changes

4. **Versioning Strategy**
   - MAJOR: Breaking changes (new required fields, field removal)
   - MINOR: Backward-compatible additions (new optional fields)
   - PATCH: Documentation or formatting only
   - Deprecation period: 2 releases before breaking change

5. **Audit Trail**
   - All schema changes committed to Git with CODEOWNERS sign-off
   - Publish hooks emit events to external audit systems
   - Schema snapshots retained for 5 years

## Consequences

**Positive:**
- ✅ Clear ownership and accountability
- ✅ Reduced risk of breaking changes
- ✅ Audit trail for compliance (GDPR, SOC2)
- ✅ Enables confident schema evolution

**Negative:**
- ❌ Schema changes require more coordination (slower time-to-value)
- ❌ Requires discipline in versioning semver
- ❌ Additional infrastructure for audit logging

**Mitigation:**
- Automate versioning detection in CI (fail on incorrect semver)
- Provide schema migration tools for major version upgrades
- Establish SLA for PR review (24-48 hours)

## Alternatives Rejected
1. **No governance**: Leads to chaos and breaking changes
2. **Centralized approval board**: Too slow; delegated to module owners via CODEOWNERS
3. **Automatic schema evolution**: Unsafe without domain expertise

## Implementation Details
- Schema registry: `src/agent_a/schema_registry.py`
- Contract tests: `tests/contract_tests/test_schema_contracts.py`
- Module charter template: `docs/module-charters/_TEMPLATE.md`
- CI checks: `.github/workflows/ci.yml` (schema validation gate)

## Related ADRs
- ADR 0001: Agent Model Selection (uses Claude for schema design)
- ADR 0003: CI/CD Platform Choice (GitHub Actions for enforcement)

---

**Approved by:** Schema Governance Team  
**Date:** 2026-05-27  
**Authors:** @mfd5mf84f5-hub