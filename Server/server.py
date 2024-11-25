from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__, template_folder='templates')

# URL of your locally running Rasa bot
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route("/", methods=["GET"])
def home():
    # Serve the index.html file
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint to interact with the Rasa bot.
    Expects JSON input: {"message": "user's message"}
    """
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Send the message to the Rasa bot
    try:
        response = requests.post(
            RASA_SERVER_URL,
            json={"sender": "user", "message": user_message},
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    # Return Rasa's response
    bot_responses = response.json()
    messages = [resp.get("text") for resp in bot_responses if "text" in resp]
    return jsonify({"responses": messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
