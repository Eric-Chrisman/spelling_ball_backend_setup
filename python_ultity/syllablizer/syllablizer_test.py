import os
from syllablizer import syllablizer 
import csv

BASE_DIR = os.path.dirname(__file__)
WORD_CSV_FILE_PATH = os.path.join(BASE_DIR, "..", "..", "datasets", "5-syllables.txt")
OUTPUT_CSV_FILE_PATH = os.path.join(BASE_DIR, "..", "..", "datasets", "5-syllables-processed.txt")

def process_syllable_csv(path):
    results_words = []
    results_breaks = []
    results = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            # row is like ['u','ni','ver','si','ty']
            syllables = row
            word = "".join(syllables)

            # compute break positions
            breaks = []
            pos = 0
            for s in syllables[:-1]:  # skip last because no break after final syllable
                pos += len(s)
                breaks.append(pos)

            results.append((word, breaks))
    # print(results)
    return results

def syllablizer_test(data):
    with open(OUTPUT_CSV_FILE_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        for word, expected_breaks in data:
            computed_syllables = syllablizer(word)

            if computed_syllables != expected_breaks:
                print(f"❌ Mismatch for '{word}': expected {expected_breaks}, got {computed_syllables}")
                writer.writerow(computed_syllables)
            else:
                print(f"✅ Match for '{word}': {computed_syllables}")


data = process_syllable_csv(WORD_CSV_FILE_PATH)
syllablizer_test(data)
