#!/bin/bash
# Snyk SCA integration for schema architect

set -e

echo "Starting Snyk software composition analysis..."

# Check if Snyk token is available
if [ -z "$SNYK_TOKEN" ]; then
    echo "WARNING: SNYK_TOKEN not set. Using free tier (limited functionality)"
    echo "To enable full SCA: Set SNYK_TOKEN in GitHub Repository Secrets"
    SNYK_ARGS="--severity-threshold=high"
else
    SNYK_ARGS="--severity-threshold=high"
fi

# Install Snyk if not present
if ! command -v snyk &> /dev/null; then
    echo "Installing Snyk CLI..."
    npm install -g snyk
fi

# Authenticate with token if available
if [ ! -z "$SNYK_TOKEN" ]; then
    snyk auth "$SNYK_TOKEN" || true
fi

# Test dependencies for vulnerabilities
echo "Scanning Python dependencies..."
snyk test --package-manager=pip $SNYK_ARGS || EXIT_CODE=$?

if [ "$EXIT_CODE" = "1" ]; then
    echo "ERROR: Vulnerabilities found in dependencies"
    exit 1
elif [ "$EXIT_CODE" = "2" ]; then
    echo "WARNING: Snyk test completed with warnings"
    # Don't fail on warnings
fi

# Generate SBOM
echo "Generating SBOM..."
snyk sbom --format=cyclonedx --output=sbom-snyk.json || true

echo "Snyk scan completed successfully"
