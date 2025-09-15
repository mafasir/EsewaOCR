import pandas as pd
import random

random.seed(42)

CONFUSION_MATRIX = {
    'o': ['0'], 'O': ['0'], 'l': ['1'], 'I': ['1'], 'z': ['2'], 'Z': ['2'],
    's': ['5', '8'], 'S': ['5', '$'], 'b': ['6', '8'], 'B': ['8'],
    'g': ['9', '6'], 'G': ['6'], 'q': ['9'], 'e': ['3'],

    'a': ['@'], 'c': ['('], 'i': ['!'], 't': ['+'], 'A': ['^'],

    'c': ['e'], 'u': ['v'], 'v': ['u', 'y'], 'w': ['vv', 'v v'], 'm': ['n'],
    'n': ['m', 'h', 'r'], 'h': ['b'], 'k': ['h', 'x'], 'f': ['t'],
    'j': ['i'], 'E': ['F'], 'd': ['b'], 'p': ['q'],

    'm': ['rn', 'r n', 'nn', 'n n'], 'w': ['vv', 'v v'], 'd': ['cl', 'c l'],
    'h': ['li', 'l i'], 'b': ['lɔ'],
    'rn': ['m'], 'nn': ['m', 'n'], 'cl': ['d'], 'li': ['h'], 'vv': ['w'],
    'ij': ['y'], 'oo': ['u'], 'ck': ['k', 'h'], 'fi': ['a', 'h'],
    'fl': ['a'], 'in': ['m'],

    '.': [',', ';', ':'], ',': ['.', ';'], '-': ['_', '—'], ' ': ['  ', ''],
}


def substitute_chars(text, prob=0.05):
    output = ""
    i = 0
    while i < len(text):
        found_multi_char_sub = False
        for key in [k for k in CONFUSION_MATRIX if len(k) > 1]:
            if text[i:i+len(key)] == key and random.random() < prob:
                output += random.choice(CONFUSION_MATRIX[key])
                i += len(key)
                found_multi_char_sub = True
                break
        if found_multi_char_sub:
            continue

        char = text[i]
        if char in CONFUSION_MATRIX and random.random() < prob:
            output += random.choice(CONFUSION_MATRIX[char])
        else:
            output += char
        i += 1
    return output

def insert_delete_chars(text, insert_prob=0.02, delete_prob=0.02):
    output = ""
    for char in text:
        if random.random() < delete_prob:
            continue
        if random.random() < insert_prob:
            spurious_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?`~"
            output += random.choice(spurious_chars)
        output += char
    return output

def merge_split_words(text, merge_prob=0.08, split_prob=0.03):
    words = text.split(' ')
    if len(words) < 2:
        return text

    if random.random() < merge_prob:
        idx_to_merge = random.randint(0, len(words) - 2)
        words[idx_to_merge] += words[idx_to_merge + 1]
        del words[idx_to_merge + 1]

    if random.random() < split_prob:
        word_to_split_idx = random.randint(0, len(words) - 1)
        word = words[word_to_split_idx]
        if len(word) > 2:
            split_point = random.randint(1, len(word) - 1)
            words[word_to_split_idx] = word[:split_point]
            words.insert(word_to_split_idx + 1, word[split_point:])
    
    return ' '.join(words)

def simulate_ocr_on_name(name):
    max_attempts = 10  
    for _ in range(max_attempts):
        ocr_name = merge_split_words(name, merge_prob=0.1, split_prob=0.05)
        ocr_name = substitute_chars(ocr_name, prob=0.05)
        ocr_name = insert_delete_chars(ocr_name, insert_prob=0.02, delete_prob=0.02)
        if ocr_name != name:
            return ocr_name
    return ocr_name + random.choice(['*', '~', '!'])

df = pd.read_csv('genderrr.csv')

ocr_dataset = []
for name in df["gender"]:
    ocr_name = simulate_ocr_on_name(name)
    ocr_dataset.append({'clean': name, 'ocr': ocr_name})

ocr_df = pd.DataFrame(ocr_dataset)

output_file_name = 'genderr_ocr.csv'
ocr_df.to_csv(output_file_name, index=False)

print(f"OCR simulated names saved to {output_file_name}")
