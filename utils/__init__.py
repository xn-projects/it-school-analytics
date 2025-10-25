"""
Utility package for the IT School Analytics project.

Includes:
- Logging setup and DataFrame display helpers
- Data summary and cleaning tools
- Input/output utilities for loading files, saving tables, plots, and datasets
- General helper functions (logging sections, duplicate cleaning)
"""

from .logging_setup import setup_logging, show_df, log_section
from .data_summary import DataSummary
from .cleaners import find_duplicates, clean_duplicates, convert_columns, frequent_non_null, clean_amount, normalize_german_level, convert_to_seconds
from .data_io import load_files, save_table_as_png, save_plot, save_clean_data

__all__ = [
    'setup_logging',
    'show_df',
    'log_section',
    'DataSummary',
    'find_duplicates',
    'clean_duplicates',
    'convert_columns'
    'frequent_non_null',
    'clean_amount',
    'normalize_german_level',
    'convert_to_seconds',
    'load_files',
    'save_table_as_png',
    'save_plot',
    'save_clean_data',
]
