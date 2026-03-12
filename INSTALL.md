# Installation & Usage Guide

## Quick Start (Recommended for Windows Users)

### Option 1: Download Standalone Executable

1. Go to [Releases](https://github.com/alemonterocr/html-cleaning-toolkit/releases)
2. Download `html-cleaner.exe` or `html-cleaner-win64.zip`
3. Run `html-cleaner.exe` directly (no installation needed!)

**That's it!** No Python installation required.

### Option 2: Install from GitHub (For Developers)

```bash
git clone https://github.com/alemonterocr/html-cleaning-toolkit
cd html-cleaning-toolkit
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .
python main.py
```

### Option 3: Use Python Package (If Python Installed)

If you have Python 3.10+ installed:

```bash
pip install html-cleaning-toolkit
html-cleaner
```

## System Requirements

**For Executable (.exe):**

- Windows 7 or newer
- ~100 MB disk space (self-contained)
- **NO Python installation required!**

**For Python Installation:**

- Python 3.10 or higher (3.13 recommended)
- ~50 MB disk space (with dependencies)
- Windows, macOS, or Linux

## First Run

1. **Launch the toolkit**

   ```bash
   html-cleaner
   ```

   Or if not installed:

   ```bash
   python main.py
   ```

2. **Choose a tool** (1-4)
   - **1**: Garbage Cleaner
   - **2**: Space Cleaner
   - **3**: HREF Analyzer
   - **4**: Exit

3. **Paste your HTML** (Ctrl+V or right-click paste)
   - Press **Enter twice** when done

4. **Result is automatically copied to clipboard!**
   - Paste anywhere (Ctrl+V)

## Examples

### Garbage Cleaner

Input:

```html
<div class="container">
  <script>
    alert("XSS");
  </script>
  <p id="toxic" style="color:red;">Hello</p>
</div>
```

Output:

```html
<div class="container">
  <p>Hello</p>
</div>
```

### Space Cleaner

Input:

```html
<div>
  <p>Text</p>
</div>
```

Output:

```html
<div><p>Text</p></div>
```

### HREF Analyzer

Interactively fixes broken links:

```
Text: Click Here
Current: /page
New Href: /page.html
```

## Troubleshooting

### "Command not found: html-cleaner"

The package didn't install properly. Try:

```bash
pip install --upgrade html-cleaning-toolkit
```

### Clipboard issues (Windows)

The tool uses PowerShell's `clip` command. Ensure you have:

- Windows Clipboard access enabled
- PowerShell installed (default on Windows)

### Python version error

Ensure you have Python 3.10+:

```bash
python --version
```

Upgrade if needed from [python.org](https://www.python.org/downloads/)

## Command Line Arguments

Future versions will support batch processing:

```bash
html-cleaner --input input.html --output output.html --mode garbage
```

## Getting Help

- **Documentation**: [github.com/.../docs/README.md](.)
- **Issues**: [github.com/.../issues](https://github.com)
- **Discussions**: [github.com/.../discussions](https://github.com)

## What's Included

✅ Garbage Cleaner - Remove junk HTML
✅ Space Cleaner - Optimize whitespace
✅ HREF Analyzer - Fix broken links
✅ Clipboard integration
✅ Rich CLI formatting
✅ Comprehensive test suite

## Advanced: Development Installation

For contributing or extending:

```bash
git clone https://github.com/alemonterocr/html-cleaning-toolkit
cd html-cleaning-toolkit
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e ".[dev]"
python tests/validate.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for more.
