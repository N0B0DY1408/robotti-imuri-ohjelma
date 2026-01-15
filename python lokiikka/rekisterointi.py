import smtplib
from email.mime.text import MIMEText 
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




email="email"

#Sähköposti Vahvistus
subject = "Koodisi on: [OTP]" #
body = """<html>
  <body>
    <p>Laitetaan Sähkopostiin HTML!</p>
  </body>
</html>"""
sender="terothemis@gmail.com"
app_password = "mnxd qfjb ayqz ukxn" 
html_message = MIMEText(body, 'html')
html_message['Subject'] = subject
html_message['From'] = email
html_message['To'] = email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(sender, app_password)
    server.sendmail(email, email, html_message.as_string())
print("gg")
