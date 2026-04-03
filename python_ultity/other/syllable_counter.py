import syllables

words = ["poem", "giant", "naive", "ruin", "theater"]

for w in words:
    print(f"{w}: {syllables.estimate(w)} syllable(s)")