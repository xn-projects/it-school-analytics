import os
import logging
import requests
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi

def load_files(base_url, files, target_folder='data'):
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
        
        with open(path, "wb") as file:
            file.write(r.content)

        logging.info(f'File "{f}" downloaded to {path}')
        saved_files.append(path)

    return saved_files


def save_table_as_png(df, name, subfolder=None, folder='figures'):
    """
    Save a DataFrame as a PNG image using dataframe_image with matplotlib backend.
    """
    base_dir = subfolder if subfolder else '.'
    path_dir = os.path.join(base_dir, folder)
    os.makedirs(path_dir, exist_ok=True)

    path = os.path.join(path_dir, f'{name}.png')
    dfi.export(df, path, table_conversion='matplotlib')
    logging.info(f'Table saved as {path}')


def save_plot(name, subfolder=None, folder='figures', dpi=300, tight=True):
    """
    Save the current matplotlib plot as a PNG.
    """
    base_dir = subfolder if subfolder else '.'
    path_dir = os.path.join(base_dir, folder)
    os.makedirs(path_dir, exist_ok=True)

    path = os.path.join(path_dir, f'{name}.png')
    if tight:
        plt.tight_layout()
    plt.savefig(path, dpi=dpi, bbox_inches='tight')
    plt.close()
    logging.info(f'Plot saved as {path}')


def save_clean_data(df, name, folder='datasets'):
    """
    Save a cleaned dataset as an Excel file (.xlsx) inside the datasets folder.
    """
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f'{name}.xlsx')
    df.to_excel(path, index=False)
    logging.info(f'Cleaned dataset saved as {path}')
