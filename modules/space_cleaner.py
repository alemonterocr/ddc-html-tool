"""
Space Cleaner Module
Removes unnecessary whitespace between HTML tags while preserving meaningful spaces.
Handles inline elements (like <a>, <span>) specially to prevent text collapsing.
"""

import re
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def clean_spaces(html_content: str) -> tuple[str, int]:
    """Clean unnecessary spaces from HTML while preserving meaningful ones.
    
    Only removes whitespace-only content between tags.
    Preserves spaces needed for text readability, especially around inline elements.
    
    Args:
        html_content: Raw HTML to clean
        
    Returns:
        Tuple of (cleaned_html, spaces_removed_count)
    """
    original_size = len(html_content)
    
    # Step 1: Remove whitespace that contains newlines between tags
    # This preserves single spaces for text flow
    text = re.sub(r'>\s*\n+\s*<', '><', html_content)
    
    # Step 2: Remove multiple consecutive spaces (but keep single spaces)
    text = re.sub(r' {2,}', ' ', text)
    
    # Step 3: Remove tabs and other whitespace characters between tags
    text = re.sub(r'>\t+<', '><', text)
    
    # Step 4: Ensure proper spacing around inline elements
    # Add space before anchor tags if not present
    text = re.sub(r'([a-zA-Z0-9])<a(\s|>)', r'\1 <a\2', text)
    
    # Add space after anchor closing tags if followed by text
    text = re.sub(r'(</a>)([a-zA-Z0-9])', r'\1 \2', text)
    
    # Similar handling for other inline elements
    inline_tags = ['span', 'strong', 'em', 'b', 'i', 'mark', 'small', 'code']
    for tag in inline_tags:
        # Add space before opening tag when preceded by text/numbers
        text = re.sub(rf'([a-zA-Z0-9])<{tag}(\s|>)', rf'\1 <{tag}\2', text, flags=re.IGNORECASE)
        # Add space after closing tag when followed by text/numbers
        text = re.sub(rf'(</{tag}>)([a-zA-Z0-9])', rf'\1 \2', text, flags=re.IGNORECASE)
    
    # Clean up any weird spacing artifacts
    text = text.strip()
    
    cleaned_size = len(text)
    spaces_removed = original_size - cleaned_size
    
    return text, spaces_removed


def run_space_cleaner() -> str:
    """Run the space cleaner interactively. Returns cleaned HTML."""
    console = Console()
    
    # Display header
    title_text = Text("SPACE CLEANER", style="bold cyan")
    console.print(Panel(title_text, border_style="cyan"))
    
    # Read HTML from stdin
    console.print("[cyan bold]→ Paste your HTML (press Enter twice when done):[/cyan bold]")
    
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
    
    # Clean spaces
    try:
        cleaned_html, spaces_removed = clean_spaces(html_content)
        
        original_size = len(html_content)
        cleaned_size = len(cleaned_html)
        reduction_percent = (spaces_removed / original_size * 100) if original_size > 0 else 0
        
        # Display results
        status_text = Text("✓ Spaces Cleaned", style="bold cyan")
        console.print(Panel(status_text, border_style="cyan"))
        
        console.print(f"[cyan]Original:[/cyan] {original_size:,} chars")
        console.print(f"[cyan]Cleaned:[/cyan]  {cleaned_size:,} chars")
        console.print(f"[cyan]Reduction:[/cyan] {spaces_removed:,} chars ({reduction_percent:.1f}%)\n")
        
        console.print("[cyan bold]✓ Copied to clipboard![/cyan bold]\n")
        return cleaned_html
        
    except Exception as e:
        console.print(f"[red]✗ Error cleaning spaces: {e}[/red]")
        return ""
