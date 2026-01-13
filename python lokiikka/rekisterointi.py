from flask import Flask, render_template

app = flask(__name__)

@app.route("/")
def index():
    return render_template(
        "../sivu/rekisteröinti.html",
        input("email")
        )


email = "email"

###tähän sitte vaan lisätään itse lähetettävä sähköposti niin että voidaan sitten viitata lähetettävään sähköpostiin email:ina

