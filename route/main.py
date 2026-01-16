from flask import Flask

message = "<p>Horse world!</p>"

app = Flask(__name__)

@app.route("/")
def hello_world():
    return message
