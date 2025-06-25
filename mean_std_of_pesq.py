import pandas as pd

# Load the original CSV
input_csv = 'Audio1_whatsapp_metrics_results.csv'  # Replace with your CSV file name if different
df = pd.read_csv(input_csv)

# Extract the integer part before the dot in 'ModifiedFileName' to create 'Percentage'
df['Percentage'] = df['ModifiedFileName'].astype(str).str.split('.').str[0].astype(int)

# Group by 'Percentage' and calculate mean and std deviation
grouped = df.groupby('Percentage').agg(
    PESQ_Mean=('PESQ', 'mean'),
    PESQ_Std=('PESQ', 'std'),
    MSE_Mean=('MSE', 'mean'),
    MSE_Std=('MSE', 'std')
).reset_index()

# Save to a new CSV
output_csv = 'Audio1_whatsapp_metrics_summary.csv'
grouped.to_csv(output_csv, index=False)

print(f"Summary saved to {output_csv}")
