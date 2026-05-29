#!/usr/bin/env python3
"""License compliance checker for dependencies.

Validates that all dependencies have approved licenses.
Usage: python scripts/license_check.py
"""

import subprocess
import json
import sys
from pathlib import Path

# Approved licenses
APPROVED_LICENSES = {
    'MIT',
    'Apache 2.0', 'Apache Software License',
    'BSD',
    'ISC',
    'MPL-2.0', 'Mozilla Public License 2.0',
    'LGPL-3.0', 'GNU Lesser General Public License v3',
    'Python Software Foundation License',
}

# Explicitly blocked licenses
BLOCKED_LICENSES = {
    'GPL',
    'AGPL',
    'GPL-2.0', 'GPL-3.0',
    'AGPL-3.0',
}


def get_installed_licenses() -> dict:
    """Get licenses for all installed packages."""
    try:
        result = subprocess.run(
            ['pip', 'install', 'pip-licenses'],
            capture_output=True,
            text=True,
            check=False
        )
        
        result = subprocess.run(
            ['pip-licenses', '--format=json'],
            capture_output=True,
            text=True,
            check=True
        )
        
        return json.loads(result.stdout)
    except Exception as e:
        print(f"ERROR: Failed to get licenses: {e}")
        return []


def check_licenses(packages: list) -> tuple[bool, list, list]:
    """Check licenses for compliance.
    
    Returns:
        (all_valid, unapproved, blocked)
    """
    unapproved = []
    blocked = []
    
    for pkg in packages:
        license_str = pkg.get('License', 'UNKNOWN')
        
        # Check for blocked licenses
        if any(blocked in license_str for blocked in BLOCKED_LICENSES):
            blocked.append((pkg['Name'], license_str))
        # Check for approved licenses
        elif not any(approved in license_str for approved in APPROVED_LICENSES):
            unapproved.append((pkg['Name'], license_str))
    
    return len(blocked) == 0 and len(unapproved) == 0, unapproved, blocked


def main():
    print("Checking dependency licenses...\n")
    
    packages = get_installed_licenses()
    if not packages:
        print("WARNING: Could not retrieve license information")
        return 1
    
    all_valid, unapproved, blocked = check_licenses(packages)
    
    # Report results
    print(f"Scanned {len(packages)} packages\n")
    
    if blocked:
        print("\u274c BLOCKED LICENSES FOUND:")
        for name, license in blocked:
            print(f"  - {name}: {license}")
        print()
    
    if unapproved:
        print("\u26a0️  UNAPPROVED LICENSES (manual review required):")
        for name, license in unapproved:
            print(f"  - {name}: {license}")
        print()
    
    if all_valid:
        print("\u2705 All licenses approved")
        return 0
    else:
        if blocked:
            print(f"\u274c FAIL: {len(blocked)} blocked license(s) found")
            return 1
        else:
            print(f"\u26a0️  WARNING: {len(unapproved)} unapproved license(s) - review required")
            return 0  # Don't fail on unapproved (manual approval)


if __name__ == '__main__':
    sys.exit(main())
