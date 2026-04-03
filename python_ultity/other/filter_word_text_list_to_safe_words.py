import os

BASE_DIR = os.path.dirname(__file__)

BAD_WORDS_FILE_PATH = os.path.join(BASE_DIR, "..", "datasets", "bad_words.txt")
WORD_LIST_TO_FILTER = os.path.join(BASE_DIR, "..", "datasets", "words.txt")

OUTPUT_FILE = os.path.join(BASE_DIR, "..", "datasets", "filtered_words.txt")

with open(BAD_WORDS_FILE_PATH , "r") as f:
    bad_words = set(line.strip().lower() for line in f if line.strip())

# Open random words and filter
with open(WORD_LIST_TO_FILTER, "r") as f:
    random_words = [line.strip().lower() for line in f if line.strip()]

# Keep only words not in the bad list
filtered_words = [word for word in random_words if word not in bad_words]

# Save to a new file
with open(OUTPUT_FILE, "w") as f:
    for word in filtered_words:
        f.write(word + "\n")