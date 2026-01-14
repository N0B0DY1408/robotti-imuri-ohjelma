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

#Sähköposti Vahvistus
subject = "Koodisi on: [OTP]" #
body = """<html>
  <body>
    <p>Laitetaan Sähkopostiin HTML!</p>
  </body>
</html>"""
sender="terothemis@gmail.com"
app_password = "" #Google App password Terolle!

def oneTimePassword():
    pass # string, random, math

def verifyEmail(): #import smtplib, from email.mime.text import MIMEText 
    pass #

