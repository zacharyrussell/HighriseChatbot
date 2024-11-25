import openai
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

# Set your OpenAI API key
openai.api_key = "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"

class ActionGPT4Response(Action):
    def name(self):
        return "action_gpt4_response"

    def run(self, dispatcher, tracker, domain):
        # Get the user message
        user_message = tracker.latest_message.get("text")

        # Call GPT-4 API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Specify GPT-4 model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150
            )
            gpt4_response = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            gpt4_response = "I'm having trouble generating a response right now."

        # Send GPT-4's response back to the user
        dispatcher.utter_message(text=gpt4_response)

        return []