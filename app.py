from flask import Flask, render_template, request, jsonify
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
import json
import random  # Added import for random choice
from flask_cors import CORS
app = Flask(__name__)

CORS(app)
# Load intents and trained model
with open("intents.json", "r") as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE, weights_only=True)  # Updated with weights_only=True

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()



# Homepage route
@app.route("/")
def home():
    return render_template("index.html")

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message")
    if not message:
        return jsonify({"reply": "Sorry, I didn't understand that."})  # Match the key with JS code

    # Process user input
    sentence = tokenize(message)
    X = bag_of_words(sentence, all_words)
    X = torch.from_numpy(X).unsqueeze(0)

    # Model prediction
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Get the response based on the tag
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                response = random.choice(intent["responses"])
                return jsonify({"reply": response})  # Match the key with JS code

    return jsonify({"reply": "I'm sorry, I didn't understand that."})  # Match the key with JS code

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 4001))  # Allow dynamic port binding for deployment
    app.run(host="0.0.0.0", port=port)
