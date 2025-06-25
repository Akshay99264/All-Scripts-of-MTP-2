import os
import csv
import re
from jiwer import wer
import numpy as np

def levenshtein_distance(ref, hyp):
    m, n = len(ref), len(hyp)
    dp = np.zeros((m + 1, n + 1), dtype=int)

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref[i - 1] == hyp[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]
                )
    return dp[m][n]

def interpret_quality(score):
    if score <= 0.05:
        return "Excellent"
    elif score <= 0.15:
        return "Good"
    elif score <= 0.30:
        return "Fair"
    elif score <= 0.50:
        return "Poor"
    else:
        return "Unusable"

def extract_percent_loss(filename):
    match = re.search(r'1_(\d+)_(\d+)\.txt', filename)
    if match:
        base = int(match.group(1))
        extra = int(match.group(2))
        return base + extra / 100
    return None

def compute_batch_metrics(folder_path, reference_file, output_csv):
    ref_path = os.path.join(folder_path, reference_file)
    
    with open(ref_path, 'r', encoding='utf-8') as f:
        reference = f.read().strip()

    results = []

    for file in os.listdir(folder_path):
        if file.endswith('.txt') and file != reference_file and file.startswith("1_"):
            percent_loss = extract_percent_loss(file)
            if percent_loss is None:
                continue

            hyp_path = os.path.join(folder_path, file)
            with open(hyp_path, 'r', encoding='utf-8') as f:
                hypothesis = f.read().strip()

            # WER (already 0 to 1)
            word_error = min(1.0, max(0.0, wer(reference, hypothesis)))

            # CER
            ref_chars = reference.replace(" ", "")
            hyp_chars = hypothesis.replace(" ", "")
            raw_cer = levenshtein_distance(ref_chars, hyp_chars) / max(1, len(ref_chars))
            cer = min(1.0, max(0.0, raw_cer))

            # Quality based on WER
            quality = interpret_quality(word_error)

            results.append([
                file,
                f"{percent_loss:.2f}",
                f"{word_error:.3f}",
                f"{cer:.3f}",
                quality
            ])

    # Sort by percent_loss
    results.sort(key=lambda x: float(x[1]))

    # Save to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["file_name", "percent_loss", "WER", "CER", "Quality"])
        writer.writerows(results)

    print(f"✅ Metrics written to {output_csv}")

# Example usage
compute_batch_metrics(folder_path='./whatsapp_string', reference_file='1_0_1.txt', output_csv='whatsapp_wer_cer_normalized_0_to_1.csv')
