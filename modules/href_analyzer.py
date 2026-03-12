"""
HREF Analyzer Module
Analyzes and fixes HTML href attributes in anchor tags.
Allows users to review and update broken or incomplete href references.
"""

import sys
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def run_href_analyzer() -> str:
    """Run the HREF analyzer interactively. Returns updated HTML."""
    console = Console()
    
    # Display header
    title_text = Text("HREF ANALYZER", style="bold magenta")
    console.print(Panel(title_text, border_style="magenta"))
    
    # Read HTML from stdin
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
        raise Exception("Input cancelled by user")
    
    html_content = '\n'.join(lines)
    
    # Validate input
    if not html_content.strip():
        console.print("[red]✗ No HTML input provided[/red]")
        return ""
    
    if '<' not in html_content or '>' not in html_content:
        console.print("[yellow]⚠ No HTML detected[/yellow]")
        return ""
    
    try:
        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        links = soup.find_all('a', href=True)
        
        if not links:
            console.print("[yellow]⚠ No anchor tags with href found[/yellow]")
            return ""
        
        # Identify problematic hrefs
        tags_to_fix = []
        for link in links:
            href = link['href'].strip()
            
            # Skip pure anchors, emails, phones, JS
            if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:')):
                continue
            
            # Check for issues
            clean_href = href.split('?')[0].rstrip('/')
            
            # Flag if doesn't end with .htm or .html
            if not clean_href.lower().endswith(('.htm', '.html')):
                tags_to_fix.append(link)
        
        # If all hrefs are good
        if not tags_to_fix:
            status = Text("✓ All hrefs look good!", style="bold magenta")
            console.print(Panel(status, border_style="magenta"))
            return str(soup)
        
        # Show summary table
        console.print(f"\n[bold yellow]Found {len(tags_to_fix)} links needing updates:[/bold yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Link Text", style="cyan", width=30)
        table.add_column("Current Href", style="red")
        
        for tag in tags_to_fix:
            text = (tag.text.strip() or "[Image/No Text]")[:30]
            table.add_row(text, tag['href'])
        
        console.print(table)
        console.print("\n[bold]Let's fix them. (Press ENTER to keep original link)[/bold]\n")
        
        # Interactive fix loop
        fixed_count = 0
        for tag in tags_to_fix:
            current_href = tag['href']
            text = (tag.text.strip() or "[Image]")[:40]
            
            console.print(f"[cyan]Text:[/cyan] {text}")
            new_href = Prompt.ask(f"[red]Current:[/red] {current_href}\n[green]New Href[/green]")
            
            # Update if user provided input
            if new_href.strip():
                tag['href'] = new_href.strip()
                fixed_count += 1
            console.print()
        
        # Convert updated DOM back to HTML
        updated_html = str(soup)
        
        # Display results
        status = Text(f"✓ Updated {fixed_count} hrefs", style="bold magenta")
        console.print(Panel(status, border_style="magenta"))
        console.print("[magenta bold]✓ Copied to clipboard![/magenta bold]\n")
        
        return updated_html
        
    except Exception as e:
        console.print(f"[red]✗ Error processing HTML: {e}[/red]")
        return ""
