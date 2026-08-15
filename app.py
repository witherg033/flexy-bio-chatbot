import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from groq import Groq
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# User Table Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Route: Homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route: AI Chatbot Endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'reply': 'No message provided'}), 400

        # Define system context for your AI
        system_instruction = (
            "You are Flexy_AI, an intelligent assistant created for the FlexyBio platform. "
            "Adem Ayech is your creator and lead developer, who works on electronics, "
            "microcontroller projects, robotics, and web application development."
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
        )

        bot_reply = chat_completion.choices[0].message.content
        return jsonify({'reply': bot_reply})

    except Exception as e:
        print(f"Error encountered: {e}")
        return jsonify({'reply': f"Backend Error: {str(e)}"}), 500

# Route: User Registration Form
@app.route('/save_user', methods=['POST'])
def save_user():
    try:
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        user = User(name=name, email=email, message=message)
        db.session.add(user)
        db.session.commit()

        return "Success!! Your data has been saved to the database.", 200

    except Exception as e:
        print(f"Database Error: {e}")
        return f"Error: Could not save data. {str(e)}", 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
