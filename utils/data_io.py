import os
import logging
import requests
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi
import textwrap


def load_files(base_url, files, target_folder='data/raw'):
    """
    Download Excel files from a given URL and save locally.
    """
    os.makedirs(target_folder, exist_ok=True)
    saved_files = []
    
    for f in files:
        url = base_url + f
        path = os.path.join(target_folder, f)
        
        r = requests.get(url)
        r.raise_for_status()
        
        with open(path, 'wb') as file:
            file.write(r.content)

        logging.info(f'File {f} downloaded to {path}')
        saved_files.append(path)

    return saved_files


def save_table_as_png(df, name, subfolder=None, folder='figures', add_index_column=True):
    """
    Save a DataFrame as a PNG image using dataframe_image with matplotlib backend.
    """ 
    df = df.copy()

    float_cols = df.select_dtypes(include='float')
    if not float_cols.empty:
        df[float_cols.columns] = df[float_cols.columns].round(1)

    if add_index_column:
        df.insert(
            0,
            '',
            ['\n'.join(textwrap.wrap(str(i), 18)) if isinstance(i, str) else i
             for i in df.index])
        df.reset_index(drop=True, inplace=True)

    rows, cols = df.shape
    width = max(8, cols * 1.5)
    height = max(2, rows * 0.4)
    plt.rcParams['figure.figsize'] = (width, height)
    plt.rcParams['figure.dpi'] = 300

    base_dir = subfolder if subfolder else '.'
    path_dir = os.path.join(base_dir, folder)
    os.makedirs(path_dir, exist_ok=True)
    path = os.path.join(path_dir, f'{name}.png')

    styled = (
        df.style
        .set_properties(**{
            'white-space': 'pre-wrap',
            'text-align': 'left',
            'font-size': '7pt'}))

    try:
        dfi.export(
            styled,
            path,
            table_conversion='matplotlib',
            dpi=300,
            max_rows=-1)
        plt.close('all')
        logging.info(f'Table saved as {path}')
    except Exception as e:
        logging.error(f'Failed to save table {name}: {e}')
        

def save_plot(name, subfolder=None, folder='figures', dpi=300, tight=True, fig=None):
    """
    Save the current matplotlib plot as a PNG.
    """
    base_dir = subfolder if subfolder else '.'
    path_dir = os.path.join(base_dir, folder)
    os.makedirs(path_dir, exist_ok=True)

    path = os.path.join(path_dir, f'{name}.png')
    if fig is None:
        fig = plt.gcf()
    if tight:
        plt.tight_layout()
    plt.savefig(path, dpi=dpi, bbox_inches='tight')
    logging.info(f'Plot saved as {path}')


def save_clean_data(df, name, folder='data/clean'):
    """
    Save a cleaned dataset as an Excel file (.xlsx) inside the data/clean folder.
    """
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{name}.xlsx')
    df.to_excel(path, index=False)
    logging.info(f'Cleaned dataset saved as {path}')


def save_styler_as_png(styler, name, subfolder=None, folder='figures'):
    """
    Saves a Styler as a PNG image, adding the first column from the index.
    """
    df = styler.data.copy()

    num_cols = df.select_dtypes(include='number').columns
    df[num_cols] = df[num_cols].round(decimals)

    df.insert(
        0,
        '',
        ['\n'.join(textwrap.wrap(str(i), 18)) if isinstance(i, str) else i
         for i in df.index]
    )
    df.reset_index(drop=True, inplace=True)

    export = new_styler.export()
    cleaned = [
        cell for cell in export.get('cellstyle', [])
        if not any('col0' in s for s in cell['selectors'])
    ]
    export['cellstyle'] = cleaned
    new_styler = df.style.use(export)
    new_styler = new_styler.format(f'{{:.{decimals}f}}', subset=num_cols)

    rows, cols = df.shape
    plt.rcParams['figure.figsize'] = (max(8, cols * 1.5), max(2, rows * 0.4))
    plt.rcParams['figure.dpi'] = 300

    base_dir = subfolder if subfolder else '.'
    path_dir = os.path.join(base_dir, folder)
    os.makedirs(path_dir, exist_ok=True)
    path = os.path.join(path_dir, f'{name}.png')

    try:
        dfi.export(
            new_styler,
            path,
            table_conversion='matplotlib',
            dpi=300,
            max_rows=-1
        )
        plt.close('all')
        logging.info(f'Table saved as {path}')
    except Exception as e:
        logging.error(f'Failed to save styled table {name}: {e}')
