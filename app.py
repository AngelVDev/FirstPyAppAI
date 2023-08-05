from flask import Flask, render_template, request, jsonify
import requests, cohere, os

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY')

co = cohere.Client(API_KEY)

chat_history = []

@app.route("/")
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/post_message', methods=['POST'])
def post_message():
    prompt = request.form.get('prompt')

    if prompt:
        response = co.generate(  
            model='command-nightly',  
            prompt=prompt,  
            max_tokens=200,  
            temperature=0.750)
        intro_paragraph = response.generations[0].text
        chat_history.append({'prompt': prompt, 'response': intro_paragraph})
        return jsonify({'status': 'success', 'prompt': 'Successful prompt'})
    else:
        return jsonify({'status': 'error', 'prompt': 'Prompt required'})

@app.route('/get_chat_history', methods=['GET'])
def get_chat_history():
    return jsonify(chat_history)

if __name__ == '__main__':
    app.run(debug=True)
