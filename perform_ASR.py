import whisper
import sys
import csv

def extract_words_with_timestamps(audio_path, output_csv):
    model = whisper.load_model("small")

    # Enable word-level timestamps
    result = model.transcribe(audio_path, word_timestamps=True)

    words_with_timestamps = []

    for segment in result.get("segments", []):  # Use .get() to prevent KeyError
        for word_info in segment.get("words", []):  
            # Debugging: Print the entire word_info structure
            print(f"DEBUG: {word_info}")

            # Extract word information safely
            word = word_info.get("word", "UNKNOWN")  # Default to "UNKNOWN" if missing
            start_time = word_info.get("start", -1)  # Default to -1 if missing
            end_time = word_info.get("end", -1)  # Default to -1 if missing
            prob = word_info.get("probability", 0) # Default to 0 if missing

            # print(word)
            # print(start_time)
            # print(end_time)
            # print(prob)

            # Only add valid entries
            if word != "UNKNOWN" and start_time != -1 and end_time != -1 and prob != -1:
                words_with_timestamps.append([word])
            else:
                print(f"Skipping due to missing values: {word_info}")

    # Write to CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["word"])
        writer.writerows(words_with_timestamps)

    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate.py <audio_file> <output_csv>")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    output_csv = sys.argv[2]
    
    extract_words_with_timestamps(audio_path, output_csv)
