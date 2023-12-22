from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/run_script', methods=['POST'])
def run_script():
    return jsonify({'output': "success"}), 200
    

@app.route('/about')
def about():
    return 'About'