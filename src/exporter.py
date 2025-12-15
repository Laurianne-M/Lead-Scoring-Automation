from utils import load_file
import scorer
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



df_lead_scores = load_file('../data/output/lead_scores.csv')
df_processed = load_file('../data/processed/processed_lead_list.csv')

def export_result(df_processed, df_lead_scores):
    
    df_lead_scores = df_processed.copy() 

    config = scorer.load_config()

    df_lead_scores['lead_score'] = df_lead_scores.apply(
        lambda row: scorer.calculate_lead_score(row.to_dict(), config),
        axis=1
    )

    df_lead_scores['lead_class'] = df_lead_scores['lead_score'].apply(
        lambda x: scorer.classify_lead(x, config)
    )

    df_lead_scores.to_csv("../data/output/lead_scores.csv", index=False)
    
    def visualize_lead_scores():

        plt.figure(figsize=(7, 6))  # Optional: set figure size
        ax = sns.countplot(x='lead_class', data=df_lead_scores)

        colors = ['#FEE2AD', '#FFC7A7', '#F08787']  # pink, blue, green
        for i, patch in enumerate(ax.patches):
            patch.set_facecolor(colors[i % len(colors)])

        plt.title('Lead Classification Distribution')
        plt.xlabel('Lead Class')
        plt.ylabel('Number of Leads')

        for p in ax.patches:
            height = p.get_height()
            ax.text(p.get_x() + p.get_width()/2, height + 0.5, int(height), ha='center')

        plt.tight_layout()
        plt.savefig('../data/output/lead_class_distribution.png')
        plt.close()
        print("[INFO] Lead classification chart saved.")
    
    visualize_lead_scores()

export_result(df_processed, df_lead_scores)