"""
HTML Cleaning Toolkit - Core Modules

This package contains the core cleaning utilities:
- garbage_cleaner: Remove scripts, styles, and unnecessary attributes
- space_cleaner: Remove unnecessary whitespace between tags
- href_analyzer: Review and fix href attributes
"""

from .garbage_cleaner import clean_html, run_garbage_cleaner, CleaningResult
from .space_cleaner import clean_spaces, run_space_cleaner
from .href_analyzer import run_href_analyzer

__all__ = [
    'clean_html',
    'run_garbage_cleaner',
    'CleaningResult',
    'clean_spaces',
    'run_space_cleaner',
    'run_href_analyzer',
]
