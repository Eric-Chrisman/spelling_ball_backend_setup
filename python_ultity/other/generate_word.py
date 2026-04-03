import random

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"

# Some syllable templates
TEMPLATES = ["CV", "CVC", "VC", "V"]

def make_syllable(template=None):
    if template is None:
        template = random.choice(TEMPLATES)
    s = ""
    for t in template:
        if t == "C":
            s += random.choice(CONSONANTS)
        else:
            s += random.choice(VOWELS)
    return s

def generate_word(syllables=3):
    return "".join(make_syllable() for _ in range(syllables))

# Example usage
for i in range(5):
    for n in [2, 3, 4]:
        word = generate_word(syllables=n)
        print(f"{word} ({n} syllables)")