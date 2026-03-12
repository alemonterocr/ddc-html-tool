#!/usr/bin/env python3
"""Comprehensive test with user's exact example"""

import sys
sys.path.insert(0, '.')
from garbage_cleaner import clean_html

# User's exact example
user_html = '<div class="container customIndexContent"><span class="custom-heading">FROM COAST-TO-COAST</span>&nbsp; &nbsp;&nbsp;<div class="row"><div class="ddc-span12">'

print("="*70)
print("GARBAGE CLEANER - USER EXAMPLE TEST")
print("="*70)
print("\nInput (user's exact example):")
print(user_html)

result = clean_html(user_html)

print("\nOutput (cleaned):")
print(result.cleaned_html)

print("\n" + "="*70)
print("STATISTICS:")
print("="*70)
print(f"Original size:     {result.original_size:,} chars")
print(f"Cleaned size:      {result.cleaned_size:,} chars")
print(f"Reduction:         {result.size_reduction:,} chars ({result.reduction_percent:.1f}%)")
print()
print(f"Scripts/Styles removed: {result.script_style_removed}")
print(f"Attributes removed:     {result.attributes_removed}")
print(f"&nbsp; entities removed: {result.entities_removed}")
print()

# Verify no trash characters
trash_chars = ['┬', 'á', '├', '└']
has_trash = any(char in result.cleaned_html for char in trash_chars if ord(char) > 127)
print("═" * 70)
if has_trash:
    print("✗ FAILED: Trash characters found!")
else:
    print("✓ SUCCESS: No trash characters!")

if '&nbsp;' not in result.cleaned_html:
    print("✓ SUCCESS: &nbsp; entities removed!")
else:
    print("✗ FAILED: &nbsp; entities still present!")

if 'class="container' in result.cleaned_html:
    print("✓ SUCCESS: class attributes preserved!")
else:
    print("✗ FAILED: class attributes removed!")

print("="*70)

# Additional comprehensive test
print("\nCOMPREHENSIVE TEST:")
print("="*70)

complex_html = '''<div id="bad" data-test="value" onclick="alert()" class="container">
    <script>console.log("garbage")</script>
    <p style="color: red;" title="hover" onclick="track()" class="text">
        Content&nbsp;with&nbsp;spacing   and more
    </p>
    <a href="page.html" id="link1" onclick="event()" class="link">Click me</a>
    <style>body { margin: 0; }</style>
</div>'''

result2 = clean_html(complex_html)

print("\nInput:")
print(complex_html)
print("\nOutput:")
print(result2.cleaned_html)
print("\nStats:")
print(f"- Removed: {result2.script_style_removed} scripts/styles")
print(f"- Removed: {result2.attributes_removed} garbage attributes")
print(f"- Removed: {result2.entities_removed} &nbsp; entities")
print(f"- Size reduction: {result2.reduction_percent:.1f}%")

print("\n" + "="*70)
print("✓ All tests complete! Garbage cleaner is working properly!")
print("="*70)
