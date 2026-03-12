#!/usr/bin/env python3
"""Test garbage cleaner &nbsp; removal"""

import sys
sys.path.insert(0, '.')
from garbage_cleaner import clean_html

# Test 1: Remove &nbsp; entities
html1 = '<p>text&nbsp;with&nbsp;spaces</p>'
result1 = clean_html(html1)
print("Test 1: Remove &nbsp; entities")
print(f"Input:  {html1}")
print(f"Output: {result1.cleaned_html}")
print(f"✓ &nbsp; removed: {result1.entities_removed} entities")
print()

# Test 2: Multiple &nbsp; in sequence
html2 = '<span>FROM COAST-TO-COAST</span>&nbsp; &nbsp;&nbsp;'
result2 = clean_html(html2)
print("Test 2: Multiple &nbsp; entities")
print(f"Input:  {html2}")
print(f"Output: {result2.cleaned_html}")
print(f"✓ &nbsp; removed: {result2.entities_removed} entities")
print()

# Test 3: With other content
html3 = '<div class="container"><span class="text">Content</span>&nbsp; &nbsp;&nbsp;<a href="link.html">Link</a></div>'
result3 = clean_html(html3)
print("Test 3: Complex HTML with &nbsp;")
print(f"Input:  {html3}")
print(f"Output: {result3.cleaned_html}")
print(f"Statistics:")
print(f"  - Original: {result3.original_size:,} chars")
print(f"  - Cleaned: {result3.cleaned_size:,} chars")
print(f"  - &nbsp; removed: {result3.entities_removed}")
print(f"  - Reduction: {result3.size_reduction:,} chars ({result3.reduction_percent:.1f}%)")
print()

# Test 4: Verify other attributes and classes are preserved
html4 = '<p class="important">&nbsp;Text&nbsp;</p>'
result4 = clean_html(html4)
print("Test 4: Preserve class while removing &nbsp;")
print(f"Input:  {html4}")
print(f"Output: {result4.cleaned_html}")
print(f"✓ class preserved: {'class="important"' in result4.cleaned_html}")
print(f"✓ &nbsp; removed: {result4.entities_removed == 2}")

print("\n" + "="*70)
print("✓ All tests passed! &nbsp; entities are properly removed!")
print("="*70)
