import csv
import os
import yaml
from utils import load_csv_if_exists
from decimal import Decimal
import pandas as pd

def load_lead():
    relative_path_processed = '../data/processed/processed_lead_list.csv'

    script_dir = os.path.dirname(__file__)

    processed_path = os.path.join(script_dir, relative_path_processed)

    df_processed = load_csv_if_exists(processed_path)

    if df_processed is not None:
        print(df_processed.head())

    return df_processed

def load_config():
    with open('../config/settings.yaml', 'r') as file:
        return yaml.safe_load(file)
    
    return config
        

def calculate_lead_score(lead: dict,config: dict) -> int:
    score = 0
    
                      # ------- Behavioral Scoring ------
    # Access Value in settings.yaml                  
    page_view_weight = config['score_rules']['pageviews']['weight']
    email_opens_weight = config['score_rules']['email_opens']['weight']
    time_on_site_weight = config['score_rules']['time_on_site_seconds']['weight']

    score += lead.get('pageviews', 0) * page_view_weight
    score += lead.get('email_opens', 0) * email_opens_weight
    score += lead.get('time_on_site_seconds', 0) * time_on_site_weight
    
                     # ------- Intent Action Scoring ------
    activity = lead.get('activity', '')                 
    activity_scores = config['score_rules']['activity_scores']

    score += activity_scores.get(activity, 0)
    
                     # ------- Lead Source Scoring ------

    lead_source = lead.get('lead_source', '')
    source_scores = config['source_scores']

    score += source_scores.get(lead_source, 0)

    rounded_score = round(score)

    return rounded_score
    
    


def classify_lead(rounded_score : int, config : dict) -> str:
    thresholds = config['thresholds']

    if rounded_score >= thresholds['hot_lead']:
        return 'hot lead'
    elif rounded_score >= thresholds['warm_lead']:
        return 'warm lead'
    else:
        return 'cold lead'



    
    #print(f'{page_view_weight} \n {email_opens_weight}\n {time_on_site_weight}')


df_processed = load_lead()
config = load_config()

for _, lead in df_processed.iterrows():   # lead is a Series here
    rounded_score = calculate_lead_score(lead, config)
    print(f'{rounded_score}')
    classification = classify_lead(rounded_score, config)
    print(f'{classification}')

    

"""
def score_data(df_processed):
    with open(processed_path, 'r') as file:
        file_reader = csv.DictReader(file)

        for line in file_reader:
            print(line)


        

score_data(df_processed)
"""