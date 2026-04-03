import os
import sqlite3

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "..", "datasets", "Words.db")
BAD_WORDS_FILE = os.path.join(BASE_DIR, "..", "datasets", "bad_words.txt")


def check_bad_words():   
    # Check if files exist
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return
    
    if not os.path.exists(BAD_WORDS_FILE):
        print(f"Error: Bad words file not found at {BAD_WORDS_FILE}")
        return
    
    # Load bad words list
    print(f"Loading bad words from: {BAD_WORDS_FILE}")
    with open(BAD_WORDS_FILE, "r", encoding="utf-8") as f:
        bad_words = set(line.strip().lower() for line in f if line.strip())
    
    print(f"Loaded {len(bad_words)} bad words to check against")
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Get all words from database
    cur.execute("SELECT name, is_real FROM Words")
    all_words = cur.fetchall()
    
    print(f"\nChecking {len(all_words)} words in database...\n")
    
    # Find matches
    real_word_matches = []
    fake_word_matches = []
    
    for word, is_real in all_words:
        word_lower = word.lower()
        if word_lower in bad_words:
            if is_real:
                real_word_matches.append(word)
            else:
                fake_word_matches.append(word)
    
    # Report results
    print("=" * 60)
    print("BAD WORDS CHECK RESULTS")
    print("=" * 60)
    
    if real_word_matches:
        print(f"\nFound {len(real_word_matches)} REAL words that are bad words:")
        for word in sorted(real_word_matches):
            print(f"  - {word}")
    else:
        print("\n✓ No bad words found in REAL words")
    
    if fake_word_matches:
        print(f"\nFound {len(fake_word_matches)} FAKE words that are bad words:")
        for word in sorted(fake_word_matches):
            print(f"  - {word}")
    else:
        print("\n✓ No bad words found in FAKE words")
    
    total_matches = len(real_word_matches) + len(fake_word_matches)
    print(f"\nTotal bad words found: {total_matches}")
    print("=" * 60)
    
    conn.close()
    
    return {
        'real_words': real_word_matches,
        'fake_words': fake_word_matches,
        'total': total_matches
    }


def remove_bad_words():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return
    
    if not os.path.exists(BAD_WORDS_FILE):
        print(f"Error: Bad words file not found at {BAD_WORDS_FILE}")
        return
    
    with open(BAD_WORDS_FILE, "r", encoding="utf-8") as f:
        bad_words = set(line.strip().lower() for line in f if line.strip())
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    placeholders = ','.join('?' * len(bad_words))
    cur.execute(f"""
        SELECT word_id, name FROM Words 
        WHERE LOWER(name) IN ({placeholders})
    """, list(bad_words))
    
    words_to_delete = cur.fetchall()  # List of (word_id, name) tuples
    
    if not words_to_delete:
        print("No bad words found to remove.")
        conn.close()
        return
    
    print(f"Found {len(words_to_delete)} bad words to remove:")
    for _, name in words_to_delete:
        print(f"  - {name}")
    
    for word_id, name in words_to_delete:
        cur.execute("DELETE FROM Syllable_Indexes WHERE word_id = ?", (word_id,))
        cur.execute("DELETE FROM Words WHERE word_id = ?", (word_id,))
    
    conn.commit()
    conn.close()
    
    print(f"\n✓ Successfully removed {len(words_to_delete)} bad words from database.")


