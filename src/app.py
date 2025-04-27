from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask Application working"

@app.route('/hello')
def hello():
    return "Hello from Flask on GKE!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
