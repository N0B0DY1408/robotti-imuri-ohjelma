#muutuja_esimerkki
import smtplib
from email.mime.text import MIMEText 
import secrets
import string
from flask import Flask, render_template, request

app = Flask(__name__,
template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def email_login():
    
    email = None

    if request.method == "POST":
        email = request.form.get("email")

        # email muuttuja on minne sähköposti lähetetään
        # pitää saada html inputista sähköposti
        print("POST tuli perille")
        print(email)
        verify_code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
        #Sähköposti Vahvistus
        subject = f"Koodisi on: [{verify_code}]" 
        body = f"""<html>
        <body>
            <p>"Koodisi on: [{verify_code}]" </p>
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
        print("Email send")

    return render_template(
        "login-register.html",
        email=email
    )

if __name__ == "__main__":
    app.run(debug=True)

"""Cookie check
if 'country' in request.cookies:
"""