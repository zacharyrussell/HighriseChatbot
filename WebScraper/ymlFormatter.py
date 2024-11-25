def combine_responses_as_text(input_file, output_file):
    combined_responses = []
    in_responses = False

    with open(input_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        # Detect the start of a new 'responses:' section
        if line.strip().startswith('nlu:'):
            in_responses = True
            continue  # Skip the 'responses:' line itself

        # Collect lines under the current 'responses:' section
        if in_responses:
            # Stop collecting if we encounter a new top-level key
            if not line.startswith(' ') and not line.strip().startswith('-'):
                in_responses = False
            else:
                combined_responses.append(line)

    # Write the combined 'responses:' section to the output file
    with open(output_file, 'w') as file:
        file.write('nlu:\n')
        file.writelines(combined_responses)

    print(f"Combined `nlu:` sections written to {output_file}")



# Usage
# combine_responses_as_text('cleaned_file_nlu.yml', 'output_nlu.yml')


def remove_backticks(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()
    
    # Remove all backticks
    cleaned_content = content.replace('`', '')

    # Write the cleaned content back to a new file
    with open(output_file, 'w') as file:
        file.write(cleaned_content)

    print(f"All backticks removed. Cleaned file written to {output_file}")

# Usage
# remove_backticks('nlu.yml', 'cleaned_file_nlu.yml')



import yaml

def rename_responses_by_order(nlu_file, responses_file, output_file):
    # Load the NLU and Responses files
    with open(nlu_file, 'r') as file:
        nlu_data = yaml.safe_load(file)

    with open(responses_file, 'r') as file:
        responses_data = yaml.safe_load(file)

    # Extract intents and responses in order
    intents = [entry.get('intent') for entry in nlu_data.get('nlu', []) if entry.get('intent')]
    responses = list(responses_data.get('responses', {}).items())

    # Check for mismatched lengths
    if len(intents) != len(responses):
        print(f"Error: Number of intents ({len(intents)}) does not match number of responses ({len(responses)}).")
        return

    # Create a new responses dictionary with properly named keys
    updated_responses = {}
    for intent, (response_key, response_value) in zip(intents, responses):
        updated_responses[f'utter_{intent}'] = response_value

    # Write the updated responses to a new file
    with open(output_file, 'w') as file:
        yaml.dump({'responses': updated_responses}, file, default_flow_style=False)

    print(f"Renamed responses written to {output_file}")

# Usage
rename_responses_by_order('output_nlu.yml', 'output.yml', 'updated_responses.yml')

