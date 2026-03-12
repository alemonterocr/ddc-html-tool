#!/usr/bin/env python3
"""
HTML Body Cleaner Utility - Interactive Clipboard Monitor
Monitors clipboard for HTML content, cleans it automatically, and returns result to clipboard.
Uses 'rich' for hacker-style CLI aesthetics.
"""

import sys
import re
import subprocess
from html.parser import HTMLParser
from io import StringIO
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table


@dataclass
class CleaningResult:
    """Immutable result of HTML cleaning operation."""
    cleaned_html: str
    original_size: int
    cleaned_size: int
    script_style_removed: int
    attributes_removed: int
    
    @property
    def size_reduction(self) -> int:
        """Calculate total characters removed."""
        return self.original_size - self.cleaned_size
    
    @property
    def reduction_percent(self) -> float:
        """Calculate percentage reduction."""
        return (self.size_reduction / self.original_size * 100) if self.original_size > 0 else 0


class HTMLCleaner(HTMLParser):
    """Pure HTML parser and cleaner. Single Responsibility: clean HTML only."""
    
    def __init__(self):
        super().__init__()
        self.output = StringIO()
        self.skip_content = False
        self.current_tag = None
        self.script_style_removed = 0
        self.attributes_removed = 0
    
    def handle_starttag(self, tag, attrs):
        """Handle opening tags, filtering attributes based on tag type."""
        tag_lower = tag.lower()
        self.current_tag = tag_lower
        
        # Skip script and style tags entirely
        if tag_lower in ('script', 'style'):
            self.skip_content = True
            self.script_style_removed += 1
            return
        
        # Determine which attributes to keep based on tag type
        original_attr_count = len(attrs)
        filtered_attrs = self._filter_attributes(tag_lower, attrs)
        self.attributes_removed += original_attr_count - len(filtered_attrs)
        
        # Write opening tag with filtered attributes
        self.output.write(f'<{tag}')
        for name, value in filtered_attrs:
            if value:
                self.output.write(f' {name}="{value}"')
            else:
                self.output.write(f' {name}')
        self.output.write('>')
    
    def _filter_attributes(self, tag, attrs):
        """Filter attributes based on tag type.
        
        Preserve 'href' only on anchor tags, 'class' on all tags.
        Remove all other attributes.
        """
        allowed_attrs = set()
        
        # href only allowed on anchor tags
        if tag == 'a':
            allowed_attrs.add('href')
        
        # class allowed on all tags
        allowed_attrs.add('class')
        
        return [(name, value) for name, value in attrs 
                if name.lower() in allowed_attrs]
    
    def handle_endtag(self, tag):
        """Handle closing tags."""
        tag_lower = tag.lower()
        
        # Don't output closing tags for script/style
        if tag_lower in ('script', 'style'):
            self.skip_content = False
            return
        
        self.output.write(f'</{tag}>')
        self.current_tag = None
    
    def handle_data(self, data):
        """Handle text content, collapsing redundant whitespace."""
        if not self.skip_content:
            lines = data.split('\n')
            lines = [line.strip() for line in lines]
            lines = [line for line in lines if line]
            
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
    
    def get_result(self) -> str:
        """Return cleaned HTML."""
        result = self.output.getvalue()
        # Final whitespace consolidation
        result = re.sub(r'\s+', ' ', result)
        return result.strip()


def clean_html(html_content: str) -> CleaningResult:
    """Clean HTML content. Pure function: no side effects or dependencies.
    
    Args:
        html_content: Raw HTML to clean
        
    Returns:
        CleaningResult with cleaned HTML and statistics
        
    Raises:
        Exception: If HTML parsing fails
    """
    original_size = len(html_content)
    cleaner = HTMLCleaner()
    
    try:
        cleaner.feed(html_content)
    except Exception as e:
        raise Exception(f"HTML parsing failed: {e}")
    
    cleaned_html = cleaner.get_result()
    
    return CleaningResult(
        cleaned_html=cleaned_html,
        original_size=original_size,
        cleaned_size=len(cleaned_html),
        script_style_removed=cleaner.script_style_removed,
        attributes_removed=cleaner.attributes_removed
    )


def get_clipboard() -> str:
    """Get text from Windows clipboard using PowerShell."""
    try:
        result = subprocess.run(
            ['powershell', '-Command', 'Get-Clipboard'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout
        return ""
    except Exception:
        return ""


def set_clipboard(text: str) -> bool:
    """Set text to Windows clipboard using clip command."""
    try:
        process = subprocess.Popen(
            ['clip'],
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        process.communicate(text.encode('utf-8'), timeout=5)
        return process.returncode == 0
    except Exception:
        return False


def read_html_from_user() -> str:
    """Read multi-line HTML input from user.
    
    Prompts user to paste HTML and reads until:
    - They press Enter twice (blank line after content), OR
    - EOF is reached
    Returns the collected HTML content.
    """
    console = Console()
    console.print("[green bold]→ Paste your HTML (press Enter twice when done):[/green bold]")
    
    lines = []
    blank_line_count = 0
    
    try:
        for line in sys.stdin:
            # Remove newline character but preserve the line content
            line = line.rstrip('\n\r')
            
            if line.strip() == "":
                blank_line_count += 1
                # Only stop if we have content AND we see a blank line
                if lines and blank_line_count >= 1:
                    break
            else:
                blank_line_count = 0
                lines.append(line)
                
    except KeyboardInterrupt:
        raise Exception("Input cancelled by user")
    
    return '\n'.join(lines)


def display_results(console: Console, result: CleaningResult) -> None:
    """Display cleaning results using rich formatting."""
    # Status message
    status_text = Text("✓ HTML Cleaned Successfully", style="bold green")
    console.print(Panel(status_text, border_style="green"))
    
    # Statistics in compact table format
    table = Table(show_header=False, show_footer=False, box=None)
    table.add_row("[green]Original:[/green]", f"{result.original_size:,} chars")
    table.add_row("[green]Cleaned:[/green]", f"{result.cleaned_size:,} chars")
    table.add_row("[green]Reduction:[/green]", f"{result.size_reduction:,} chars ({result.reduction_percent:.1f}%)")
    table.add_row("[green]Scripts/Styles:[/green]", f"{result.script_style_removed} removed")
    table.add_row("[green]Attributes:[/green]", f"{result.attributes_removed} removed")
    
    console.print(Panel(
        table,
        title="[bold green]📊 Cleanup Stats[/bold green]",
        border_style="green"
    ))


def main() -> None:
    """Main entry point - interactive CLI waiting for user input."""
    console = Console()
    
    # Display startup header
    title_text = Text("HTML CLEANER", style="bold green")
    console.print(Panel(title_text, border_style="green"))
    
    try:
        while True:
            # Wait for user to paste HTML
            try:
                html_content = read_html_from_user()
            except Exception as e:
                if "cancelled" in str(e).lower():
                    console.print("\n[green bold]✓ Exiting HTML Cleaner[/green bold]")
                    sys.exit(0)
                console.print(f"[red]✗ Error reading input: {e}[/red]")
                continue
            
            # Check if we got valid HTML
            if not html_content.strip():
                # EOF reached, exit gracefully
                console.print("\n[green bold]✓ Exiting HTML Cleaner[/green bold]")
                sys.exit(0)
            
            if '<' not in html_content or '>' not in html_content:
                console.print("[yellow]⚠ No HTML detected. Make sure you paste valid HTML.\n[/yellow]")
                continue
            
            # Clean the HTML
            try:
                result = clean_html(html_content)
                
                # Update clipboard with cleaned HTML
                success = set_clipboard(result.cleaned_html)
                
                if success:
                    # Display results
                    display_results(console, result)
                    console.print("[green bold]✓ Copied to clipboard![/green bold]\n")
                else:
                    console.print("[yellow]⚠ Warning: Could not update clipboard[/yellow]\n")
                    
            except Exception as e:
                console.print(f"[red]✗ Error cleaning HTML: {e}[/red]\n")
                
    except KeyboardInterrupt:
        console.print("\n[green bold]✓ Exiting HTML Cleaner[/green bold]")
        sys.exit(0)


if __name__ == '__main__':
    main()
