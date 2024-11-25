import openai
import os
import re
from collections import OrderedDict
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
# Set your OpenAI API key
openai.api_key = "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"
yaml = YAML()
yaml.default_flow_style = False

# File paths
input_file = "nlu.yml"  # Input file containing intents and examples
annotated_intents_file = "annotated_intents.yml"  # Output file for annotated intents
entities_file = "extracted_entities.yml"  # Output file for entity definitions

def load_yaml(file_path):
    try:
        with open(file_path, "r") as f:
            return yaml.load(f)
    except FileNotFoundError:
        # Return default structure if file doesn't exist
        if "nlu" in file_path:
            return {"nlu": []}
        return {"entities": []}

def save_yaml(data, file_path):
    with open(file_path, "w") as f:
        yaml.dump(data, f)


# Function to call ChatGPT for entity annotation
def annotate_examples(intent_name, examples):
    prompt = f"""
    You are a chatbot expert. Your task is to annotate examples with entities for the intent '{intent_name}'.

    Add entity annotations by enclosing entities in square brackets and labeling them in parentheses.

    For example:
    - What is [pinning](feature)?
    - Can you tell me about the [pin](feature) function?

    Here are the examples:
    {examples}

    Return the annotated examples line by line, with no extra formatting. At the end, provide a list of entities extracted from the examples in the format: Entities: entity_name1, entity_name2.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert entity annotator."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling ChatGPT for intent '{intent_name}': {e}")
        return None

def process_intents(input_file, nlu_output_file, entities_output_file):
    # Load input data and initialize outputs
    data = load_yaml(input_file)
    updated_nlu = load_yaml(nlu_output_file)
    if updated_nlu is None or "nlu" not in updated_nlu:
        updated_nlu = {"version": data.get("version", "3.1"), "nlu": []}

    # Load or initialize entities
    extracted_entities = set(load_yaml(entities_output_file).get("entities", []))

    for intent in data["nlu"]:
        intent_name = intent["intent"]
        examples = intent["examples"]

        # Call ChatGPT to annotate examples
        print(f"Processing intent: {intent_name}")
        result = annotate_examples(intent_name, examples)
        if result:
            # Extract examples and entities from GPT response
            lines = result.split("\n")
            annotated_examples = [line.strip() for line in lines if line.strip() and not line.startswith("Entities:")]
            entity_line = next((line for line in lines if line.startswith("Entities:")), None)

            # Add entities to the set
            if entity_line:
                entities = entity_line.replace("Entities:", "").strip().split(", ")
                extracted_entities.update(entities)

            # Add annotated intent to updated NLU data
            updated_nlu["nlu"].append({
                "intent": intent_name.strip("- "),
                "examples": LiteralScalarString("\n".join(f"{example}" for example in annotated_examples))
            })

            # Save updated NLU and entities after processing each intent
            save_yaml(updated_nlu, nlu_output_file)
            save_yaml({"entities": list(extracted_entities)}, entities_output_file)
            print(f"Annotated examples for intent '{intent_name}' saved.")
        else:
            print(f"No response for intent '{intent_name}'. Skipping.")

    print(f"Processing complete. NLU saved to {nlu_output_file}, entities saved to {entities_output_file}.")

# Run the script
if __name__ == "__main__":
    process_intents(input_file, annotated_intents_file, entities_file)