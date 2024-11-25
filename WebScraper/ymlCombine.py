import yaml

def combine_nlu_and_responses(nlu_file, responses_file, output_file):
    # Load the NLU and Responses files
    with open(nlu_file, 'r') as file:
        nlu_data = yaml.safe_load(file)

    with open(responses_file, 'r') as file:
        responses_data = yaml.safe_load(file)

    # Extract responses dictionary
    responses = responses_data.get('responses', {})

    # Create rules structure
    rules = {'rules': []}

    for nlu_entry in nlu_data.get('nlu', []):
        intent = nlu_entry.get('intent')
        examples = nlu_entry.get('examples', '')

        if not intent or not examples:
            print(f"Skipping invalid NLU entry: {nlu_entry}")
            continue

        # Find the corresponding response
        response = responses.get(f'utter_{intent}')
        if not response:
            print(f"No matching response found for intent: {intent}")
            continue

        # Add a rule for the intent and response
        rule = {
            'rule': f"Respond to {intent}",
            'steps': [
                {'intent': intent},
                {'action': f'utter_{intent}'}
            ]
        }
        rules['rules'].append(rule)

    # Write the combined rules to the output file
    with open(output_file, 'w') as file:
        yaml.dump(rules, file, default_flow_style=False)

    print(f"Combined rules written to {output_file}")

# Usage
combine_nlu_and_responses('output_nlu.yml', 'output.yml', 'output_rules.yml')
