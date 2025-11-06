##EXCEL CLEANSE / IMPORT .CSV FILES##

# 1. Import libraries
import pandas as pd
import os

# 2. Define folder structure
folder_path = r"C:\Users\danhe\OneDrive\Desktop\Data Science BSC\Professional Practice\Projects\Idea 1 - Cannabis Legislisation in Canada\Canada CPI"

# 3. Identify files to open
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
# Define an empty list to hold all dataframes for later in process

all_dfs = []

# Define parameters to be removed from clean text later
def clean_product_category(text):
    """Clean product category names"""
    if isinstance(text, str):
        # Remove everything after '(' including the bracket
        text = text.split('(')[0]
        # Remove any trailing numbers and spaces
        text = ''.join([i for i in text if not i.isdigit()]).strip()
        # Remove any double spaces
        text = ' '.join(text.split())
        # Remove all text after commas
        text = text.split(',')[0]
        # Remove all special characters except spaces and hyphens
        text = ''.join(e for e in text if e.isalnum() or e in [' ', '-'])
        return text
    return text

artefacts = ['symbol legend', 'footnotes', 'how to cite']

# 4. Read the files
for file in files:
    # Read CSV file
    df = pd.read_csv(
        os.path.join(folder_path, file),
        skiprows=lambda x: x in list(range(9)) + [10],
        encoding='cp1252',
        nrows=30
    )

    # Rename the column before any other operations
    df = df.rename(columns={df.columns[0]: 'Product Category'})

    # Handle the 'Services' category special case
    if len(df.index) >= 26:
        if pd.notna(df.iloc[25, 4]):
            services_value = df.iloc[25, 4]
            if pd.isna(df.iloc[25, 0]):
                df.iloc[25, 0] = services_value

    # Clean Product Category names using the new function
    df['Product Category'] = df['Product Category'].apply(clean_product_category)
    df['Product Category'] = df['Product Category'].str.strip().str.lower()
    df = df[~df['Product Category'].isin(artefacts)]
    df = df.drop_duplicates(subset=['Product Category'])

    # Keep first 6 columns only
    df = df.iloc[:, :6]

    # Remove NaN values after cleaning
    df = df.dropna(subset=['Product Category'])
    df = df.dropna(how='all')

    # Clean column names - keeps original formatting
    new_columns = ['Product Category']
    for col in df.columns[1:]:
        if pd.notna(col) and col.strip():
            new_columns.append(col.strip())
    df.columns = new_columns

    # Store the processed dataframe
    all_dfs.append(df)
    print(f"Processed {file} with columns: {new_columns}")

# Merge all dataframes into a single dataframe on Product Category
final_df = all_dfs[0]
for df in all_dfs[1:]:
    final_df = final_df.merge(df, on='Product Category', how='outer')

# Save to CSV with overwrite
output_path = os.path.join(folder_path, 'CPI_Combined_TimeSeries.csv')
try:
    final_df.to_csv(output_path, index=False, mode='w')
    print(f"\nSuccessfully saved to: {output_path}")
except PermissionError:
    print(f"\nError: Cannot write to {output_path}. File may be open in another program.")
    alternative_path = os.path.join(folder_path, 'CPI_Combined_TimeSeries_new.csv')
    final_df.to_csv(alternative_path, index=False)
    print(f"Saved to alternative location: {alternative_path}")

print(f"Final dataset shape: {final_df.shape}")

# 10. Format data
# 11. Combine data
