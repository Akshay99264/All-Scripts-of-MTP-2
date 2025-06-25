import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load both datasets
normal_df = pd.read_csv('normal_loss_analysis_summary.csv')
whatsapp_df = pd.read_csv('whatsapp_loss_analysis_summary.csv')

# Ensure 'Group' column is float
normal_df['Group'] = normal_df['Group'].astype(float)
whatsapp_df['Group'] = whatsapp_df['Group'].astype(float)

# X-axis values
x_normal = normal_df['Group']
x_whatsapp = whatsapp_df['Group']

# --- Error bars clamping function ---
def clamp_errors(mean_series, std_series):
    lower_errors = [min(std, mean) for mean, std in zip(mean_series, std_series)]
    upper_errors = std_series
    return lower_errors, upper_errors

# Compute clamped errors
normal_wer_lower, normal_wer_upper = clamp_errors(normal_df['WER_mean'], normal_df['WER_std'])
whatsapp_wer_lower, whatsapp_wer_upper = clamp_errors(whatsapp_df['WER_mean'], whatsapp_df['WER_std'])

normal_cer_lower, normal_cer_upper = clamp_errors(normal_df['CER_mean'], normal_df['CER_std'])
whatsapp_cer_lower, whatsapp_cer_upper = clamp_errors(whatsapp_df['CER_mean'], whatsapp_df['CER_std'])

# Create subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# --- WER subplot ---
ax1.errorbar(x_normal, normal_df['WER_mean'],
             yerr=[normal_wer_lower, normal_wer_upper],
             fmt='o-', capsize=4,
             color='steelblue', marker='o', label='Normal WER')

ax1.errorbar(x_whatsapp, whatsapp_df['WER_mean'],
             yerr=[whatsapp_wer_lower, whatsapp_wer_upper],
             fmt='o-', capsize=4,
             color='firebrick', marker='x', label='WhatsApp WER')

ax1.set_ylabel('WER Score', fontsize=16)
ax1.set_title('WER vs Percentage Loss', fontsize=18, fontweight='bold')
ax1.tick_params(axis='both', labelsize=12)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(fontsize=12)
ax1.set_ylim(bottom=0)

# --- CER subplot ---
ax2.errorbar(x_normal, normal_df['CER_mean'],
             yerr=[normal_cer_lower, normal_cer_upper],
             fmt='s-', capsize=4,
             color='darkorange', marker='s', label='Normal CER')

ax2.errorbar(x_whatsapp, whatsapp_df['CER_mean'],
             yerr=[whatsapp_cer_lower, whatsapp_cer_upper],
             fmt='s-', capsize=4,
             color='green', marker='d', label='WhatsApp CER')

ax2.set_xlabel('Percentage Loss', fontsize=16)
ax2.set_ylabel('CER Score', fontsize=16)
ax2.set_title('CER vs Percentage Loss', fontsize=18, fontweight='bold')
ax2.tick_params(axis='both', labelsize=12)
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(fontsize=12)
ax2.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('wer_cer_comparison.png')
plt.show()
