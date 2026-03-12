#!/usr/bin/env python3
"""Test garbage cleaner with HTML entities"""

import sys
from pathlib import Path

# Add modules directory to path (works on local machine and GitHub Actions)
modules_dir = Path(__file__).parent.parent / 'modules'
sys.path.insert(0, str(modules_dir))

from garbage_cleaner import clean_html

# Test with the exact input from the user
html_test = '''<div class="container customIndexContent"><span class="custom-heading">FROM COAST-TO-COAST</span>&nbsp; &nbsp;&nbsp;<div class="row"><div class="ddc-span12">'''

print("="*70)
print("GARBAGE CLEANER - HTML ENTITY TEST")
print("="*70)
print("\nInput:")
print(repr(html_test[:100]))
print("...")

result = clean_html(html_test)

print("\nOutput:")
print(repr(result.cleaned_html[:100]))
print("...")

print("\n" + "-"*70)
print("Visual comparison:")
print("-"*70)
print("\nInput (visual):")
print(html_test)

print("\nOutput (visual):")
print(result.cleaned_html)

print("\n" + "="*70)
# Check if entities are preserved
if '&nbsp;' in result.cleaned_html:
    print("✓ &nbsp; entities properly preserved!")
else:
    print("✗ &nbsp; entities not found")

# Check for trash characters
trash_chars = ['┬á', '┬', '├', '└']
has_trash = any(char in result.cleaned_html for char in trash_chars)
if has_trash:
    print("✗ Found trash characters in output")
else:
    print("✓ No trash characters found")

print("="*70)
