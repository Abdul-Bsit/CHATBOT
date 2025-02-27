from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os

# Create the Flask app
app = Flask(__name__)

# Create or initialize the chatbot
english_bot = ChatBot(
    'Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch'
        },
    ],
    database_uri='sqlite:///db.sqlite3'  # Use SQLite database to store conversations
)

# Create an instance of the ListTrainer
trainer = ListTrainer(english_bot)

# Check if there are any existing saved conversations, and get the next available file number
conversation_folder = 'saved_conversations'
if not os.path.exists(conversation_folder):
    os.makedirs(conversation_folder)

# Get the next file number dynamically
existing_files = os.listdir(conversation_folder)
if existing_files:
    filenumber = int(existing_files[-1].split('.')[0]) + 1  # Get the next file number
else:
    filenumber = 1  # Start from 1 if no files exist

# Create a new conversation file and write the introduction message
file_path = os.path.join(conversation_folder, f'{filenumber}.txt')
with open(file_path, 'w+') as file:
    file.write('bot : Hi There! I am a medical chatbot. You can begin conversation by typing in a message and pressing enter.\n')

# Train the chatbot (ensure to train using a corpus or custom data)
# You can add your custom training files here
# e.g., trainer.train(['Hello', 'Hi there!', 'How can I help you?'])
# This part should be adjusted based on your data
# For now, we'll skip custom training data to avoid errors.

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    
    # Get a response from the bot
    response = str(english_bot.get_response(userText))

    # Log the conversation to the appropriate file
    with open(file_path, "a") as appendfile:
        appendfile.write(f'user : {userText}\n')
        appendfile.write(f'bot : {response}\n')

    return response

if __name__ == "__main__":
    app.run(debug=True)
