import pandas as pd
import matplotlib.pyplot as plt

# Load the two CSV files
whatsapp_file = 'Audio1_whatsapp_metrics_summary.csv'
normal_file = 'Audio1_normal_metrics_summary.csv'

df_whatsapp = pd.read_csv(whatsapp_file)
df_normal = pd.read_csv(normal_file)

# Create figure with 2 subplots
fig, axs = plt.subplots(2, 1, figsize=(12, 8))

# Define x-ticks based on union of both files
all_percentages = sorted(set(df_whatsapp['Percentage']).union(set(df_normal['Percentage'])))

# --- First subplot: PESQ ---
axs[0].errorbar(df_whatsapp['Percentage'], df_whatsapp['PESQ_Mean'], 
                yerr=df_whatsapp['PESQ_Std'], fmt='-o', capsize=5, color='blue', label='WhatsApp')
axs[0].errorbar(df_normal['Percentage'], df_normal['PESQ_Mean'], 
                yerr=df_normal['PESQ_Std'], fmt='-o', capsize=5, color='orange', label='Normal')

axs[0].set_title('PESQ Mean and Standard Deviation (Normal vs WhatsApp)', fontsize=20, fontweight='bold')
axs[0].set_xlabel('Percentage Error (%)', fontsize=18)
axs[0].set_ylabel('PESQ Score', fontsize=18)
axs[0].set_xticks(all_percentages)
axs[0].tick_params(axis='both', labelsize=16)
axs[0].legend(fontsize=16)
axs[0].grid(True)

# --- Second subplot: MSE ---
axs[1].errorbar(df_whatsapp['Percentage'], df_whatsapp['MSE_Mean'], 
                yerr=df_whatsapp['MSE_Std'], fmt='-o', capsize=5, color='blue', label='WhatsApp')
axs[1].errorbar(df_normal['Percentage'], df_normal['MSE_Mean'], 
                yerr=df_normal['MSE_Std'], fmt='-o', capsize=5, color='orange', label='Normal')

axs[1].set_title('MSE Mean and Standard Deviation (Normal vs WhatsApp)', fontsize=20, fontweight='bold')
axs[1].set_xlabel('Percentage Error (%)', fontsize=18)
axs[1].set_ylabel('Mean Squared Error', fontsize=18)
axs[1].set_xticks(all_percentages)
axs[1].tick_params(axis='both', labelsize=16)
axs[1].legend(fontsize=16)
axs[1].grid(True)

# Tight layout with top padding for suptitle
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Show the plot
plt.show()
