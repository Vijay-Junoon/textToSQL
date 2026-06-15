import os
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from src.main import ask_prompt,performQuery,formatResponse


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")

# Placeholder for LLM logic
def get_ai_response(user_input, history):

    userQuery_response = ask_prompt(userQuery=user_input)[6:-3]
    query_result = performQuery(userQuery_response)
    response = formatResponse(userQuery_response,query_result)
    return response

@app.route('/')
def index():
    session['history'] = []
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message"}), 400
    
    # Update History
    history = session.get('history', [])
    history.append({"role": "user", "content": user_message})
    
    # Get Response
    response = get_ai_response(str(user_message), history)
    
    history.append({"role": "bot", "content": response})
    session['history'] = history
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)