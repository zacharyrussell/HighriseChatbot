# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import openai
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

# Set your OpenAI API key
openai.api_key = "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"
from rasa_sdk import Action
from rasa_sdk.events import UserUtteranceReverted

class ActionGPT4Response(Action):
    def name(self):
        return "action_gpt4_response"

    def run(self, dispatcher, tracker, domain):
        # Get user message and conversation history
        user_message = tracker.latest_message.get("text")
        conversation_history = self.format_conversation(tracker)

        # Prepare the system prompt for FAQ bot behavior
        system_prompt = (
            "You are a helpful assistant for Highrise. "
            "You specialize in answering FAQs to help users learn about Highrise."
            "Be concise, clear, and try your best to answer all questions."
            "If you do not have an answer to a FAQ question, prompt the user to visit the Highrise FAQ help page"
            "Do not say a feature doesnt exist, if you do not have information on a feature, refer them to the FAQ help page."
        )

        # Call GPT-4 API
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *conversation_history,  # Include formatted conversation history
                    {"role": "user", "content": user_message},
                ],
                max_tokens=200,
            )
            gpt4_response = response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            gpt4_response = "I'm having trouble generating a response right now."

        # Send GPT-4's response back to the user
        dispatcher.utter_message(text=gpt4_response)

        # Revert user utterance to prevent further processing
        return [UserUtteranceReverted()]

    def format_conversation(self, tracker):
        """
        Format the conversation history for GPT-4.
        """
        history = []
        for event in tracker.events:
            if event["event"] == "user":
                history.append({"role": "user", "content": event["text"]})
            elif event["event"] == "bot":
                history.append({"role": "assistant", "content": event["text"]})
        return history[-5:]  # Include the last 5 exchanges for brevity
    


import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

# Configure logger for helpful feedback
helpful_logger = logging.getLogger("helpful_logger")
helpful_logger.setLevel(logging.INFO)
helpful_handler = logging.FileHandler("helpful.log")
helpful_formatter = logging.Formatter("%(asctime)s - %(message)s")
helpful_handler.setFormatter(helpful_formatter)
helpful_logger.addHandler(helpful_handler)

# Configure logger for unhelpful feedback
unhelpful_logger = logging.getLogger("unhelpful_logger")
unhelpful_logger.setLevel(logging.INFO)
unhelpful_handler = logging.FileHandler("unhelpful.log")
unhelpful_formatter = logging.Formatter("%(asctime)s - %(message)s")
unhelpful_handler.setFormatter(unhelpful_formatter)
unhelpful_logger.addHandler(unhelpful_handler)

logger = logging.getLogger("interaction_logger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("interactions.log")
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

class ActionLogAndRequestFeedback(Action):
    def name(self) -> Text:
        return "action_log_and_request_feedback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Log user message and intent
        user_message = tracker.latest_message.get("text", "No user message")
        intent = tracker.latest_message.get("intent", {}).get("name", "unknown")
        bot_response = next(
            (event["text"] for event in reversed(tracker.events) if event["event"] == "bot"),
            "No response available"
        )

        # Log the interaction
        print(f"User: {user_message}, Intent: {intent}, Bot Response: {bot_response}")
        logger.info(f"User: {user_message}, Intent: {intent}, Bot Response: {bot_response}")

        # Ask for feedback
        # dispatcher.utter_message(bot_response)
        dispatcher.utter_message(
            text="Was this response helpful?",
            buttons=[
                {"title": "Yes", "payload": "/feedback_helpful"},
                {"title": "No", "payload": "/feedback_unhelpful"},
            ],
        )

        return []
    
class ActionHandleHelpfulFeedback(Action):
    def name(self) -> Text:
        return "action_handle_helpful_feedback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Get the actual user message and bot response before the feedback
        user_message = next(
            (event["text"] for event in reversed(tracker.events) if event["event"] == "user"),
            "No user message"
        )
        bot_response = next(
            (event["text"] for event in reversed(tracker.events) if event["event"] == "bot"),
            "No response available"
        )

        # Log the helpful feedback
        helpful_logger.info(
            f"User: {user_message}, Bot: {bot_response}, Feedback: Helpful"
        )
        dispatcher.utter_message("Thank you for your feedback!")
        return []

class ActionHandleUnhelpfulFeedback(Action):
    def name(self) -> Text:
        return "action_handle_unhelpful_feedback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Get the actual user message and bot response before the feedback
        user_message = next(
            (event["text"] for event in reversed(tracker.events) if event["event"] == "user"),
            "No user message"
        )
        bot_response = next(
            (event["text"] for event in reversed(tracker.events) if event["event"] == "bot"),
            "No response available"
        )

        # Log the unhelpful feedback
        unhelpful_logger.info(
            f"User: {user_message}, Bot: {bot_response}, Feedback: Unhelpful"
        )
        dispatcher.utter_message("Thank you for your feedback! I'll try to improve.")
        return []
