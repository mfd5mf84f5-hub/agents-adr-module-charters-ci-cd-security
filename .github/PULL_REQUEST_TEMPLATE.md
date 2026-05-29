# Pull Request

## Description
<!-- Concisely describe the change (1-3 sentences) -->

## Type of change
<!-- Mark the relevant option -->
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] Feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality change)
- [ ] Documentation (documentation only)

## Related Issues
<!-- Link related issues: Fixes #123, Relates to #456 -->

## Testing
<!-- Describe how you tested this change -->
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Pre-submission Checklist

### Code Quality
- [ ] My code follows the repository's code style and conventions
- [ ] I have performed a self-review of my own code
- [ ] Linting passes (`flake8 src tests`, `black --check .`)
- [ ] Code is formatted correctly (`black .`)

### Testing
- [ ] Unit tests pass (`pytest -q`)
- [ ] Unit test coverage threshold met (75% minimum)
- [ ] All existing tests still pass
- [ ] Contract tests pass (if schema changes): `pytest tests/contract_tests -v`

### Documentation
- [ ] README.md updated (if applicable)
- [ ] Module charter updated (if new module)
- [ ] Docstrings added/updated for public APIs
- [ ] Migration guide provided (if breaking change)

### Security & Compliance
- [ ] No secrets, API keys, or credentials in code
- [ ] No hardcoded passwords or tokens
- [ ] Dependencies updated in `pyproject.toml` (if added/changed)
- [ ] SBOM regenerated (if dependencies changed)
- [ ] Security scan results reviewed (SCA, SAST)

### Governance
- [ ] CODEOWNERS have been assigned and notified
- [ ] ADR created (if architectural decision made)
- [ ] Change log entry added (if user-facing)
- [ ] Backward compatibility maintained (unless major version bump)

## Additional context
<!-- Anything else reviewers should know? -->

## Checklist for Reviewers

### Functional Review
- [ ] Correctly implements the intended behavior
- [ ] Handles edge cases and error conditions
- [ ] Performance impact assessed (if applicable)
- [ ] Backward compatibility maintained (unless intentional breaking change)

### Code Quality
- [ ] Code is readable and maintainable
- [ ] No unnecessary complexity
- [ ] DRY principle followed (no code duplication)
- [ ] Comments/docstrings are clear and accurate

### Testing
- [ ] Test coverage is adequate
- [ ] Tests are meaningful (not just checking syntax)
- [ ] Edge cases are tested
- [ ] Contract tests validate schema compatibility

### Security
- [ ] No security vulnerabilities introduced
- [ ] Input validation present (if applicable)
- [ ] Secrets handling correct (none committed)
- [ ] Dependency versions pinned appropriately

### Compliance
- [ ] CODEOWNERS approved (if required)
- [ ] Documentation complete
- [ ] Audit trail maintained (git history clear)
- [ ] Compliance obligations met (GDPR, SOC2, etc.)

---

**Note:** All items in the pre-submission checklist must be completed before requesting review. Reviewers will not approve PRs with incomplete checklists.
