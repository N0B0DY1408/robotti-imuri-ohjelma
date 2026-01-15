import smtplib
from email.mime.text import MIMEText 
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route("/rekisterointi", methods=["GET", "POST"])
def rekisterointi():
    email = None

    if request.method == "POST":
        email = request.form.get("email")

        print("POST tuli perille")
        print(email)


        #Sähköposti Vahvistus
        subject = "Koodisi on: [OTP]" #
        body = """<html>
        <body>
            <p>Laitetaan Sähkopostiin HTML!</p>
        </body>
        </html>"""
        sender="terothemis@gmail.com"
        app_password = "xxqe cpsw uzrv tbhw" 
        html_message = MIMEText(body, 'html')
        html_message['Subject'] = subject
        html_message['From'] = mail
        html_message['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, app_password)
            server.sendmail(mail, email, html_message.as_string())   
        print("gg")

    return render_template(
        "rekisterointi.html",
        email=email
    )

if __name__ == "__main__":
    app.run(debug=True)