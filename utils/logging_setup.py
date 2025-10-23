import logging
import os
from datetime import datetime


def setup_logging(level: int = logging.INFO, log_dir: str = 'logs') -> None:
    """
    Configure logging for the project.

    Creates a directory for log files and writes log messages

    Parameters
    ----------
    level : int, optional
        Logging level (default is logging.INFO).
    log_dir : str, optional
        Directory where log files will be stored (default is "logs").

    Returns
    -------
    None
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
    Display a pandas DataFrame in Jupyter or Google Colab.

    Prints a short overview with the DataFrame name, shape, and a few sample rows.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to display.
    name : str, optional
        Custom name for the DataFrame (default is 'DataFrame').
    max_rows : int, optional
        Maximum number of rows to display (default is 5).

    Returns
    -------
    None
    """
    from IPython.display import display, HTML
    display(HTML(f'<b>{name}</b> ({df.shape[0]} rows × {df.shape[1]} columns)'))
    display(df.head(max_rows))
