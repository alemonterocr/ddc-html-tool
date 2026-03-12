"""
HREF Analyzer Module
Analyzes and fixes HTML href attributes in anchor tags.
Allows users to review and update broken or incomplete href references.
"""

import sys
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


@dataclass
class AnalysisResult:
    """Result of href analysis."""
    updated_html: str
    broken_links_fixed: int
    total_problems_found: int


def read_html_from_stdin(console: Console) -> str:
    """Read HTML from stdin until double Enter. Returns empty string if cancelled."""
    console.print("[magenta bold]→ Paste your HTML (press Enter twice when done):[/magenta bold]")
    
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
        console.print("[red]✗ Input cancelled[/red]")
        return ""
    
    return '\n'.join(lines)


def validate_html_string(html_content: str) -> bool:
    """Check if string contains valid HTML markup."""
    return '<' in html_content and '>' in html_content


def is_special_href(href: str) -> bool:
    """True if href is anchor, email, phone, or JavaScript (skip these)."""
    special_prefixes = ('#', 'mailto:', 'tel:', 'javascript:')
    return not href or href.startswith(special_prefixes)


def needs_fixing(href: str) -> bool:
    """True if href is missing proper file extension."""
    clean_href = href.split('?')[0].rstrip('/')
    valid_extensions = ('.htm', '.html')
    return not clean_href.lower().endswith(valid_extensions)


def find_broken_links(soup: BeautifulSoup) -> list:
    """Find all anchor tags with problematic href values."""
    all_links = soup.find_all('a', href=True)
    
    broken_links = []
    for link in all_links:
        href = link['href'].strip()
        
        if is_special_href(href):
            continue
        
        if needs_fixing(href):
            broken_links.append(link)
    
    return broken_links


def get_link_display_text(tag: Tag, max_length: int = 40) -> str:
    """Extract displayable text from link tag."""
    text = (tag.text.strip() or "[Image/No Text]")
    return text[:max_length]


def display_broken_links_table(console: Console, broken_links: list) -> None:
    """Display summary table of broken links."""
    console.print(f"\n[bold yellow]Found {len(broken_links)} links needing updates:[/bold yellow]")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Link Text", style="cyan", width=30)
    table.add_column("Current Href", style="red")
    
    for tag in broken_links:
        text = get_link_display_text(tag, max_length=30)
        table.add_row(text, tag['href'])
    
    console.print(table)
    console.print("\n[bold]Let's fix them. (Press ENTER to keep original link)[/bold]\n")


def fix_broken_links_interactively(console: Console, broken_links: list) -> int:
    """Interactively fix each broken link. Returns count of fixed links."""
    fixed_count = 0
    
    for tag in broken_links:
        current_href = tag['href']
        text = get_link_display_text(tag)
        
        console.print(f"[cyan]Text:[/cyan] {text}")
        new_href = Prompt.ask(f"[red]Current:[/red] {current_href}\n[green]New Href[/green]")
        
        if new_href.strip():
            tag['href'] = new_href.strip()
            fixed_count += 1
        
        console.print()
    
    return fixed_count


def run_href_analyzer() -> str:
    """Orchestrate href analysis and fixing. Returns updated HTML."""
    console = Console()
    
    # Display header
    title_text = Text("HREF ANALYZER", style="bold magenta")
    console.print(Panel(title_text, border_style="magenta"))
    
    # Read input
    html_content = read_html_from_stdin(console)
    
    if not html_content.strip():
        console.print("[red]✗ No HTML input provided[/red]")
        return ""
    
    if not validate_html_string(html_content):
        console.print("[yellow]⚠ No HTML detected[/yellow]")
        return ""
    
    # Parse and analyze
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        broken_links = find_broken_links(soup)
        
        if not broken_links:
            status = Text("✓ All hrefs look good!", style="bold magenta")
            console.print(Panel(status, border_style="magenta"))
            return str(soup)
        
        # Display and fix
        display_broken_links_table(console, broken_links)
        fixed_count = fix_broken_links_interactively(console, broken_links)
        
        # Report results
        updated_html = str(soup)
        status = Text(f"✓ Updated {fixed_count} hrefs", style="bold magenta")
        console.print(Panel(status, border_style="magenta"))
        console.print("[magenta bold]✓ Copied to clipboard![/magenta bold]\n")
        
        return updated_html
        
    except Exception as e:
        console.print(f"[red]✗ Error processing HTML: {e}[/red]")
        return ""
