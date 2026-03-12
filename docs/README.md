# HTML Cleaning Toolkit

A modular suite of HTML cleaning utilities built with clean architecture principles. Choose exactly what you need to clean your HTML.

## Features

### 1. **Garbage Cleaner**

- Removes `<script>` and `<style>` tags completely
- Strips unnecessary HTML attributes (keeps only `class` and `href` on `<a>`)
- Collapses redundant whitespace within text
- Display cleanup statistics

**Ideal for:** Removing client-side code and presentation attributes from HTML

### 2. **Space Cleaner**

- Removes excessive whitespace between HTML tags
- Preserves meaningful spaces around inline elements
- Special handling for `<a>`, `<span>`, `<b>`, `<i>`, `<strong>`, `<em>`, etc.
- Keeps text readable and properly formatted

**Ideal for:** Minifying HTML while maintaining readability

### 3. **HREF Analyzer**

- Detects anchor tags with incomplete or problematic href attributes
- Interactive interface to review and fix broken links
- Identify links missing `.htm`/`.html` extensions
- Bulk update href references

**Ideal for:** Fixing broken internal links and updating URL schemes

---

## Usage

### Run the Interactive Menu

```powershell
python main.py
```

The menu will display:

```
────────────────────────────────────
       HTML CLEANING TOOLKIT
────────────────────────────────────

1. Garbage Cleaner
   Remove scripts, styles, and unnecessary attributes.

2. Space Cleaner
   Delete unnecessary spaces between tags.

3. HREF Analyzer
   Review and fix broken href references.

4. Exit
```

### Interactive Workflow

1. **Select an option** (1-4)
2. **Paste your HTML** when prompted:
   ```
   → Paste your HTML (press Enter twice when done):
   ```

   - Paste your HTML content
   - Press Enter twice (once for newline, once blank line) when finished
3. **Review results** - Each tool displays:
   - What was changed
   - Statistics (size reduction, items removed, etc.)
   - Cleaned HTML is automatically **copied to clipboard**

4. **Choose another tool** or exit

---

## Example Usage

### Garbage Cleaner Example

**Input:**

```html
<div id="container" data-test="value" onclick="alert()" class="main">
  <script>
    console.log("bad");
  </script>
  <p style="color: red;" class="text">Content</p>
  <a href="page.html" onclick="track()" class="link">Click</a>
</div>
```

**Output:**

```html
<div class="main">
  <p class="text">Content</p>
  <a href="page.html" class="link">Click</a>
</div>
```

✅ Removed: 1 script, 5 garbage attributes  
✅ Reduction: 56.8% size reduction

---

### Space Cleaner Example

**Input:**

```html
<div id="test" class="container">
  <p>Some content</p>
  <a href="test.html">Link</a>
</div>
```

**Output:**

```html
<div id="test" class="container">
  <p>Some content</p>
  <a href="test.html">Link</a>
</div>
```

✅ Removed unnecessary newlines and excessive spaces between tags

---

### HREF Analyzer Example

**Input:**

```html
<div>
  <a href="about">About (missing .html)</a>
  <a href="page.html">Home (good)</a>
  <a href="contact.pdf">Download (PDF)</a>
</div>
```

**Detection:**

```
Found 2 links needing updates:
• About: "about"
• Download: "contact.pdf"
```

**Interactive Fix:**

```
Text: About
Current: about
New Href: about.html    ← You enter the fix

Text: Download
Current: contact.pdf
New Href:              ← Press ENTER to keep original
```

---

## Module Architecture

### Separation of Concerns

```
main.py                    ← Menu orchestration
├── garbage_cleaner.py    ← HTML sanitization logic
├── space_cleaner.py      ← Whitespace optimization
└── href_analyzer.py      ← Link verification & fixing
```

Each module:

- Has a single responsibility
- Contains both business logic and interactive functions
- Returns cleaned HTML for clipboard copy
- Displays its own formatted output

### Running Modules Individually

```python
from garbage_cleaner import clean_html, run_garbage_cleaner
from space_cleaner import clean_spaces, run_space_cleaner
from href_analyzer import run_href_analyzer

# Use directly in your code
result = clean_html(html_string)
cleaned, removed = clean_spaces(html_string)
```

---

## Requirements

- Python 3.8+
- `rich` - CLI formatting and panels
- `beautifulsoup4` - HTML parsing for HREF analyzer

### Installation

```powershell
pip install rich beautifulsoup4
```

---

## Add to PATH (Windows)

To use from anywhere in your terminal:

1. Copy `main.py` to a directory in your PATH (or create one)
2. Create a batch file wrapper:
   ```batch
   @echo off
   python C:\path\to\main.py %*
   ```
3. Name it `html-toolkit.bat`

Now run from anywhere:

```powershell
html-toolkit
```

---

## Tips & Tricks

✅ **Copy between tools:** The output from one tool becomes clipboard content. Use it as input for another tool!

✅ **Batch cleaning:** Process multiple HTML snippets in one session - just choose another tool or repeat the same one.

✅ **Preview before applying:** Review the statistics to decide if changes are appropriate before pasting the clipboard content.

✅ **Inspect what was removed:** Each tool shows exactly what was deleted so you can understand the changes.

---

## Troubleshooting

**Q: No HTML detected error**

- Make sure your HTML contains at least one `<` and `>` character
- Paste on a new line after the prompt

**Q: Spaces being removed incorrectly**

- Space Cleaner is aggressive but preserves text spacing
- If you need complete safety, manually review the output

**Q: HREF Analyzer not finding links**

- Make sure you have `<a href="...">` tags
- Anchors without href attributes are skipped

---

## Architecture Principles

This toolkit follows your workspace guidelines:

✅ **Single Responsibility** - Each function does one thing  
✅ **Dependency Injection** - All dependencies passed explicitly  
✅ **Composition** - Modules composed, not inherited  
✅ **Immutable Data** - Results returned as dataclasses  
✅ **Fail Fast** - Input validation at function entry  
✅ **Separation of Concerns** - Business logic separate from UI

---

**Enjoy cleaner HTML!** 🎉
