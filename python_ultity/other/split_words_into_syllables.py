import pyphen
import sqlite3
import re
import os

# ---------- CONFIG ----------
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "..", "..", "datasets", "test_database.db")
WORDS_FILE = os.path.join(BASE_DIR, "..", "..", "datasets", "filtered_words.txt")
LOG_FILE = os.path.join(BASE_DIR, "syllables_log.txt")
# ----------------------------

dic = pyphen.Pyphen(lang="en")

def classify_syllable(syl: str):
    syl = syl.lower()
    vowels = "aeiouy"

    if re.match(r".*[aeiou]{1}[^aeiouy]$", syl):
        return "Closed"
    if syl and syl[-1] in vowels:
        return "Open"
    if re.match(r".*[aeiou][bcdfghjklmnpqrstvwxyz]e$", syl):
        return "Magic-e"
    if re.search(r"(aa|ee|ea|ai|oa|oo|ou|ie|ue)", syl):
        return "Vowel Team"
    if re.search(r"[aeiou]r", syl):
        return "R-controlled"
    if re.search(r"(oi|oy|ow|ou)", syl):
        return "Diphthong"
    if syl.endswith(("ble","cle","dle","fle","gle","kle","ple","tle","zle")):
        return "Consonant-le"
    return None

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Open log file for writing
with open(LOG_FILE, "w") as log:
    # Load words
    with open(WORDS_FILE, "r") as f:
        words = [line.strip() for line in f if line.strip()]

    for word in words:
        # Raw syllables from Pyphen
        syllables = dic.inserted(word).split("-")

        # Write raw Pyphen output to file
        log.write(f"{syllables}\n")

        for syl in syllables:
            syl_type = classify_syllable(syl)
            if syl_type is None:
                continue

            cur.execute("""
                INSERT INTO syllables (syllable, type, count)
                VALUES (?, ?, 1)
                ON CONFLICT(syllable) DO UPDATE SET count = count + 1
            """, (syl, syl_type))

conn.commit()
cur.close()
conn.close()

print("✅ Finished inserting syllables into test_database.db")
print(f"📄 Raw Pyphen splits saved to {LOG_FILE}")