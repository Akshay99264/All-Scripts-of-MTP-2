import os
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.ndimage import zoom
from pesq import pesq
from scipy.signal import resample_poly
import csv

# Function to calculate PESQ and MSE
def calculate_metrics(y1, y2, sr1, sr2, target_sr):
    # Resample both signals
    y1_resampled = resample_poly(y1, target_sr, sr1)
    y2_resampled = resample_poly(y2, target_sr, sr2)

    # Pad to same length
    max_length = max(len(y1_resampled), len(y2_resampled))
    y1_padded = np.pad(y1_resampled, (0, max_length - len(y1_resampled)), 'constant')
    y2_padded = np.pad(y2_resampled, (0, max_length - len(y2_resampled)), 'constant')

    # Calculate PESQ
    try:
        pesq_score = pesq(target_sr, y1_padded, y2_padded, mode='wb')
    except Exception as e:
        pesq_score = None
        print(f"Error calculating PESQ: {e}")

    # Calculate MSE in 100Hz-4000Hz band
    S1 = np.abs(librosa.stft(y1_padded))
    S2 = np.abs(librosa.stft(y2_padded))
    S1_db = librosa.amplitude_to_db(S1, ref=np.max)
    S2_db = librosa.amplitude_to_db(S2, ref=np.max)

    min_freq = 100
    max_freq = 4000
    frequencies = librosa.fft_frequencies(sr=target_sr)
    freq_indices = np.where((frequencies >= min_freq) & (frequencies <= max_freq))[0]
    S1_db_voice = S1_db[freq_indices, :]
    S2_db_voice = S2_db[freq_indices, :]

    if S1_db_voice.shape != S2_db_voice.shape:
        scale_factor = S2_db_voice.shape[1] / S1_db_voice.shape[1]
        S1_db_voice = zoom(S1_db_voice, (1, scale_factor), order=1)

    mse = np.mean((S1_db_voice - S2_db_voice) ** 2)

    return pesq_score, mse

# Paths
reference_file = "../Audios_with_required_format/Recorded/1_0_1.wav"       # Reference clean audio
modified_folder = "../Audios_with_required_format/Recorded/"   # Folder containing all degraded/modified audios
output_csv = "Audio1_whatsapp_metrics_results.csv"    # Output CSV

# Load reference audio
y_ref, sr_ref = librosa.load(reference_file, sr=None)

# Prepare CSV
header = ['ModifiedFileName', 'PESQ', 'MSE']

with open(output_csv, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(header)

    # Iterate through all files in the modified folder
    for modified_filename in os.listdir(modified_folder):
        modified_path = os.path.join(modified_folder, modified_filename)
        
        if os.path.isfile(modified_path):
            # Load modified audio
            y_mod, sr_mod = librosa.load(modified_path, sr=None)
            
            # Calculate PESQ and MSE
            target_sr = 16000  # Target sample rate for PESQ
            pesq_score, mse = calculate_metrics(y_ref, y_mod, sr_ref, sr_mod, target_sr)

            # Handle PESQ errors
            if pesq_score is None:
                pesq_score = 'N/A'

            # Write to CSV
            writer.writerow([modified_filename, pesq_score, mse])

            print(f"Processed {modified_filename}: PESQ = {pesq_score}, MSE = {mse}")

print(f"\n✅ All results saved in {output_csv}")
