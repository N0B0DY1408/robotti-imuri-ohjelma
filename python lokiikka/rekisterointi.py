from flask import Flask, render_template, request

app = flask(__name__)

@app.route("/rekisteröinti", methods=["GET", "POST"])
def rekisteröinti():
    email = none

    if request.method == "POST":
        email = request.form.get("email")

    return render_template(
        "rekisterointi.html",
        email=email
    )

if __name__ == "__main__":
    app.run(debug=True)


print(email)


email = "email"

###tähän sitte vaan lisätään itse lähetettävä sähköposti niin että voidaan sitten viitata lähetettävään sähköpostiin email:ina

