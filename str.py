import os
import csv
import re

# Folder containing your CSV files
csv_folder = './EXTRACTED_RECORDED_AUDIO'
output_folder = './whatsapp_string'

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(csv_folder):
    if filename.endswith('.csv'):
        csv_path = os.path.join(csv_folder, filename)
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_path = os.path.join(output_folder, txt_filename)

        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header
            words = [row[0].strip() for row in reader if row]

        # Join words and remove all characters except letters and spaces
        raw_text = ' '.join(words)
        clean_text = re.sub(r'[^A-Za-z ]+', '', raw_text)

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(clean_text)

        print(f"Processed: {filename} → {txt_filename}")
