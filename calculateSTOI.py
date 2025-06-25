import librosa
import numpy as np
import soundfile as sf
import os
import pandas as pd
from pystoi.stoi import stoi

def load_audio(file_path, target_sr=16000):
    audio, sr = librosa.load(file_path, sr=target_sr, mono=True)
    return audio, sr

def pad_audio(audio1, audio2):
    len1, len2 = len(audio1), len(audio2)
    if len1 > len2:
        audio2 = np.pad(audio2, (0, len1 - len2), mode='constant')
    elif len2 > len1:
        audio1 = np.pad(audio1, (0, len2 - len1), mode='constant')
    return audio1, audio2

def calculate_stoi(reference_audio, test_audio, sr):
    ref_audio, test_audio = pad_audio(reference_audio, test_audio)
    return stoi(ref_audio, test_audio, sr, extended=False)

def batch_calculate_stoi(reference_audio_path, test_folder_path, output_csv_path):
    # Load reference audio
    ref_audio, sr_ref = load_audio(reference_audio_path)

    results = []

    # Loop through all files in the test folder
    for filename in os.listdir(test_folder_path):
        if filename.lower().endswith('.wav'):
            test_file_path = os.path.join(test_folder_path, filename)
            test_audio, sr_test = load_audio(test_file_path, target_sr=sr_ref)

            score = calculate_stoi(ref_audio, test_audio, sr_ref)
            print(f"{filename} - STOI: {score:.4f}")
            
            results.append({
                'FileName': filename,
                'STOI': score
            })

    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_csv_path, index=False)
    print(f"\nAll STOI scores saved to {output_csv_path}")

# Example usage
if __name__ == "__main__":
    reference_audio_path = "../Audios_with_required_format/Recorded/1_0_1.wav"  # path to your reference normal audio
    test_folder_path = "../Audios_with_required_format/Recorded/"           # folder containing the distorted/test audios
    output_csv_path = "Audio1_whatsapp_stoi_scores.csv"          # output CSV path
    
    batch_calculate_stoi(reference_audio_path, test_folder_path, output_csv_path)
