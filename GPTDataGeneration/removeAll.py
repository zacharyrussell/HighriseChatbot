import string

def remove_punctuation_except_colons_and_dashes(input_file, output_file):
    """
    Reads a YAML file as plain text and removes all punctuation except colons and dashes.
    """
    # Create a translation table to remove punctuation except for colons and dashes
    allowed_punctuation = ":-"  # Keep colons and dashes
    punctuation_table = str.maketrans('', '', ''.join(c for c in string.punctuation if c not in allowed_punctuation))

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Remove punctuation from each line, excluding allowed characters
            cleaned_line = line.translate(punctuation_table)
            outfile.write(cleaned_line)

    print(f"Cleaned YAML saved to {output_file}")

# Example usage
input_file = 'extracted_entities.yml'  # Replace with your input YAML file path
output_file = 'output_file_entities.yml'  # Replace with your desired output YAML file path
remove_punctuation_except_colons_and_dashes(input_file, output_file)
