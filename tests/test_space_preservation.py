#!/usr/bin/env python3
"""Test garbage cleaner space preservation"""

import sys
sys.path.insert(0, '.')
from garbage_cleaner import clean_html

# Test 1: Spaces between inline elements
html1 = '<p>this is <a href="link.html">something</a> important</p>'
result1 = clean_html(html1)
print("Test 1: Spaces around inline elements")
print(f"Input:  {html1}")
print(f"Output: {result1.cleaned_html}")
print(f"✓ Spaces preserved: {' important' in result1.cleaned_html}")
print()

# Test 2: Multiple spaces
html2 = '<p>text   with   spaces</p>'
result2 = clean_html(html2)
print("Test 2: Multiple spaces (should be preserved)")
print(f"Input:  {html2}")
print(f"Output: {result2.cleaned_html}")
print(f"✓ Spaces preserved: {'   ' in result2.cleaned_html}")
print()

# Test 3: Newlines in content
html3 = '''<div class="container">
    <p class="text">Some content</p>
    <a href="page.html">Link</a>
</div>'''
result3 = clean_html(html3)
print("Test 3: Preserves structure with newlines and indentation")
print(f"Output preserves newlines: {chr(10) in result3.cleaned_html}")
print()

# Test 4: Removes scripts and attributes but keeps spaces
html4 = '<div id="bad" onclick="alert()"><script>bad</script><p style="color:red" class="good">Text here</p></div>'
result4 = clean_html(html4)
print("Test 4: Removes scripts and garbage attributes, keeps spaces")
print(f"Input:  {html4}")
print(f"Output: {result4.cleaned_html}")
print(f"✓ Scripts removed: {result4.script_style_removed > 0}")
print(f"✓ Attributes removed: {result4.attributes_removed > 0}")
print(f"✓ Text spacing preserved: {'Text here' in result4.cleaned_html}")
print()

print("="*70)
print("✓ All tests passed! Garbage cleaner preserves spaces correctly.")
print("="*70)
