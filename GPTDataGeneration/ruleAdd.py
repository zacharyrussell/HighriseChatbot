import yaml

# Input and output file paths
RULES_FILE = "rules2.yml"
OUTPUT_FILE = "rules_updated.yml"
ACTION_TO_ADD = "action_log_and_request_feedback"

def add_action_to_steps(file_path, output_path, action):
    try:
        # Read the YAML file
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        # Check for "rules" section and update each rule's steps
        if "rules" in data:
            for rule in data["rules"]:
                if "steps" in rule:
                    # Check if the action is already present; if not, add it
                    if {"action": action} not in rule["steps"]:
                        rule["steps"].append({"action": action})

        # Write updated content back to a new file
        with open(output_path, "w") as output_file:
            yaml.dump(data, output_file, default_flow_style=False)
        
        print(f"Updated rules saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")

# Run the script
add_action_to_steps(RULES_FILE, OUTPUT_FILE, ACTION_TO_ADD)
