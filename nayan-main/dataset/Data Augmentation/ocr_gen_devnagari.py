import pandas as pd
import numpy as np
import random
import os
import time

CONFUSION_MATRIX = {
    'भ': ['म'], 'म': ['भ', 'ऩ'], 'ध': ['घ'], 'घ': ['ध'], 'ष': ['प'], 'प': ['ष', 'य'],
    'व': ['ब'], 'ब': ['व'], 'ठ': ['ढ'], 'ढ': ['ठ'], 'ण': ['ए', 'ग'], 'ए': ['ण'],
    'न': ['त'], 'त': ['न'], 'ट': ['त'], 'श': ['य', 'स'],
    'ि': ['ी', ''], 'ी': ['ि', ''], 'ु': ['ू', ''], 'ू': ['ु', ''], 'े': ['ै'], 'ै': ['े'],
    'ो': ['ौ'], 'ौ': ['ो'], 'ं': ['ँ', ''], 'ँ': ['ं'], 'ा': [''], 'र्': [''],
    'क्ष': ['क् ष', 'क ्ष', 'छ'], 'त्र': ['त् र', 'ज्ञ'], 'ज्ञ': ['ग् य', 'त्र'],
    'द्य': ['द् य'], 'प्र': ['पर्'], 'श्र': ['शर्'], 'द्ध': ['दध'], 'क्क': ['कक'],
    'ख': ['रव', 'र व'], 'भ': ['म ा', 'भा'],
    'रव': ['ख'], 'ग्य': ['ज्ञ'],
    
    '।': ['l', '1', '.'], ',': ['.', ';'], '-': ['_', '—', ' '],
    'o': ['०'], 'O': ['०'], '0': ['०', 'o', 'O'],
    '1': ['१', 'l', '।'], 'l': ['१', '।'],
    '2': ['२', 'z', 'Z'], 'Z': ['२'],
    '3': ['३', '8'], '8': ['३', 'B', 'b'],
    '4': ['४', 'y'],
    '5': ['५', 's', 'S', '6'], 's': ['५', 'S'],
    '6': ['६', 'b', 'g', '5'], 'b': ['६', '8'],
    '7': ['७'],
    '9': ['९', 'g'], 'g': ['९', '6'],
}

def substitute_chars(text, prob=0.04):
    output = ""; i = 0; text = str(text)
    while i < len(text):
        char = text[i]
        if char in CONFUSION_MATRIX and random.random() < prob:
            output += random.choice(CONFUSION_MATRIX[char])
        else: output += char
        i += 1
    return output

def insert_delete_chars(text, insert_prob=0.01, delete_prob=0.01):
    output = ""; text = str(text)
    for char in text:
        if random.random() < delete_prob: continue
        if random.random() < insert_prob:
            output += random.choice("!@#$%^&*()_+-=,.")
        output += char
    return output

def merge_split_words(text, merge_prob=0.05, split_prob=0.03):
    text = str(text); words = text.split(' ')
    if len(words) < 2: return text
    if random.random() < merge_prob and len(words) > 1:
        idx = random.randint(0, len(words) - 2)
        words[idx] += words[idx + 1]
        del words[idx + 1]
    if random.random() < split_prob and words:
        idx = random.randint(0, len(words) - 1)
        word = words[idx]
        if len(word) > 2:
            split_point = random.randint(1, len(word) - 1)
            words[idx] = word[:split_point]
            words.insert(idx + 1, word[split_point:])
    return ' '.join(words)


def apply_guaranteed_ocr_errors(text, error_types=['substitute', 'insert_delete', 'merge_split']):
    if pd.isna(text):
        return text
    
    original_text = str(text)
    noisy_text = original_text

    if 'substitute' in error_types:
        noisy_text = substitute_chars(noisy_text)
    if 'insert_delete' in error_types:
        noisy_text = insert_delete_chars(noisy_text)
    if 'merge_split' in error_types:
        noisy_text = merge_split_words(noisy_text)

    if noisy_text == original_text:
        if len(noisy_text) > 1:
            idx = random.randint(0, len(noisy_text) - 2)
            char_list = list(noisy_text)
            char_list[idx], char_list[idx+1] = char_list[idx+1], char_list[idx]
            noisy_text = "".join(char_list)
        else:
            noisy_text += random.choice(['*', '~', '।'])
            
    return noisy_text

INPUT_FILE = 'final_voter_data_with_random_ids.csv' 
OUTPUT_FILE = 'final_voter_data_GUARANTEED_ERRORS.csv'
CHUNKSIZE = 100_000

if not os.path.exists(INPUT_FILE):
    print(f"ERROR: Input file '{INPUT_FILE}' not found.")
    exit()

print(f"Starting GUARANTEED OCR error generation for '{INPUT_FILE}'...")

start_time = time.time()
records_processed = 0
header_written = False

try:
    chunk_iterator = pd.read_csv(INPUT_FILE, chunksize=CHUNKSIZE, encoding='utf-8')

    for i, chunk in enumerate(chunk_iterator):
        text_cols = ['voter_name', 'voter_gender', 'district', 'municipality', 'father_name', 'mother_name']
        structured_cols = ['id_number', 'dob']

        for col in text_cols:
            if col in chunk.columns:
                # Apply full suite of errors
                chunk[f'{col}_ocr'] = chunk[col].apply(lambda x: apply_guaranteed_ocr_errors(x, error_types=['substitute', 'insert_delete', 'merge_split']))
        
        for col in structured_cols:
            if col in chunk.columns:
                chunk[f'{col}_ocr'] = chunk[col].apply(lambda x: apply_guaranteed_ocr_errors(x, error_types=['substitute', 'insert_delete']))
        
        final_columns = []
        original_columns = ['id_number', 'voter_name', 'voter_gender', 'district', 'municipality', 'father_name', 'mother_name', 'dob']
        for col in original_columns:
            if col in chunk.columns:
                final_columns.append(col)
                if f'{col}_ocr' in chunk.columns:
                    final_columns.append(f'{col}_ocr')
        
        chunk = chunk[final_columns]
        
        if not header_written:
            chunk.to_csv(OUTPUT_FILE, mode='w', header=True, index=False, encoding='utf-8-sig')
            header_written = True
        else:
            chunk.to_csv(OUTPUT_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

        records_processed += len(chunk)
        print(f"  Processed {records_processed:,.0f} records...")

    end_time = time.time()
    total_time = end_time - start_time
    print("\n" + "="*50)
    print(f"Success! OCR error generation complete.")
    print(f"Total time taken: {total_time:.2f} seconds.")
    print(f"The final dataset with GUARANTEED errors has been saved to: '{OUTPUT_FILE}'")
    print("="*50)

except Exception as e:
    print(f"\nAn error occurred during processing: {e}")