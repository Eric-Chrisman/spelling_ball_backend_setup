import sqlite3
import os
import random

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "..","datasets", "Words.db")


def get_random_syllable(cur):
    cur.execute("""
        SELECT syllable 
        FROM Syllables
        WHERE syllable_type IS NOT NULL
        ORDER BY RANDOM() 
        LIMIT 1
    """)
    row = cur.fetchone()
    return row[0] if row else None


def get_following_syllables(cur, last_two):
    cur.execute("""
        SELECT DISTINCT syllable
        FROM Syllables
        WHERE syllable_type IS NOT NULL
          AND syllable LIKE ?
    """, (last_two + '%',))
    rows = cur.fetchall()
    return [row[0] for row in rows]


def generate_word(length=5):
    if length < 3 or length > 10:
        raise ValueError("Word length must be between 3 and 10")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Pick a random starting syllable
    chunk = get_random_syllable(cur)
    if not chunk or len(chunk) > length:
        conn.close()
        return None

    word = chunk

    # Extend word until reaching desired length
    attempts = 0
    max_attempts = 100
    
    while len(word) < length and attempts < max_attempts:
        last_two = word[-2:]
        options = get_following_syllables(cur, last_two)
        
        if not options:
            # Dead end - try a random syllable
            random_syl = get_random_syllable(cur)
            if random_syl and len(word) + len(random_syl) <= length:
                word += random_syl
            else:
                break
        else:
            # Filter options that won't exceed target length
            valid_options = [opt for opt in options if len(word) + len(opt) <= length]
            if valid_options:
                next_chunk = random.choice(valid_options)
                word += next_chunk
            else:
                break
        
        attempts += 1

    conn.close()

    # Check if we generated a word that already exists in real words
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM Words WHERE name = ? AND is_real = 1", (word,))
    is_real = cur.fetchone() is not None
    conn.close()

    # Only accept words of exact requested length and not in real words list
    if len(word) == length and not is_real:
        return word
    return None