import os
from syllable_classifier import classify_syllable
import sqlite3
import sys

# Add the fake word generator to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from nonsence_word_generator import generate_word
from check_bad_words import remove_bad_words

BASE_DIR = os.path.dirname(__file__)

# Path to make db; copy paste into godot project when ready
DB_PATH = os.path.join(BASE_DIR, "..", "datasets", "Words.db")

INPUT_SOURCE_SYLLABLES = os.path.join(BASE_DIR, "..", "datasets", "real_words_syllables")
# 1 through 8; add file_name_prefix to INPUT_SOURCE to get full file name; put number at start
file_name_prefix_syllables = "-syllables-sorted-by-frequency.txt"

INPUT_SOURCE_FRIENDLY_WORDS_FOR_KIDS = os.path.join(BASE_DIR, "..", "datasets", "real_words_friendly")
file_name_prefix_friendly = "_syllables.txt"


def create_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    if os.path.exists(DB_PATH):
        print(f"Error: Database already exists at {DB_PATH}. Delete it manually to recreate.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE Words (
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        syllable_count INTEGER,
        letter_count INTEGER,
        is_real BOOLEAN NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE Syllables (
        syllable_id INTEGER PRIMARY KEY AUTOINCREMENT,
        syllable TEXT NOT NULL UNIQUE,
        syllable_type TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE Syllable_Indexes (
        syllable_id INTEGER NOT NULL,
        word_id INTEGER NOT NULL,
        position INTEGER NOT NULL,
        PRIMARY KEY (syllable_id, word_id, position),
        FOREIGN KEY (syllable_id) REFERENCES Syllables(syllable_id),
        FOREIGN KEY (word_id) REFERENCES Words(word_id)
    );
    """)

    cur.execute("""
    CREATE TABLE Problem_Sets (
        set_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    """)

    cur.execute("""
    CREATE TABLE Problem_Set_Words (
        set_id INTEGER NOT NULL,
        word_id INTEGER NOT NULL,
        PRIMARY KEY (set_id, word_id),
        FOREIGN KEY (set_id) REFERENCES Problem_Sets(set_id),
        FOREIGN KEY (word_id) REFERENCES Words(word_id)
    );
    """)

    conn.commit()
    conn.close()
    print(f"Database created successfully at: {DB_PATH}")


def insert_real_words():
    if not os.path.exists(DB_PATH):
        print("Error: Database does not exist. Run create_database() first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    vowels = "aeiouy"
    total_words_read = 0
    total_words_inserted = 0
    total_words_skipped = 0

    for syllable_count in range(1, 9):  # 1 to 8
        filename = f"{syllable_count}{file_name_prefix_syllables}"
        file_path = os.path.join(INPUT_SOURCE_SYLLABLES, filename)

        if not os.path.exists(file_path):
            print(f"Error: Missing file: {file_path}")
            continue

        print(f"Reading: {file_path} ...")

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                total_words_read += 1

                # com;put;er -> computer is the word, syllables are com, put, er, index is com=0, put=1, er=2
                syllables = [s.strip() for s in line.split(";") if s.strip()]
                
                # Check if any syllable has no vowels - if so, skip this word entirely
                skip_word = False
                for syllable in syllables:
                    if not any(char in vowels for char in syllable.lower()):
                        print(f"  Skipping word '{(''.join(syllables))}' - syllable '{syllable}' has no vowels")
                        skip_word = True
                        total_words_skipped += 1
                        break
                
                if skip_word:
                    continue
                
                word = "".join(syllables)
                letter_count = len(word)

                cur.execute("""
                    INSERT OR IGNORE INTO Words (name, syllable_count, letter_count, is_real)
                    VALUES (?, ?, ?, ?)
                """, (word, len(syllables), letter_count, True))

                cur.execute("SELECT word_id FROM Words WHERE name = ?", (word,))
                word_id = cur.fetchone()[0]

                total_words_inserted += 1

                for position, syllable in enumerate(syllables):
                    syllable_type = classify_syllable(syllable)
                    if syllable_type == "Unknown":
                        print(f"  Warning: Could not classify syllable '{syllable}' in word '{word}'")
                    cur.execute("""
                        INSERT OR IGNORE INTO Syllables (syllable, syllable_type)
                        VALUES (?, ?)
                    """, (syllable, syllable_type))

                    cur.execute("SELECT syllable_id FROM Syllables WHERE syllable = ?", (syllable,))
                    syllable_id = cur.fetchone()[0]

                    cur.execute("""
                        INSERT OR IGNORE INTO Syllable_Indexes (syllable_id, word_id, position)
                        VALUES (?, ?, ?)
                    """, (syllable_id, word_id, position))

    conn.commit()
    conn.close()
    print(f"\nFinished inserting real words.")
    print(f"Total words read: {total_words_read}")
    print(f"Total words inserted: {total_words_inserted}")
    print(f"Total words skipped (no vowels): {total_words_skipped}")


def insert_fake_words(word_length, count):
    if not os.path.exists(DB_PATH):
        print("Error: Database does not exist. Run create_database() first.")
        return

    print(f"\nGenerating {count} fake words of length {word_length}...")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    generated = set()
    attempts = 0
    max_attempts = count * 50  # Allow more attempts for harder lengths
    
    while len(generated) < count and attempts < max_attempts:
        word = generate_word(word_length)
        if word and word not in generated:
            generated.add(word)
            
            if len(generated) % 50 == 0:
                print(f"  Progress: {len(generated)}/{count}")
        
        attempts += 1
    
    if len(generated) < count:
        print(f"  Warning: Only generated {len(generated)} words out of {count} requested")
    
    # Insert generated words
    inserted = 0
    for word in generated:
        letter_count = len(word)
        syllable_count = 1  # Treat all fake words as 1 syllable
        
        try:
            cur.execute("""
                INSERT OR IGNORE INTO Words (name, syllable_count, letter_count, is_real)
                VALUES (?, ?, ?, ?)
            """, (word, syllable_count, letter_count, False))

            cur.execute("SELECT word_id FROM Words WHERE name = ?", (word,))
            result = cur.fetchone()
            if result:
                word_id = result[0]

                cur.execute("""
                    INSERT OR IGNORE INTO Syllables (syllable, syllable_type)
                    VALUES (?, ?)
                """, (word, "Unknown-Fake"))

                cur.execute("SELECT syllable_id FROM Syllables WHERE syllable = ?", (word,))
                syl_result = cur.fetchone()
                if syl_result:
                    syllable_id = syl_result[0]

                    cur.execute("""
                        INSERT OR IGNORE INTO Syllable_Indexes (syllable_id, word_id, position)
                        VALUES (?, ?, ?)
                    """, (syllable_id, word_id, 0))

                    inserted += 1
                
        except Exception as e:
            print(f"  Error inserting word '{word}': {e}")

    conn.commit()
    conn.close()
    print(f"  Successfully inserted: {inserted}/{count}")


def filter_to_friendly_words():
    """Remove any real word from the DB that does not appear in the friendly word lists.
    Fake words (is_real = False) are left untouched."""

    if not os.path.exists(DB_PATH):
        print("Error: Database does not exist. Run create_database() first.")
        return

    # Load all friendly words from files 1_syllables.txt through 4_syllables.txt
    friendly_words = set()
    for syllable_count in range(1, 5):  # 1 to 4
        filename = f"{syllable_count}{file_name_prefix_friendly}"
        file_path = os.path.join(INPUT_SOURCE_FRIENDLY_WORDS_FOR_KIDS, filename)

        if not os.path.exists(file_path):
            print(f"Warning: Missing friendly word file: {file_path}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    friendly_words.add(word)

    print(f"\nLoaded {len(friendly_words)} friendly words across all syllable files.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get all real words from the DB
    cur.execute("SELECT word_id, name FROM Words WHERE is_real = 1")
    real_words = cur.fetchall()

    print(f"Checking {len(real_words)} real words against friendly list...")

    removed = 0
    for word_id, name in real_words:
        if name.lower() not in friendly_words:
            cur.execute("DELETE FROM Syllable_Indexes WHERE word_id = ?", (word_id,))
            cur.execute("DELETE FROM Words WHERE word_id = ?", (word_id,))
            removed += 1

    conn.commit()
    conn.close()

    kept = len(real_words) - removed
    print(f"  Removed: {removed} real words not found in friendly list")
    print(f"  Kept:    {kept} real words")


def reset_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Deleted existing database at {DB_PATH}.")
    create_database()
    insert_real_words()
    insert_fake_words(3, 200)
    insert_fake_words(4, 200)
    insert_fake_words(5, 200)
    insert_fake_words(6, 200)

    # Remove bad words
    print("\n" + "=" * 60)
    print("REMOVING BAD WORDS")
    print("=" * 60)
    remove_bad_words()

    # Filter real words down to friendly kids list only (fake words are skipped)
    print("\n" + "=" * 60)
    print("FILTERING TO FRIENDLY WORDS")
    print("=" * 60)
    #filter_to_friendly_words()


if __name__ == "__main__":
    reset_database()