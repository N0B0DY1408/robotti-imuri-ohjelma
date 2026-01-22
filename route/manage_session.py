from flask import Flask, redirect, request, session
from flask_session import Session
import connect

app = Flask(__name__)

app.config["SESSION_TYPE"] = "filesystem"     # Väliaikainen vaihta db jossain vaiheesa
Session(app)

Session(app)

@app.route("/")
def index():
    if not session.get("name"):
        return "<p>need to login</p>"
    return f"<p>logged in as {session["name"]}</p>"

@app.route("/login", methods=["GET", "POST"])
def login():
    session["name"] = "testName"
    return redirect("/")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
