from cleaner import clean_data
from exporter import export_result
from utils import load_file

df_lead_scores = load_file('../data/output/lead_scores.csv')
df_processed = load_file("../data/processed/processed_lead_list.csv")

def run():

    export_result(df_processed, df_lead_scores)

run()