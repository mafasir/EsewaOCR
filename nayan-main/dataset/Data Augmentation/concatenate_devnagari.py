import pandas as pd
import os
import time

INPUT_FILE = 'merged_voter_sample_with_dob.csv'  
OUTPUT_FILE = 'mt5_training_dataset_nepali.csv'     

COLUMN_LABELS = {
    'id_number': 'आईडी',
    'name': 'नाम',
    'dob': 'जन्म मिति',
    'gender': 'लिङ्ग',
    'district': 'जिल्ला',
    'municipality': 'नगरपालिका',
    'father_name': 'बुबाको नाम',
    'mother_name': 'आमाको नाम'
}

FIELD_ORDER = ['id_number', 'name', 'dob', 'gender', 'district', 'municipality', 'father_name', 'mother_name']

CHUNKSIZE = 100_000

def format_row_as_string(row, column_suffix=''):
    parts = []
    for base_col_name in FIELD_ORDER:
        col_name_to_find = base_col_name + column_suffix
        
        if col_name_to_find in row and pd.notna(row[col_name_to_find]):
            label = COLUMN_LABELS.get(base_col_name)
            value = row[col_name_to_find]
            parts.append(f"{label}: {value}")
            
    return ", ".join(parts)

if not os.path.exists(INPUT_FILE):
    print(f" ERROR: Input file '{INPUT_FILE}' not found.")
    exit()

print(f" Starting to reformat data from '{INPUT_FILE}' for model training...")
print(f"Output will be saved to '{OUTPUT_FILE}'.")

start_time = time.time()
records_processed = 0
header_written = False

try:
    chunk_iterator = pd.read_csv(INPUT_FILE, chunksize=CHUNKSIZE, encoding='utf-8')

    for i, chunk in enumerate(chunk_iterator):
        
        output_texts = chunk.apply(lambda row: format_row_as_string(row, column_suffix=''), axis=1)
        
        input_texts = chunk.apply(lambda row: format_row_as_string(row, column_suffix='_ocr'), axis=1)

        output_chunk_df = pd.DataFrame({
            'input_text': input_texts,
            'output_text': output_texts
        })

        if not header_written:
            output_chunk_df.to_csv(OUTPUT_FILE, mode='w', header=True, index=False, encoding='utf-8-sig')
            header_written = True
        else:
            output_chunk_df.to_csv(OUTPUT_FILE, mode='a', header=False, index=False, encoding='utf-8-sig')

        records_processed += len(chunk)
        print(f"  Processed and reformatted {records_processed:,.0f} records...")

    end_time = time.time()
    total_time = end_time - start_time

    print("\n" + "="*50)
    print(f" Success! Data reformatting complete.")
    print(f"Total records processed: {records_processed:,.0f}")
    print(f"Total time taken: {total_time:.2f} seconds.")
    print(f"Training-ready file saved to: '{OUTPUT_FILE}'")
    print("="*50)

except Exception as e:
    print(f"\n An error occurred during processing: {e}")