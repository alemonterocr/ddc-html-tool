"""
HTML Garbage Cleaner Module
Removes script/style tags, redundant whitespace, and unnecessary HTML attributes.
Preserves 'href' on <a> tags and 'class' on all tags.
"""

import sys
import re
from html.parser import HTMLParser
from html.entities import name2codepoint, codepoint2name
from io import StringIO
from dataclasses import dataclass
import html

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
    entities_removed: int
    
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
        super().__init__(convert_charrefs=False)  # Don't auto-convert entities
        self.output = StringIO()
        self.skip_content = False
        self.current_tag = None
        self.script_style_removed = 0
        self.attributes_removed = 0
        self.entities_removed = 0  # Will be set in get_result()
    
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
        """Handle text content, preserving original spacing."""
        if not self.skip_content:
            self.output.write(data)
    
    def handle_entityref(self, name):
        """Handle HTML entities by reconstructing them."""
        if not self.skip_content:
            # Preserve entities (nbsp will be removed in get_result)
            if name in name2codepoint:
                self.output.write(f'&{name};')
            else:
                self.output.write(f'&{name};')
    
    def handle_charref(self, name):
        """Handle character references (numeric entities like &#160;)."""
        if not self.skip_content:
            # Reconstruct the character reference properly
            try:
                # Handle both decimal and hex references
                if name.startswith('x') or name.startswith('X'):
                    code = int(name[1:], 16)
                else:
                    code = int(name)
                # Write the character reference to preserve the entity format
                self.output.write(f'&#{name};')
            except ValueError:
                # Fallback - shouldn't happen with valid HTML
                self.output.write(f'&#{name};')
    
    def get_result(self) -> str:
        """Return cleaned HTML with proper entity encoding and &nbsp; removal."""
        result = self.output.getvalue()
        
        # Count and remove &nbsp; entities (before conversion)
        nbsp_count = result.count('&nbsp;')
        self.entities_removed = nbsp_count
        result = result.replace('&nbsp;', '')
        
        # Remove the non-breaking space character (U+00A0) that HTMLParser converts from &nbsp;
        nbsp_char = '\xa0'  # Non-breaking space
        result = result.replace(nbsp_char, '')
        
        # Ensure proper handling of special characters and entities
        # Map common Unicode characters to their HTML entity equivalents
        entity_map = {
            '\u2013': '&ndash;',  # En dash
            '\u2014': '&mdash;',  # Em dash
            '\u2019': '&rsquo;',  # Right single quotation
            '\u201c': '&ldquo;',  # Left double quotation
            '\u201d': '&rdquo;',  # Right double quotation
        }
        
        # Replace special characters with proper HTML entities
        for char, entity in entity_map.items():
            result = result.replace(char, entity)
        
        return result


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
        attributes_removed=cleaner.attributes_removed,
        entities_removed=cleaner.entities_removed
    )


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
    table.add_row("[green]&nbsp; Entities:[/green]", f"{result.entities_removed} removed")
    
    console.print(Panel(
        table,
        title="[bold green]📊 Cleanup Stats[/bold green]",
        border_style="green"
    ))


def run_garbage_cleaner() -> str:
    """Run the garbage cleaner interactively. Returns cleaned HTML."""
    console = Console()
    
    # Display header
    title_text = Text("HTML GARBAGE CLEANER", style="bold green")
    console.print(Panel(title_text, border_style="green"))
    
    # Read HTML from stdin
    console.print("[green bold]→ Paste your HTML (press Enter twice when done):[/green bold]")
    
    lines = []
    blank_line_count = 0
    
    try:
        for line in sys.stdin:
            line = line.rstrip('\n\r')
            
            if line.strip() == "":
                blank_line_count += 1
                if lines and blank_line_count >= 1:
                    break
            else:
                blank_line_count = 0
                lines.append(line)
                
    except KeyboardInterrupt:
        raise Exception("Input cancelled by user")
    
    html_content = '\n'.join(lines)
    
    # Validate input
    if not html_content.strip():
        console.print("[red]✗ No HTML input provided[/red]")
        return ""
    
    if '<' not in html_content or '>' not in html_content:
        console.print("[yellow]⚠ No HTML detected[/yellow]")
        return ""
    
    # Clean HTML
    try:
        result = clean_html(html_content)
        display_results(console, result)
        console.print("[green bold]✓ Copied to clipboard![/green bold]\n")
        return result.cleaned_html
    except Exception as e:
        console.print(f"[red]✗ Error cleaning HTML: {e}[/red]")
        return ""
