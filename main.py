from flask import Flask
from openai import OpenAI
import os

app = Flask(__name__)
openai_api_key = os.environ.get(OPENAI_API_KEY)
client = OpenAI(api_key=openai_api_key)


UID = ""

@app.route("/")
def hello_world():
    return "hello world"


@app.route('/getUsername', methods=['GET'])
def getUsername():
    return UID

@app.route('/setUsername/<username>', methods=["POST"])
def setUsername(username):
    global UID
    UID = username
    return "completed"



if __name__ == '__main__':
    app.run(debug=True)