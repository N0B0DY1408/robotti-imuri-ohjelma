import smtplib
from email.mime.text import MIMEText 
from flask import Flask, render_template, request
from os import path

app = Flask(__name__,
template_folder="../templates")

@app.route("/", methods=["GET", "POST"])
def rekisterointi():
    email = None

    if request.method == "POST":
        email = request.form.get("email")

        # receiver muuttuja on minne sähköposti lähetetään
        # pitää saada html inputista sähköposti
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
        html_message['From'] = sender
        html_message['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, app_password)
            server.sendmail(sender, email, html_message.as_string())   
        print("gg")

    return render_template(
        "login-register.html",
        email=email
    )

if __name__ == "__main__":
    app.run(debug=True)
