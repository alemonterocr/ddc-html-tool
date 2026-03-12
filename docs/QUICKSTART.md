# Project Structure Summary

## Files Overview

```
c:\Users\Ale-CodeRoad\Desktop\Optimizers\projects\
├── main.py                      ← START HERE: Main menu orchestrator
├── garbage_cleaner.py           ← Module 1: Remove scripts, styles, attributes
├── space_cleaner.py             ← Module 2: Remove unnecessary whitespace
├── href_analyzer.py             ← Module 3: Fix broken href references
├── README.md                    ← Full documentation
├── test_modules.py              ← Unit tests for all modules
│
├── [Legacy files - optional cleanup]
├── html-cleaner.py              ← Original interactive clipboard monitor
├── space-remover.py             ← Original space remover
├── hrefs-analyzer.py            ← Original HREF analyzer
│
└── [Test/sample files]
    ├── test-input.txt
    ├── menu-test-input.txt

```

## How to Use

### Start the Menu

```powershell
cd c:\Users\Ale-CodeRoad\Desktop\Optimizers\projects
python main.py
```

### Features by Tool

1. **Garbage Cleaner** (Option 1)
   - Removes: `<script>`, `<style>`, garbage attributes
   - Keeps: `class`, `href` on `<a>` tags
   - Output includes detailed statistics

2. **Space Cleaner** (Option 2)
   - Removes: Unnecessary whitespace between tags
   - Preserves: Meaningful spaces around inline elements
   - Safe minification without breaking text flow

3. **HREF Analyzer** (Option 3)
   - Detects: Incomplete or missing `.htm`/`.html` extensions
   - Interactive: Lets you fix each link individually
   - Updates: BeautifulSoup-parsed HTML with your changes

## Architecture

✅ **Modular Design**

- Each tool is independent
- Can be used individually or via menu
- Easy to extend with new tools

✅ **Clean Code Principles**

- Single Responsibility (each module has one purpose)
- Dependency Injection (no globals)
- Pure Functions (clean_html, clean_spaces return values)
- Separated Concerns (UI separate from logic)

✅ **Clipboard Integration**

- Input: Paste multi-line HTML
- Process: Clean it
- Output: Automatically copied to clipboard

## Installation

```powershell
# Install dependencies
pip install rich beautifulsoup4

# Run the toolkit
python main.py
```

## Sample Workflow

```
1. Start: python main.py
2. Choose: Option 1 (Garbage Cleaner)
3. Paste: Your messy HTML
4. Review: Statistics showing what was removed
5. Check: Clipboard contains cleaned HTML
6. Choose: Option 2 (Space Cleaner)
7. Paste: Same HTML or new HTML
8. Review: Space reduction statistics
9. Choose: Option 3 (HREF Analyzer)
10. Paste: HTML with anchor tags
11. Fix: Review and update broken links interactively
12. Exit: Option 4
```

## Module Dependencies

```
main.py
├── garbage_cleaner.py
│   ├── rich (Display formatting)
│   ├── html.parser (Parse HTML)
│
├── space_cleaner.py
│   ├── rich (Display formatting)
│   ├── re (Regex for space removal)
│
└── href_analyzer.py
    ├── rich (Display formatting, prompts)
    └── beautifulsoup4 (Parse HTML, find tags)
```

## Next Steps (Optional)

1. **Add to PATH** - Create a batch file to run from anywhere
2. **Extend Tools** - Add new transformations as separate modules
3. **Batch Processing** - Create a wrapper to process multiple files
4. **Web Version** - Port to Flask/FastAPI for browser-based access

---

**Your toolkit is ready to use!** Each tool is production-ready and follows clean architecture best practices. 🚀
