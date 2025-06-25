import pandas as pd
import matplotlib.pyplot as plt

# Load the data
whatsapp_file = 'Audio1_whatsapp_metrics_summary.csv'
normal_file = 'Audio1_normal_metrics_summary.csv'

df_whatsapp = pd.read_csv(whatsapp_file)
df_normal = pd.read_csv(normal_file)

# Plot
plt.figure(figsize=(12, 6))

# WhatsApp metrics
plt.errorbar(df_whatsapp['Percentage'], df_whatsapp['STOI_Mean'], yerr=df_whatsapp['STOI_Std'],
             fmt='-o', capsize=5, color='purple', label='WhatsApp')

# Normal metrics
plt.errorbar(df_normal['Percentage'], df_normal['STOI_Mean'], yerr=df_normal['STOI_Std'],
             fmt='-o', capsize=5, color='green', label='Normal')

# Titles and labels with increased font size and bold title
plt.title('STOI Mean and Standard Deviation (Normal vs WhatsApp)', fontsize=20, fontweight='bold')
plt.xlabel('Percentage Error (%)', fontsize=18)
plt.ylabel('STOI Score', fontsize=18)

# Set x-ticks at an interval of 1
min_percentage = min(df_whatsapp['Percentage'].min(), df_normal['Percentage'].min())
max_percentage = max(df_whatsapp['Percentage'].max(), df_normal['Percentage'].max())
plt.xticks(range(int(min_percentage), int(max_percentage) + 1, 1), fontsize=16)
plt.yticks(fontsize=16)

# Grid, legend and layout
plt.grid(True)
plt.legend(fontsize=12)
plt.tight_layout()

# Show the plot
plt.show()
