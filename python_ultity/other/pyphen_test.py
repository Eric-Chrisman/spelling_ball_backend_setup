import pyphen

# Initialize Pyphen with English
dic = pyphen.Pyphen(lang='en')

word = "abandon"
split_word = dic.inserted(word)

print("Original word:", word)
print("Syllables:", split_word)