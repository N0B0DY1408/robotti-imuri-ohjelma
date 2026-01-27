#muutuja_esimerkki
import smtplib
from email.mime.text import MIMEText
import random
import string
from flask import Flask, render_template, request, redirect
from flask_session import Session
from route import connect, manage_session

app = Flask(__name__,
template_folder=connect.template_folder)

app.config["SESSION_TYPE"] = "filesystem" # Väliaikainen vaihta db jossain vaiheesa
# mahdollisesti voisi tehdä erillisen tiedoston app.configeille
# https://flask.palletsprojects.com/en/stable/config/

Session(app) # tämä on mihin tarvittiin flask_session

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    # id generator email koodeihin

@app.route("/", methods=["GET", "POST"])
def email_login():
    
    email = None

    if request.method == "POST":
        email = request.form.get("email")

        # email muuttuja on minne sähköposti lähetetään
        # pitää saada html inputista sähköposti
        print("POST tuli perille")
        print(email)

        if "@student.kpedu.fi" in email:
            verify_code = id_generator
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
        else: print("anna oikea sähköposti") and exit

    return render_template(
        "index.html",
        email=email
    )

@app.route("/logout", methods=["GET", "POST"])
def logout(): # jos menee /logout sivulle kirjaudut ulos
    manage_session.set_session()
    return redirect("/")

def login(email): # tekee tilin jos tili ei ole olemassa sitten antaa keksin
    accountcheck = connect.tira_cur.execute(f"SELECT sähköposti FROM käyttäjät WHERE sähköposti='{email}'")
    # if email not in käyttäjät sähköposti ^
    # en ole varma mutta f string tässä voi olla tietoturva riski mutta se toimii
    if accountcheck.fetchone() is None:
        data = [email]
        connect.tira_cur.execute("INSERT INTO käyttäjät(sähköposti) VALUES (?)", data)
        # jostain syystä ottaa tuplen sen sijaan kun stringin
        connect.tira_con.commit()
    manage_session.set_session(email) # sun sessio on nyt sun email

if __name__ == "__main__":
    app.run(debug=True)

"""Cookie check
if 'country' in request.cookies:
"""
# ^^^ ???
