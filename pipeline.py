import timeit
import logging
from jobs.reader import read_datalinks, load_data
from jobs.cleaner import clean_data
from jobs.process import generate_json

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

logger = logging.getLogger(__name__)

def main():
    # Launch a timer
    start = timeit.default_timer()

    datalinks = read_datalinks()

    # Load drugs data
    if "drugs" in datalinks :
        drugs = load_data(datalinks["drugs"])
    else:
        raise Exception("drugs key not found in datalinks.json!")
            
    # Load pubmed data
    if "pubmed" in datalinks :
        pubmed = load_data(datalinks["pubmed"])
    else:
        raise Exception("pubmed key not found in datalinks.json!")

    # Load clinical trials data
    if "clinical_trials" in datalinks :
        clinical_trials = load_data(datalinks["clinical_trials"])
    else:
        raise Exception("clinical_trials key not found in datalinks.json!")

    # Clean the tables
    drugs = clean_data(drugs)
    pubmed = clean_data(pubmed)
    clinical_trials = clean_data(clinical_trials)

    # Generate the output JSON
    generate_json(drugs, pubmed, clinical_trials)

    stop = timeit.default_timer() 
    execution_time = stop - start
    logger.info("****** Done --Execution Time : "+str(execution_time)+ " secondes")

if __name__ == "__main__":
    main()


