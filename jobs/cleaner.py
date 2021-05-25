import pandas as pd
import numpy as np

def clean_data(table):
    """
    That function applies some cleaning tasks

    Args:
        table (dataframe): the table before cleaning tasks 

    Returns:
        table (dataframe): the table after cleaning tasks
    """
    # Normalize datatime to one structure '%Y-%m-%d'
    if 'date' in table.columns:
        table['date'] = pd.to_datetime(table['date'])
        table['date'] = table['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    # Remove escape characters from scientific_title
    if 'scientific_title' in table.columns:
        table['scientific_title'] = table.scientific_title.str.replace(r'\\x[0-9A-Fa-f]{2}','', regex=True).values
        table['scientific_title'] = table.scientific_title.str.replace('  ',' ', ).values

    # Remove escape characters from title
    if 'title' in table.columns:
        table['title'] = table.title.str.replace(r'\\x[0-9A-Fa-f]{2}','', regex=True).values
        table['title'] = table.title.str.replace('  ',' ', ).values
    
    # Remove escape characters from journal
    if 'journal' in table.columns:
        table['journal'] = table.journal.str.replace(r'\\x[0-9A-Fa-f]{2}','', regex=True).values
        table['journal'] = table.journal.str.replace('  ',' ').values

    # replace field that's entirely space (or empty) with NaN
    table = table.replace(r'^\s*$', np.nan, regex=True)
    # Remove rows with NaN values
    table = table.dropna()

    return table
