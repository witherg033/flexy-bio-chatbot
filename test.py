import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from groq import Groq
from flask_sqlalchemy import SQLAlchemy
# Load environment variables from .env
load_dotenv()

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)
app = Flask(__name__, static_folder=".", static_url_path="")

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    message  =  db.Column(db.String(100), nullable = False)

with app.app_context():
    db.create_all()

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Bonjour!",
        }
    ],
    model="llama-3.3-70b-versatile",
)

# Print the response back
print(chat_completion.choices[0].message.content)
