import re
import string

def remove_punctuation_in_brackets_and_parentheses(input_file, output_file):
    """
    Reads a YAML file as plain text and removes all punctuation inside square brackets or parentheses.
    """
    # Regex to match square brackets or parentheses with content inside
    bracket_parenthesis_pattern = re.compile(r"(\[|\()(.*?)(\]|\))")

    # Function to remove punctuation inside brackets or parentheses
    def clean_content(match):
        open_bracket = match.group(1)
        content = match.group(2)
        close_bracket = match.group(3)
        # Remove all punctuation from the content
        cleaned_content = content.translate(str.maketrans('', '', string.punctuation))
        return f"{open_bracket}{cleaned_content}{close_bracket}"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Clean the line by removing punctuation inside brackets and parentheses
            cleaned_line = bracket_parenthesis_pattern.sub(clean_content, line)
            outfile.write(cleaned_line)

    print(f"Cleaned YAML saved to {output_file}")

# Example usage
input_file = 'nlu.yml'  # Replace with your input YAML file path
output_file = 'output_file_nlu.yml'  # Replace with your desired output YAML file path
remove_punctuation_in_brackets_and_parentheses(input_file, output_file)
