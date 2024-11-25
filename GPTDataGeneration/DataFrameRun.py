import pandas as pd
import re
import ast
from Generate import process_topic_with_gpt
# Specify the file path
file_path = 'C:/Users/Zach/Desktop/PocketWorldsProject/WebScraper/aggregateDF.csv'  # Ensure the correct file extension is used (likely .csv)

# Specify output files
output_file_nlu = "nlu.yml"
output_file_responses = "responses.yml"

# Load the DataFrame from the CSV file
df = pd.read_csv(file_path, sep='\t', quotechar='"')

for _, row in df.iterrows():
    header = row["Header"]
    print(header)
    paragraph = row["Paragraphs"]
    process_topic_with_gpt(header, paragraph, output_file_nlu, output_file_responses)