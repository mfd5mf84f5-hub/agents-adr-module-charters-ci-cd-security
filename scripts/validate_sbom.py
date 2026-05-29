#!/usr/bin/env python3
"""Validate CycloneDX SBOM format and content.

Usage:
    python scripts/validate_sbom.py sbom.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def validate_sbom(sbom_path):
    """Validate SBOM format and completeness."""
    
    if not Path(sbom_path).exists():
        print(f"ERROR: SBOM not found: {sbom_path}")
        return False
    
    try:
        with open(sbom_path) as f:
            sbom = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        return False
    
    errors = []
    warnings = []
    
    # Required fields
    required_fields = ['bomFormat', 'specVersion', 'components', 'metadata']
    for field in required_fields:
        if field not in sbom:
            errors.append(f"Missing required field: {field}")
    
    # Format validation
    if sbom.get('bomFormat') != 'CycloneDX':
        errors.append(f"Invalid bomFormat: {sbom.get('bomFormat')}")
    
    if not sbom.get('specVersion', '').startswith('1.'):
        warnings.append(f"Consider using CycloneDX 1.4+: {sbom.get('specVersion')}")
    
    # Component validation
    components = sbom.get('components', [])
    print(f"\nValidating {len(components)} components...\n")
    
    for i, component in enumerate(components):
        component_name = component.get('name', f'Component {i}')
        
        # Required component fields
        if 'type' not in component:
            errors.append(f"{component_name}: Missing type")
        
        if 'name' not in component:
            errors.append(f"Component {i}: Missing name")
        
        if 'version' not in component:
            warnings.append(f"{component_name}: Missing version")
        
        # Check for vulnerable versions (placeholder)
        # In Phase 3, integrate with OSS Index API
        version = component.get('version', '')
        if version.startswith('0.'):
            warnings.append(f"{component_name} v{version}: Pre-release version")
    
    # Metadata validation
    metadata = sbom.get('metadata', {})
    if 'timestamp' not in metadata:
        warnings.append("Missing metadata.timestamp")
    
    if not metadata.get('component'):
        warnings.append("Missing metadata.component")
    
    # Report results
    print(f"\n=== SBOM Validation Report ===")
    print(f"File: {sbom_path}")
    print(f"Format: {sbom.get('bomFormat')} v{sbom.get('specVersion')}")
    print(f"Components: {len(components)}")
    print(f"Timestamp: {metadata.get('timestamp', 'N/A')}")
    
    if errors:
        print(f"\n❌ ERRORS ({len(errors)}):")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors:
        print(f"\n✅ SBOM is valid")
        return True
    else:
        print(f"\n❌ SBOM validation failed")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/validate_sbom.py <sbom.json>")
        sys.exit(1)
    
    sbom_path = sys.argv[1]
    success = validate_sbom(sbom_path)
    sys.exit(0 if success else 1)
