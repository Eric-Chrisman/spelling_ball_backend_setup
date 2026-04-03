import re

def classify_syllable(syl: str, strip: bool = False):
    if not syl:
        return None
        
    syl = syl.lower().strip()
    vowels = "aeiou"
    vowels_with_y = "aeiouy"
    consonants = "bcdfghjklmnpqrstvwxz"
    
    # Check if syllable has traditional vowels
    has_regular_vowel = any(c in vowels for c in syl)
    
    # If no regular vowels, treat 'y' as a vowel for classification
    active_vowels = vowels if has_regular_vowel else vowels_with_y
    
    # 7. Consonant-le (must be final syllable in word, checked elsewhere)
    # Pattern: consonant + 'le' at end
    if re.match(r"^[bcdfghjklmnpqrstvwxz]le$", syl):
        return "Consonant-le"
    
    # 3. Magic-e (VCe pattern)
    # Pattern: vowel + one or more consonants + silent 'e'
    # Examples: placed, rived, posed, ticed, duced, gaged
    if len(syl) >= 3 and syl[-1] == 'e':
        # Check for vowel + consonant(s) + e
        pattern = r"[" + active_vowels + r"][^" + active_vowels + r"]+e$"
        if re.search(pattern, syl):
            return "Magic-e"
    
    # 6. Diphthong (specific vowel pairs that glide)
    # Must check before vowel team since there's overlap
    if re.search(r"oi|oy|ou|ow", syl):
        return "Diphthong"
    
    # 4. Vowel Team (two vowels together)
    # Common teams: ai, ay, ea, ee, oa, oe, oo, ue, ui, au, aw, ie, ei, ey, io, ia
    if re.search(r"ia|ua|ai|aa|ay|ea|ee|oa|oe|oo|ue|ui|au|aw|ie|ei|ey|io", syl):
        return "Vowel Team"
    
    # 5. R-Controlled (vowel followed by 'r')
    # Include 'yr' when y is acting as vowel (e.g., 'lyr', 'myr', 'tyr')
    if not has_regular_vowel:
        if re.search(r"yr", syl):
            return "R-controlled"
    if re.search(r"[aeiou]r", syl):
        return "R-controlled"
    
    # Check for syllables ending in consonant clusters
    # Examples: lines, syn, selves, piled, gym, myth, crypt
    consonant_pattern = r"[^" + active_vowels + r"]{2,}$"
    if re.search(consonant_pattern, syl):
        vowel_count = sum(1 for c in syl if c in active_vowels)
        if vowel_count >= 1:
            return "Closed"
    
    # 1. Closed Syllable
    # Pattern: vowel(s) followed by one or more consonants
    # Must have consonant at end
    # Examples: gym, myth, sync, crypt (when y is the vowel)
    if syl[-1] in consonants:
        vowel_count = sum(1 for c in syl if c in active_vowels)
        if vowel_count >= 1:
            return "Closed"
    
    # 2. Open Syllable
    # Pattern: ends with a vowel (including 'y' when it acts as vowel)
    if syl[-1] in vowels_with_y:
        return "Open"
    
    # Syllables that don't fit standard patterns
    return "Unknown"