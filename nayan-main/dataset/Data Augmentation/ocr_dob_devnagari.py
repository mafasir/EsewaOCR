import pandas as pd
import random

df = pd.read_csv("dob_column_sample_100k.csv") 

ocr_confusions = {
    '०': ['O', 'o', 'Q', '०'],
    '१': ['l', 'I', '१'],
    '२': ['Z', '2', '२'],
    '३': ['3', 'E', '३'],
    '४': ['A', '4', '४'],
    '५': ['S', '5', '५'],
    '६': ['G', '6', '६'],
    '७': ['T', '7', '७'],
    '८': ['B', '8', '८'],
    '९': ['g', '9', '९']
}

word_errors = {
    'year': ['साल', 'सा ल', 'साल्', 'स@ल', 'शाल', 'sाल'],
    'month': ['महिना', 'म हिना', 'महीना', 'म@हिना', 'maहिना'],
    'day': ['गते', 'ग ते', 'गते्', 'ग@ते', 'घते', 'gते']
}

def generate_ocr_error(dob):
    try:
        year, month, day = dob.strip().split('-')
        year_ocr = ''.join(random.choice(ocr_confusions[d]) for d in year)
        month_ocr = ''.join(random.choice(ocr_confusions[d]) for d in month)
        day_ocr = ''.join(random.choice(ocr_confusions[d]) for d in day)

        year_label = random.choice(word_errors['year'])
        month_label = random.choice(word_errors['month'])
        day_label = random.choice(word_errors['day'])

        return f"{year_ocr} {year_label} {month_ocr} {month_label} {day_ocr} {day_label}"
    except:
        return ""

df['ocr_dob'] = df['dob'].apply(generate_ocr_error)

df.to_csv("dob_with_ocr_errors.csv", index=False)
print("Saved as dob_with_ocr_errors.csv")
