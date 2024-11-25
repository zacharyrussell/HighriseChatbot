import pandas as pd

file_path = './aggregateDF.csv'  # Ensure the correct file extension is used (likely .csv)


# Load the DataFrame from the CSV file
df = pd.read_csv(file_path, sep='\t', quotechar='"')
print(df.head)
# Extract the 'headers' column
headers_df = df[['Header']]  # Select only the 'headers' column

# Save to Excel
file_path = 'output.xlsx'
headers_df.to_excel(file_path, index=False, header=False)  # `header=False` removes column name in the file

print(f"Data successfully written to {file_path}.")
