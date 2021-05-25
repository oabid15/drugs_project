# PART 1 : Drugs

### Data Pipeline 

The goal of this project is to develop a data pipeline based on drugs data.

The developed pipeline is composed of :

1. Data loading 

It consists of reading data from different formats and merge them in one dataframe.

2. Data cleaning

It consists of : 
- removing rows with NaN values
- normalizing datetime format
- removing escape characters like : \\xc3\\x28

3. Data manipulation

Based on the graph in description, I loop on drugs table and I search drug name in pubmed & clinical trials titles. 
The main keys of our output dictionnary are drug_ids. On a second level, we have the related entities to drugs which are Pubmed, clinical_trials and journal. In pubmed and clinical_trials, we will found in the JSON the titles of publications referenced by date. Finaly, we will have in the output the associated journals to these publications referenced also by date. 

This vision was translated by the following JSON Schema : 
```yaml
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
```

This pipeline can be launched using :

```python
python pipeline.py
```
Output : 
```python
24-May-21 01:04:52 - __main__ - INFO - ****** Done --Execution Time : 0.1246179999999999 secondes
```

** This python script will use other python scripts in jobs folder. The other python scripts consist of each step/job of the pipeline.

### Ad-hoc 
The ad-hoc part is kind of some data analysis after the previous data pipeline. It is based on the output JSON and it consists of returning the journal which mentions the most differents drugs.

This ad-hoc can be launched using :

```python
python ad-hoc.py
```
Output :
```python
24-May-21 01:15:15 - __main__ - INFO - ****** Journal qui mentionne le plus de médicaments différents : Psychopharmacology
24-May-21 01:15:15 - __main__ - INFO - ****** Done --Execution Time : 0.022651399999999988 secondes
```

# PART 2 : SQL Requests
1. 
``` sql
SELECT date, SUM(prod_price*prod_qty) AS ventes FROM transaction
WHERE date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY date
ORDER BY date ASC;
``` 

2. 
``` sql
SELECT transaction.client_id,
	SUM(CASE WHEN product_nomenclature.product_type = 'MEUBLE' THEN transaction.prod_price*transaction.prod_qty ELSE 0 END) AS ventes_meubles,
	SUM(CASE WHEN product_nomenclature.product_type = 'DECO' THEN transaction.prod_price*transaction.prod_qty ELSE 0 END) AS ventes_deco
FROM transaction
JOIN product_nomenclature ON transaction.prod_id = product_nomenclature.product_id
WHERE transaction.date BETWEEN '2019-01-01' AND '2019-12-31'
GROUP BY transaction.client_id;
```

