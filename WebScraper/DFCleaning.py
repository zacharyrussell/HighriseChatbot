import pandas as pd
import re
import ast
# Specify the file path
file_path = './aggregateDF.csv'  # Ensure the correct file extension is used (likely .csv)


# Load the DataFrame from the CSV file
df = pd.read_csv(file_path, sep='\t', quotechar='"')
print("CSV file loaded successfully.")
df.to_json('jsonData.json', orient='records', lines=True)


# # Function to remove emojis
# def remove_emojis(text):
#     emoji_pattern = re.compile(
#         "["
#         "\U0001F600-\U0001F64F"  # emoticons
#         "\U0001F300-\U0001F5FF"  # symbols & pictographs
#         "\U0001F680-\U0001F6FF"  # transport & map symbols
#         "\U0001F700-\U0001F77F"  # alchemical symbols
#         "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
#         "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
#         "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
#         "\U0001FA00-\U0001FA6F"  # Chess Symbols
#         "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
#         "\U00002702-\U000027B0"  # Dingbats
#         "\U000024C2-\U0001F251"  # Enclosed characters
#         "]+", flags=re.UNICODE
#     )
#     return emoji_pattern.sub(r"", text) if isinstance(text, str) else text

# Apply the function to all columns
# df = df.applymap(remove_emojis)
# df["Paragraphs"] = df["Paragraphs"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
# # Display the modified DataFrame
# print(df)
# ar = df['Paragraphs']
# print(type(ar[0]))
# print(df['Paragraphs'][0])
# print(df.shape)


# df.to_csv("aggregateDF.csv", sep='\t', index = False)
# df = df.drop(index=0)
# df.columns = ['index', 'Header', 'Paragraphs']
# print(df['Paragraphs'])



