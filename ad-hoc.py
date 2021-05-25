import json 
import logging
import timeit
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)

def count_distinct_drugs():
    """
    That function explores the output json file in order to get the most journal that mentions differents drugs

    Args:
        None

    Returns:
        None
    """

    # Opening JSON file
    f = open('./output/output.json',)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)

    # construct a list of tuples of the combinations 
    journal_drug = [(journal, drug) for drug in data for journal in list(set(sum(data[drug]['journal'].values(), [])))]
    result_df = pd.DataFrame(columns=['journal','drug_id'], data=journal_drug)

    logger.info('****** Journal qui mentionne le plus de médicaments différents : %s', result_df['journal'].value_counts(sort=True).index.tolist()[0])

def main():
    # Launch a timer
    start = timeit.default_timer()

    # Count distinct drugs mentions in journal 
    count_distinct_drugs()

    stop = timeit.default_timer() 
    execution_time = stop - start
    logger.info("****** Done --Execution Time : "+str(execution_time)+ " secondes")

if __name__ == "__main__":
    main()