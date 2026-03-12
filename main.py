#!/usr/bin/env python3
"""
HTML Cleaning Toolkit - Main Entry Point
Orchestrates three HTML cleaning utilities:
1. Garbage Cleaner - Removes scripts, styles, and unnecessary attributes
2. Space Cleaner - Removes excessive whitespace between tags
3. HREF Analyzer - Reviews and fixes href attributes
"""

import sys
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

# Import modules from the modules folder
sys.path.insert(0, 'modules')
from garbage_cleaner import run_garbage_cleaner
from space_cleaner import run_space_cleaner
from href_analyzer import run_href_analyzer


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


def display_menu() -> None:
    """Display the main menu options."""
    console = Console()
    
    title = Text("HTML CLEANING TOOLKIT", style="bold bright_white on blue")
    console.print(Panel(title, border_style="blue"))
    
    options = """
[bold cyan]1.[/bold cyan] [cyan]Garbage Cleaner[/cyan]
   Remove scripts, styles, and unnecessary attributes.
   Keeps: <a href> and <* class>
   
[bold cyan]2.[/bold cyan] [cyan]Space Cleaner[/cyan]
   Delete unnecessary spaces between tags.
   Preserves meaningful spaces around inline elements.
   
[bold cyan]3.[/bold cyan] [cyan]HREF Analyzer[/cyan]
   Review and fix broken href references.
   Interactive link fixing tool.
   
[bold red]4.[/bold red] [red]Exit[/red]
"""
    console.print(options)


def main() -> None:
    """Main entry point. Display menu and orchestrate tools."""
    console = Console()
    
    try:
        while True:
            display_menu()
            
            choice = Prompt.ask("[bold]Choose an option[/bold]", choices=["1", "2", "3", "4"])
            console.print()
            
            result = ""
            
            try:
                if choice == "1":
                    result = run_garbage_cleaner()
                elif choice == "2":
                    result = run_space_cleaner()
                elif choice == "3":
                    result = run_href_analyzer()
                elif choice == "4":
                    console.print("\n[green bold]✓ Goodbye![/green bold]")
                    sys.exit(0)
                
                # Copy result to clipboard if we got one
                if result:
                    if set_clipboard(result):
                        pass  # Already displayed by the module
                    else:
                        console.print("[yellow]⚠ Warning: Could not update clipboard[/yellow]\n")
                        
            except KeyboardInterrupt:
                console.print("\n[yellow]Operation cancelled[/yellow]\n")
            except Exception as e:
                console.print(f"[red]✗ Error: {e}[/red]\n")
            
            # Ask if user wants to continue
            again = Prompt.ask("\n[bold]Process another HTML[/bold]", choices=["y", "n"])
            if again.lower() != "y":
                console.print("\n[green bold]✓ Thank you for using HTML Toolkit![/green bold]")
                sys.exit(0)
            
            console.print()
    
    except KeyboardInterrupt:
        console.print("\n\n[green bold]✓ Exiting...[/green bold]")
        sys.exit(0)


if __name__ == '__main__':
    main()
