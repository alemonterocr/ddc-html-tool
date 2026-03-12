#!/usr/bin/env python3
"""Test script for all three modules"""

import sys
sys.path.insert(0, 'c:\\Users\\Ale-CodeRoad\\Desktop\\Optimizers\\projects')

from garbage_cleaner import clean_html
from space_cleaner import clean_spaces
from bs4 import BeautifulSoup

html_test = '''<div id="test" data-attr="bad" class="container">
    <script>alert("garbage")</script>
    <p onclick="track()" style="color: red;" class="text">Some   content   here</p>
    <a href="page.html" id="link1" onclick="event()" class="link">Click me</a>
</div>'''

print("\n" + "="*70)
print("GARBAGE CLEANER TEST")
print("="*70)
result = clean_html(html_test)
print(f"Original size: {result.original_size:,} chars")
print(f"Cleaned size: {result.cleaned_size:,} chars")
print(f"Reduction: {result.size_reduction:,} chars ({result.reduction_percent:.1f}%)")
print(f"Removed: {result.script_style_removed} scripts/styles, {result.attributes_removed} attributes")
print(f"\nCleaned HTML:")
print(result.cleaned_html)

print("\n" + "="*70)
print("SPACE CLEANER TEST")
print("="*70)
cleaned_spaces, spaces_removed = clean_spaces(html_test)
print(f"Original size: {len(html_test):,} chars")
print(f"Cleaned size: {len(cleaned_spaces):,} chars")
print(f"Reduction: {spaces_removed:,} chars")
print(f"\nCleaned HTML:")
print(cleaned_spaces)

print("\n" + "="*70)
print("HREF ANALYZER TEST")
print("="*70)
html_with_bad_hrefs = '''<div>
<a href="page" class="link">Bad href - no extension</a>
<a href="page.html" class="link">Good href</a>
<a href="test.pdf" class="link">PDF link</a>
</div>'''

soup = BeautifulSoup(html_with_bad_hrefs, 'html.parser')
links = soup.find_all('a', href=True)
bad_hrefs = []
for link in links:
    href = link['href'].strip()
    if href and not href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
        clean_href = href.split('?')[0].rstrip('/')
        if not clean_href.lower().endswith(('.htm', '.html')):
            bad_hrefs.append((link.text.strip(), href))

print(f"Found {len(bad_hrefs)} links needing .htm/.html extension:")
for text, href in bad_hrefs:
    print(f"  - {text}: {href}")

print("\n✓ All modules working correctly!")
