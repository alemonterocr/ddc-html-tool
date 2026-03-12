#!/usr/bin/env python3
"""Validation script - checks that all modules are working"""

import sys
import os

# Add parent directory to path so we can import modules and main
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'modules'))

print("="*70)
print("HTML CLEANING TOOLKIT - VALIDATION")
print("="*70)

tests_passed = 0
tests_total = 0

# Test 1: Import garbage_cleaner
tests_total += 1
try:
    from garbage_cleaner import run_garbage_cleaner, clean_html
    print("✓ garbage_cleaner module imported")
    tests_passed += 1
except Exception as e:
    print(f"✗ Error importing garbage_cleaner: {e}")

# Test 2: Import space_cleaner
tests_total += 1
try:
    from space_cleaner import run_space_cleaner, clean_spaces
    print("✓ space_cleaner module imported")
    tests_passed += 1
except Exception as e:
    print(f"✗ Error importing space_cleaner: {e}")

# Test 3: Import href_analyzer
tests_total += 1
try:
    from href_analyzer import run_href_analyzer
    print("✓ href_analyzer module imported")
    tests_passed += 1
except Exception as e:
    print(f"✗ Error importing href_analyzer: {e}")

# Test 4: Import main
tests_total += 1
try:
    import main
    print("✓ main menu imported")
    tests_passed += 1
except Exception as e:
    print(f"✗ Error importing main: {e}")

# Test 5: Quick functionality test
tests_total += 1
try:
    test_html = '<div id="test"><script>bad</script><p class="text">Good</p></div>'
    result = clean_html(test_html)
    assert '<script>' not in result.cleaned_html
    assert 'class="text"' in result.cleaned_html
    print("✓ garbage_cleaner functionality test passed")
    tests_passed += 1
except Exception as e:
    print(f"✗ Garbage cleaner functionality test failed: {e}")

print("\n" + "="*70)
print(f"RESULTS: {tests_passed}/{tests_total} tests passed")
print("="*70)

if tests_passed == tests_total:
    print("\n✓ All systems ready! Run: python main.py")
    sys.exit(0)
else:
    print(f"\n✗ {tests_total - tests_passed} test(s) failed")
    sys.exit(1)
