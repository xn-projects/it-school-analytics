import logging
import os
from datetime import datetime


def setup_logging(level: int = logging.INFO, log_dir: str = 'logs') -> None:
    """
    Configure logging for the project. Create a folder and write logs to file + console.
    """
    os.makedirs(log_dir, exist_ok=True)
    log_filename = f'log_{datetime.now():%Y-%m-%d_%H-%M-%S}.txt'
    log_path = os.path.join(log_dir, log_filename)

    logging.basicConfig(
        level=level,
        format='%(asctime)s — [%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_path, encoding="utf-8")
        ],
        force=True
    )

    logging.info(f'Logging started. File: {log_path}')


def show_df(df, name: str = 'DataFrame', max_rows: int = 5) -> None:
    """
    Display a pandas DataFrame or Series in Jupyter or Google Colab.
    Prints a short overview with the DataFrame name, shape, and a few sample rows.
    """
    from IPython.display import display, HTML
    import pandas as pd

    if isinstance(df, pd.Series):
        df = df.to_frame(name=df.name or 'value')

    display(HTML(f'<b>{name}</b> ({df.shape[0]} rows × {df.shape[1]} columns)'))
    display(df.head(max_rows))

def log_section(title):
    """
    Write a visible header section into logs for better structure.
    """
    logging.info('=' * 50)
    logging.info(f'{title}')
    logging.info('=' * 50)
