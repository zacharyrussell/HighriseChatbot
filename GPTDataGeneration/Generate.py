import openai
import yaml

from dotenv import load_dotenv
import os 
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def process_topic_with_gpt(topic, text, output_file_nlu, output_file_responses):
    """
    Process a topic header and text to split it into Rasa-compatible intents, examples, and responses.
    Append the new intents to an `nlu` file and responses to a `responses` file.
    """
    # Define the GPT prompt
    prompt = f"""
You are a chatbot assistant specializing in generating YAML for Rasa. Given a topic and some text, 
split the text into multiple intents, each with examples and corresponding responses, revolving around the topic.

Topic: {topic}

Text:
{text}

Provide the output in the following YAML structure:
- The `nlu` section should contain all intents with 3-5 examples each.
- The `responses` section should contain all bot responses with unique names.
- Do not include `nlu:` and `responses:` together in the same YAML block.
- Separate them logically so that `nlu:` data is valid for one file and `responses:` is valid for another.
- Use proper YAML indentation and formatting for compatibility with Rasa.

Return the output in two sections:
1. NLU Section (for the intents)
2. Responses Section (for the bot responses)
    """

    # Call the GPT API
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant generating YAML for Rasa intents and responses."},
            {"role": "user", "content": prompt}
        ]
    )

    # Get the generated YAML output
    output = response.choices[0].message['content']

    # Split the generated output into NLU and Responses sections
    try:
        nlu_start = output.index("nlu:")
        responses_start = output.index("responses:")
    except ValueError as e:
        print("Error: GPT did not return the expected structure. Please check the response.")
        print("GPT Output:\n", output)
        return

    # Extract each section
    nlu_section = output[nlu_start:responses_start].strip()
    responses_section = output[responses_start:].strip()

    # Append the NLU section to the nlu file
    try:
        with open(output_file_nlu, "a") as nlu_file:
            nlu_file.write(f"\n{nlu_section}\n")
    except Exception as e:
        print(f"Error writing to {output_file_nlu}: {e}")

    # Append the Responses section to the responses file
    try:
        with open(output_file_responses, "a") as responses_file:
            responses_file.write(f"\n{responses_section}\n")
    except Exception as e:
        print(f"Error writing to {output_file_responses}: {e}")

    print(f"Successfully appended NLU data to {output_file_nlu} and Responses data to {output_file_responses}.")

# Example input
topic = "Pinning Feature"
text = """
Pinning allows you to highlight important content in your profile or feed. 
You can pin feed comments, profile posts, creations, and showcase items.
To pin a post, navigate to it, tap and hold, then select the 'Pin' option.
To unpin, follow the same steps and choose 'Unpin.' Pinned items are marked 
with a icon and sorted by the most recent pin. You can pin up to 64 items.
"""

# Specify output files
output_file_nlu = "delete.yml"
output_file_responses = "deletethis.yml"

# Generate and append YAML
process_topic_with_gpt(topic, text, output_file_nlu, output_file_responses)