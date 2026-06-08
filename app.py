from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "GitOps CI/CD Working - webh00ktesting"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
