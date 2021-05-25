import json 
import pandas as pd

def generate_json(drugs, pubmed, trials):
    """
    That function creates a json output file based on the graph presented in the description of the project
    The output JSON file schema :
    {
        drug_id : {
                    "pubmed": { // the founded titles are grouped by date and shown in a list in order to have a great visibility about the concerned drug
                                mention_date1: [title1, title2..], 
                                mention_date2: [title3]
                                ... 
                            },
                    "clinical_trials": { // the founded titles are grouped by date and shown in a list in order to have a great visibility about the concerned drug
                                mention_date1: [title1, title2..],
                                mention_date2: [title3]
                                ...
                            },
                    "journal": { // The drug is referenced in the journal by the date 
                                mention_date1: [Journal_name1],
                                mention_date2: [Journal_name1],
                                mention_date3: [Journal_name2],
                                ...
                            }
                }
    } 

    Args:
        drugs (dataframe): drugs table
        pubmed (dataframe): pubmed table
        trials (dataframe): clinical trials table 

    Returns:
        None
    """
    output = {}

    for index,row in drugs.iterrows():
        # Search the drug name in the titles of PubMed table 
        pubmed_request = pubmed[pubmed['title'].str.lower().str.contains(row['drug'].lower(), na=False)]

        # Search the drug name in the titles of clinical trials table
        trials_request = trials[trials['scientific_title'].str.lower().str.contains(row['drug'].lower(), na=False)]

        # Define the output JSON schema
        output[row['atccode']] = {}
    
        all_journal = pd.DataFrame()
    
        if len(pubmed_request) > 0:
            # group pubmed request by date and move the result to a dictionnary which the keys are mention dates
            output[row['atccode']]['pubmed'] = pubmed_request.groupby('date')['title'].apply(list).to_dict()
            # select only these three columns in order to prepare the journal founded between pubmed and trials
            pubmed_request = pubmed_request[['title','date','journal']]
            all_journal = all_journal.append(pubmed_request, ignore_index = True)
                
        if len(trials_request) > 0:
            # group clinical trials request by date and move the result to a dictionnary which the keys are mention dates
            output[row['atccode']]['clinical_trials'] = trials_request.groupby('date')['scientific_title'].apply(list).to_dict()
            # select only these three columns in order to prepare the journal founded between pubmed and trials
            trials_request = trials_request[['scientific_title','date','journal']]
            # rename scientific_title column in order to concat the both request results
            trials_request = trials_request.rename(columns = {'scientific_title':'title'})
            trials_request = trials_request[['title','date','journal']]
            all_journal = all_journal.append(trials_request, ignore_index = True)
        
        if len(all_journal) > 0:
            # group the journals by date and move the result to a dictionnary which the keys are mention dates
            output[row['atccode']]['journal'] = all_journal.groupby('date')['journal'].apply(set).apply(list).to_dict()

        if not output[row['atccode']]:
            output.pop(row['atccode'])

    # create an output json file and write the designed dictionnary
    with open('./output/output.json', 'w') as outfile:
        json.dump(output, outfile, indent=4, ensure_ascii=False)