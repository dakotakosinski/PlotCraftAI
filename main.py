from flask import Flask


app = Flask(__name__)

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