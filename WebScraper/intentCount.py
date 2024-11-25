import yaml

def generate_intents_for_domain(nlu_file, domain_file):
    # Load intents from the nlu.yml file
    with open(nlu_file, 'r') as file:
        nlu_data = yaml.safe_load(file)

    # Extract the list of intents
    intents = [entry.get('intent') for entry in nlu_data.get('nlu', []) if entry.get('intent')]

    if not intents:
        print("No intents found in the NLU file.")
        return

    # Load existing domain.yml file if it exists, otherwise create a new structure
    try:
        with open(domain_file, 'r') as file:
            domain_data = yaml.safe_load(file) or {}
    except FileNotFoundError:
        domain_data = {}

    # Update the intents section in the domain data
    domain_data['intents'] = intents

    # Write the updated domain.yml file
    with open(domain_file, 'w') as file:
        yaml.dump(domain_data, file, default_flow_style=False)

    print(f"Updated domain.yml with {len(intents)} intents.")

# Usage
generate_intents_for_domain('output_nlu.yml', 'domainIntent.yml')