import pandas as pd
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)

def read_datalinks():
    """
    That function reads the links of different data sources from the json file datalinks.json
    The json file has the following schema :
    {
        source_content(drugs/pubmed/trials) : {
            data_format1 = [path1,2,3...]
            data_format2 = [path1,2,3...]
            ...
        }
    }

    Args:
        None

    Returns:
        Dict: the paths of each data format
    """
    with open("datalinks.json") as f:
        data = json.load(f)
    return data

def read_csv_files(files, table):
    """
    That function reads the CSV data format and concat the files in one dataframe
    
    Args:
        files (list): the list of CSV files given in datalinks.json 
        table (dataframe): the table that we will construct based all the given files

    Returns:
        table (dataframe): the paths after concatenating all csv files
    """
    for filename in files:
        # Temporary dataframe that contains the current CSV file data
        tmp = pd.read_csv(filename, encoding='utf-8')
        table = pd.concat([table,tmp])
    return table

def read_json_files(files, table):
    """
    That function reads the JSON data format and concat the files in one dataframe
    
    Args:
        files (list): the list of JSON files given in datalinks.json 
        table (dataframe): the table that we will construct based on all the given files

    Returns:
        table (dataframe): the paths after concatenating all json files
    """
    for filename in files:
        with open(filename) as f:
            data = json.load(f)
        # Temporary dataframe that contains the current json file data
        tmp = pd.DataFrame(data)
        table = pd.concat([table,tmp])
    return table

def load_data(datalinks):
    """
    That function ensures loading data from different formats and concat all the given files (JSON/CSV..) in one dataframe
    
    Args:
        datalinks (dict): the paths of each data format for only one content (drugs or pubmed or trials) 

    Returns:
        table (dataframe): the paths after concatenating all json files
    """
    table = pd.DataFrame()

    for key in datalinks:
        if key == "csv": 
            table = read_csv_files(datalinks[key], table)
        elif key == 'json':
            table = read_json_files(datalinks[key], table)
        else:
            raise Exception(key + ' format not yet developped!')
    return table