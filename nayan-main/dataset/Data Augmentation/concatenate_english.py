import pandas as pd
import numpy as np

try:
    df = pd.read_csv('new dataset.csv')

    df.fillna('', inplace=True)

    df['Clean ID Number'] = df['Clean ID Number'].apply(lambda x: str(int(float(x))) if x != '' else '')

    df['Clean DOB'] = pd.to_datetime(df['Clean DOB'], errors='coerce')

    df['Clean DOB'] = df['Clean DOB'].dt.strftime('%Y-%m-%d').fillna('')

    df['input_text'] = 'ID: ' + df['OCR ID Number'].astype(str) + \
                     ', Name: ' + df['OCR Name'].astype(str) + \
                     ', DOB: ' + df['OCR DOB'].astype(str) + \
                     ', Gender: ' + df['OCR Gender'].astype(str) + \
                     ', District: ' + df['OCR District'].astype(str) + \
                     ', Municipality: ' + df['OCR Municipality'].astype(str) + \
                     ", Father's name: " + df["OCR Father's Name"].astype(str) + \
                     ", Mother's name: " + df["OCR Mother's Name"].astype(str)

    df['output_text'] = 'ID: ' + df['Clean ID Number'].astype(str) + \
                      ', Name: ' + df['Clean Name'].astype(str) + \
                      ', DOB: ' + df['Clean DOB'].astype(str) + \
                      ', Gender: ' + df['Clean Gender'].astype(str) + \
                      ', District: ' + df['Clean District'].astype(str) + \
                      ', Municipality: ' + df['Clean Municipality'].astype(str) + \
                      ", Father's Name: " + df["Clean Father's Name"].astype(str) + \
                      ", Mother's Name: " + df["Clean Mother's Name"].astype(str)

    processed_df = df[['input_text', 'output_text']]

    processed_df.to_csv('processed_dataset_int_id2.csv', index=False)

    print("Successfully processed the dataset and created 'processed_dataset_int_id.csv'")
    print("Here's a preview of the processed data with ID as an integer:")
    print(processed_df.head())

except FileNotFoundError:
    print("The file 'updated_dataset.csv' was not found. Please make sure the file is uploaded and the name is correct.")
except Exception as e:
    print(f"An error occurred: {e}")