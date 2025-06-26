from pydub import AudioSegment
import random
import csv
import os

def add_percentage_silence(input_file, silence_percentage, output_dir):
    if not (0 <= silence_percentage <= 100):
        raise ValueError("Silence percentage must be between 0 and 100 (inclusive).")
    
    # Load the input audio file
    audio = AudioSegment.from_wav(input_file)

    # Initialize variables
    total_duration = len(audio)  # Total duration of audio in milliseconds
    silence_length = 50  # Fixed silence duration in ms
    num_silences = (silence_percentage * total_duration) // (100 * silence_length)  # Calculate number of 50ms silences
    silence_data = []

    # Generate silence periods and their positions
    silence_positions = random.sample(range(0, total_duration - silence_length, silence_length), int(num_silences))
    silence_positions.sort()  # Optional: to keep silence positions in order

    for silence_start in silence_positions:
        # Create a silent audio segment
        silence_segment = AudioSegment.silent(duration=silence_length)

        # Replace the original audio segment with silence
        audio = audio[:silence_start] + silence_segment + audio[silence_start + silence_length:]

        # Record silence start time and length
        silence_data.append((silence_start / 1000, silence_length))

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Generate dynamic output file names
    output_file = os.path.join(output_dir, f"Modified_{silence_percentage}_percent.wav")
    silence_info_file = os.path.join(output_dir, f"silence_info_{silence_percentage}_percent.csv")

    # Save the modified audio to the output file
    audio.export(output_file, format="wav")

    # Save silence data to a CSV file
    with open(silence_info_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Silence Start (sec)", "Silence Length (ms)"])
        writer.writerows(silence_data)

    print(f"Output audio saved to: {output_file}")
    print(f"Silence information saved to: {silence_info_file}")

# Example usage
input_file = "NormalAudio1.wav"  # Input WAV file
silence_percentage = 1  # Percentage of silence to add (0 to 100)
output_dir = "./Testing"  # Output directory

add_percentage_silence(input_file, silence_percentage, output_dir)
