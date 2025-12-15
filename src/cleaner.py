import csv
import os
import pandas as pd
from utils import load_csv_if_exists
from utils import load_file
from validate_email import validate_email



df_raw = load_file("../data/raw/lead_list_100.csv")
df_processed = load_file("../data/processed/processed_lead_list.csv")


def clean_data(df_raw, df_processed):
     
    df_processed = df_raw.copy()

    df_processed.columns = (
        df_processed.columns
        .str.strip()
        .str.lower()
        .str.replace(' ','_')
        .str.replace('-', '_')
        .str.replace('(','')
        .str.replace(')','')
    )

    for column in ['pageviews', 'email_opens', 'time_on_site_seconds']:
        df_processed[column] = pd.to_numeric(df_processed[column], errors="coerce").fillna(0).astype(int)
        
   
    df_processed = df_processed.drop_duplicates(subset=["email_address"], keep="first")
    
    df_processed = (
        df_processed
        .drop(columns = 'extra_column??', errors = 'ignore')
        .replace('missing', '')
        .replace('unknown', '')
        .fillna('')
    )

    is_valid = validate_email('example@example.com')
    df_processed = df_processed[df_processed['email_address'].apply(validate_email)]

    df_processed['lead_source'] = (
        df_processed['lead_source']
        .str.lower()
        .str.replace(' ', '_')
    )

    df_processed['activity'] = (
        df_processed['activity']
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('-', '_')
    )

    for x in df_processed.index:
        if df_processed.loc[x, "full_name"] == '':
            df_processed.drop(x, inplace = True)

    print(df_processed)

    df_processed.to_csv('../data/processed/processed_lead_list.csv', index=False) #this line will modify our processed csv file (must be activate at the end of the function)

clean_data(df_raw, df_processed)



