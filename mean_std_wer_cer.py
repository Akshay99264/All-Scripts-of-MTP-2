import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv("whatsapp_wer_cer_normalized_0_to_1.csv")  # replace with your filename

# Create a new column for grouped percent loss (integer part)
df['percent_loss_group'] = df['percent_loss'].apply(lambda x: int(x))

# Group by this new column
grouped = df.groupby('percent_loss_group')

# Prepare list to store summary
summary = []

# Iterate through each group and calculate stats
for group_val, group_data in grouped:
    count = len(group_data)
    wer_mean = group_data['WER'].mean()
    wer_std = group_data['WER'].std()
    cer_mean = group_data['CER'].mean()
    cer_std = group_data['CER'].std()
    
    print(f"Loss % Group: {group_val} -> Count: {count}")
    
    summary.append([
        group_val, count,
        wer_mean, wer_std,
        cer_mean, cer_std
    ])

# Create a summary DataFrame
summary_df = pd.DataFrame(summary, columns=[
    "percent_loss_group", "count", "WER_mean", "WER_std", "CER_mean", "CER_std"
])

# Save to CSV
summary_df.to_csv("loss_analysis_summary.csv", index=False)

print("\nSummary saved to 'loss_analysis_summary.csv'")
