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
from .cleaners import find_duplicates, clean_duplicates, convert_columns, frequent_non_null, clean_amount, normalize_german_level, convert_to_seconds, convert_to_minutes, convert_to_hours
from .data_io import load_files, save_table_as_png, save_plot, save_clean_data
from .my_palette import get_my_palette, cmap_cornflower, cmap_lime, cmap_tomato, cmap_yellow, cmap_lavender, cmap_neutral
from .descriptive_stats import describe_num, describe_cat, compare_distributions, plot_change

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
    'convert_to_minutes',
    'convert_to_hours',
    'load_files',
    'save_table_as_png',
    'save_plot',
    'save_clean_data',
    'get_my_palette',
    'cmap_cornflower',
    'cmap_lime',
    'cmap_tomato',
    'cmap_yellow',
    'cmap_lavender',
    'cmap_neutral',
    'describe_num',
    'describe_cat',
    'compare_distributions',
    'plot_change'
]
