import os
from nonsence_word_generator import generate_word

# ---------- CONFIG ----------
BASE_DIR = os.path.dirname(__file__)
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "..", "datasets", "generated_words.txt")
# ----------------------------

def main():
    try:
        num_words = int(input("How many words do you want to generate? "))
        length = int(input("How long should each word be (3–10)? "))
    except ValueError:
        print("❌ Please enter valid numbers.")
        return

    words = []
    while len(words) < num_words:
        word = generate_word(length)
        if word and word not in words:  # ensure uniqueness in this run
            words.append(word)

    words.sort()
    # Write to file
    with open(OUTPUT_FILE, "w") as f:
        for w in words:
            f.write(w + "\n")

    # Print to terminal
    print("\nGenerated words:")
    print("\n".join(words))
    print(f"\n✅ Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()