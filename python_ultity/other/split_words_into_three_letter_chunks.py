import sqlite3
import os

# ---------- CONFIG ----------
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "..", "..", "datasets", "test_database.db")
WORDS_FILE = os.path.join(BASE_DIR, "..", "..", "datasets", "filtered_words.txt")
# ----------------------------

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Ensure table exists (with weight column)
cur.execute("""
CREATE TABLE IF NOT EXISTS three_chars (
    col1 CHAR(1) NOT NULL,
    col2 CHAR(1) NOT NULL,
    col3 CHAR(1) NOT NULL,
    weight INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (col1, col2, col3)
)
""")

# Load words
with open(WORDS_FILE, "r") as f:
    words = [line.strip().lower() for line in f if line.strip()]

# Process each word into overlapping 3-char chunks
for word in words:
    if len(word) < 3:
        continue

    for i in range(len(word) - 2):
        chunk = word[i:i+3]
        col1, col2, col3 = chunk[0], chunk[1], chunk[2]

        # Insert new chunk, or add +1 to weight if already exists
        cur.execute("""
            INSERT INTO three_chars (col1, col2, col3, weight)
            VALUES (?, ?, ?, 1)
            ON CONFLICT(col1, col2, col3) DO UPDATE SET weight = weight + 1
        """, (col1, col2, col3))

conn.commit()
cur.close()
conn.close()

print("✅ Finished inserting 3-letter chunks with weights into test_database.db")