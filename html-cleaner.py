#!/usr/bin/env python3
"""
HTML Body Cleaner Utility
Removes script/style tags, redundant whitespace, and unnecessary HTML attributes.
Reads from clipboard, outputs cleaned HTML back to clipboard, shows statistics.
"""

import sys
import re
import subprocess
from html.parser import HTMLParser
from io import StringIO


def get_clipboard():
    """Get text from Windows clipboard using built-in commands."""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-Clipboard'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout
        else:
            raise Exception("Failed to read clipboard")
    except Exception as e:
        print(f"Error reading clipboard: {e}", file=sys.stderr)
        sys.exit(1)


def set_clipboard(text):
    """Set text to Windows clipboard using built-in commands."""
    try:
        process = subprocess.Popen(
            ['clip'],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        process.communicate(text.encode('utf-8'), timeout=5)
        if process.returncode != 0:
            raise Exception("Failed to write to clipboard")
    except Exception as e:
        print(f"Error writing to clipboard: {e}", file=sys.stderr)
        sys.exit(1)


class HTMLCleaner(HTMLParser):
    """Custom HTML parser to clean and rebuild HTML."""
    
    def __init__(self):
        super().__init__()
        self.output = StringIO()
        self.skip_content = False
        self.script_style_removed = 0
        self.attributes_removed = 0
    
    def handle_starttag(self, tag, attrs):
        """Handle opening tags."""
        tag_lower = tag.lower()
        
        # Skip script and style tags entirely
        if tag_lower in ('script', 'style'):
            self.skip_content = True
            self.script_style_removed += 1
            return
        
        # Filter attributes: keep only 'class' attribute
        original_attr_count = len(attrs)
        filtered_attrs = [(name, value) for name, value in attrs if name.lower() == 'class']
        self.attributes_removed += original_attr_count - len(filtered_attrs)
        
        # Write tag
        self.output.write(f'<{tag}')
        for name, value in filtered_attrs:
            if value:
                self.output.write(f' {name}="{value}"')
            else:
                self.output.write(f' {name}')
        self.output.write('>')
    
    def handle_endtag(self, tag):
        """Handle closing tags."""
        tag_lower = tag.lower()
        
        # Don't output closing tags for script/style
        if tag_lower in ('script', 'style'):
            self.skip_content = False
            return
        
        self.output.write(f'</{tag}>')
    
    def handle_data(self, data):
        """Handle text content."""
        if not self.skip_content:
            # Collapse whitespace: strip lines and join with single space
            lines = data.split('\n')
            lines = [line.strip() for line in lines]
            lines = [line for line in lines if line]  # Remove empty lines
            
            if lines:
                self.output.write(' '.join(lines))
    
    def handle_entityref(self, name):
        """Handle HTML entities."""
        if not self.skip_content:
            self.output.write(f'&{name};')
    
    def handle_charref(self, name):
        """Handle character references."""
        if not self.skip_content:
            self.output.write(f'&#{name};')
    
    def get_result(self):
        """Return cleaned HTML."""
        return self.output.getvalue()


def clean_html(html_content):
    """Clean HTML content and return result with statistics."""
    cleaner = HTMLCleaner()
    
    try:
        cleaner.feed(html_content)
    except Exception as e:
        print(f"Error parsing HTML: {e}", file=sys.stderr)
        sys.exit(1)
    
    result = cleaner.get_result()
    
    # Final whitespace consolidation
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()
    
    return result, cleaner


def main():
    """Main entry point."""
    print("HTML Body Cleaner")
    print("=" * 60)
    
    # Get HTML from clipboard
    print("📋 Reading from clipboard...")
    html_content = get_clipboard()
    
    if not html_content.strip():
        print("❌ Error: Clipboard is empty", file=sys.stderr)
        sys.exit(1)
    
    original_size = len(html_content)
    print(f"   Original size: {original_size:,} characters")
    
    # Clean HTML
    print("🧹 Cleaning HTML...")
    cleaned_html, cleaner = clean_html(html_content)
    
    cleaned_size = len(cleaned_html)
    size_reduction = original_size - cleaned_size
    reduction_percent = (size_reduction / original_size * 100) if original_size > 0 else 0
    
    print(f"   Cleaned size: {cleaned_size:,} characters")
    print(f"   Reduction: {size_reduction:,} characters ({reduction_percent:.1f}%)")
    
    # Display statistics
    print("\n🗑️  Garbage Deleted:")
    print(f"   - Script/Style tags removed: {cleaner.script_style_removed}")
    print(f"   - HTML attributes removed: {cleaner.attributes_removed}")
    
    # Set clipboard
    print("\n📋 Copying cleaned HTML to clipboard...")
    set_clipboard(cleaned_html)
    print("✅ Done! Cleaned HTML is ready in your clipboard")


if __name__ == '__main__':
    main()
