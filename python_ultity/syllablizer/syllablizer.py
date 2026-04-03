vowels = "aeiouy"
consonants = "bcdfghjklmnpqrstvwxyz"

blends = "bl, cl, fl, gl, pl, sl, br, cr, dr, fr, gr, pr, tr, sc, sk, sm, sn, sp, st, sw, tw, wh, wr, ch, sh, th" # return to this later

def word_with_syllables(word, syllables_list):
    # add a semicolon where the syllables split
    for i in range(len(syllables_list)):
        pos = syllables_list[i] + i  # account for previously added semicolons
        word = word[:pos] + ";" + word[pos:]
    print(word)

def syllablizer(word):
    syallbles_list = []

    # first find vowel positions
    vowel_positions = [i for i, letter in enumerate(word) if letter in vowels]
    print(vowel_positions)
    syallbles_list = vowel_positions.copy()
    for i in range(len(syallbles_list)-1):
        syallbles_list[i] += 1  # move to the position after the vowel
    # check le
    # if word.endswith("le") and len(word) > 2:
    #     print()
    #     print(word)
    #     vowel_positions.pop(-1)  # treat 'le' as a vowel position
    #     if word[-3] not in vowels:
    #         syallbles_list.append(len(word)-3)
    #         syallbles_list.append(len(word)-5)
    #     else:
    #         syallbles_list.append(len(word)-2)
    #     word_with_syllables(word, syallbles_list)

    # elif word.endswith("e") and len(word):
    #     vowel_positions.pop(-1)  # don't treat silent 'e' as a vowel position
    # print(vowel_positions)
    # then combine vowel teams
    word_with_syllables(word, syallbles_list)
    return syallbles_list