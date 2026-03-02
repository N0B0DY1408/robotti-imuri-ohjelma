#muutuja_esimerkki
import datetime
import smtplib
import ssl
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
import random
import string
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from route import connect, manage_session, login_logic

context = ssl.create_default_context()

load_dotenv("salaisetjutut/email.env")

ehost = os.getenv("emailhost")
eport = int(os.getenv("emailport"))
euser = os.getenv("emailuser")
epassword = os.getenv("emailpassword")

print("HOST:", ehost)
print("PORT:", eport)
print("USER:", euser)
print("PASS:", epassword)

app = Flask(__name__,
template_folder=connect.template_folder)

app.config["SESSION_TYPE"] = "filesystem" # Väliaikainen vaihta db jossain vaiheesa
# mahdollisesti voisi tehdä erillisen tiedoston app.configeille
# https://flask.palletsprojects.com/en/stable/config/

Session(app) # tämä on mihin tarvittiin flask_session

def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    # id generator email koodeihin


@app.route("/", methods=["GET", "POST"])
def email_login():
    
    email = None

    if request.method == "POST":
        email = request.json.get("email")

        # email muuttuja on minne sähköposti lähetetään
        # pitää saada html inputista sähköposti
        print("POST tuli perille")
        print(email)
        status = "sent"

        if not email or "@student.kpedu.fi" not in email:
            return jsonify({"success": False, "message": "Syötä kpedu-sähköposti"})
        else:
            code = id_generator()
            session["verify_code"] = code
            session["email"] = email
            #Sähköposti Vahvistus
            subject = f"Koodisi on: [{code}]"
            body = f"""<html>
            <body>
                <p>"Koodisi on: [{code}]" </p>
            </body>
            </html>"""
            sender = euser
            app_paswword = epassword
            html_message = MIMEText(body, 'html')
            html_message['Subject'] = subject
            html_message['From'] = sender
            html_message['To'] = email
            try:
                with smtplib.SMTP(ehost, eport) as server:
                    server.starttls(context=context)
                    server.login(euser, epassword)
                    server.sendmail(sender, email, html_message.as_string())
                print("Email sent")
            except Exception as e:
                import traceback
                traceback.print_exc()
                return jsonify({"success": False, "message": "Sähköpostin lähetys epäonnistui"})

        return jsonify({"status": "sent", "success": True})
        


    return render_template(
        "index.html",
        email=email
    )

@app.route("/verify", methods=["POST"])
def verify():
    user_code = request.json.get("code")
    real_code = session.get("verify_code")

    print("User code:", user_code)
    print("Real code:", real_code)

    if not real_code:
        return jsonify({"success": False, "message": "Sessio vanhentunut"})

    if user_code == real_code:
        login(user_code)
        session.pop("verify_code", None)  # poista käytetty koodi
        return jsonify({"success": True})

    return jsonify({"success": False, "message": "Väärä koodi"})


@app.route("/logincheck", methods=["GET", "POST"])
def logincheck():
    # debug sivu ennen kun missään muualla on tätä infoo
    baba = manage_session.isloggedin()
    return f"<p>{baba}</p>"

@app.route("/logout", methods=["GET", "POST"])
def logout(): # jos menee /logout sivulle kirjaudut ulos
    manage_session.set_session()
    return redirect("/")

@app.route("/help", methods=["GET", "POST"])
def timer_thing():
    time_since = connect.tira_cur.execute("SELECT start FROM History WHERE device_id = 1 AND end = 0").fetchone()
    if time_since is None:
        return render_template(
            "help.html",
            time_since="vapaa"
        )
    time_since = time_since[0]
    time_since = datetime.datetime.fromtimestamp(int(time_since))
    print(time_since)
    return render_template(
        "help.html",
        time_since=time_since
    )

@app.route("/varaus", methods=["GET", "POST"])
def reserve_page():
    # sivu vuoron varaukseen

    #user = manage_session.isloggedin()
    #if not user: # jos et ole kirjautunut et voi olla sivulla
    #    return redirect("/")
    # ^tarkistaa jos on kirjautunut
    # kommentoitu testauksen takia
    robots1 = connect.tira_cur.execute("SELECT device FROM devices").fetchall()
    # robots2 on vaan kunnolla formatoitu
    robots2 = connect.r_sqlite_of(robots1)

    if request.method == "POST":
        robotit = request.form.get("robotit")
        the_date = request.form.get("the_date")
        the_time = request.form.get("the_time")
        length = request.form.get("length")
        print(robotit,the_date,the_time,length)
        # pitää tehdä tarkistuksia ja sitten tallentaa sqlite historiaan
        # aiotaan näyttää sqlitest tärkee historia sivulla
    return render_template(
        "varaus.html", robots=robots2
    )

def login(code): # tekee tilin jos tili ei ole olemassa sitten antaa keksin
    email = login_logic.use_code(code)
    if email:
        email_as_list = [email]
        accountcheck = connect.tira_cur.execute("SELECT email FROM Users WHERE email= ?", email_as_list)
        # ^ jos tällä scriptillä on joku omituinen virhe tämä on varmaan syy
        if accountcheck.fetchone() is None:
            connect.tira_cur.execute("INSERT INTO Users(email) VALUES (?)", email_as_list)
            # jostain syystä ottaa tuplen sen sijaan kun stringin
            connect.tira_con.commit()
        manage_session.set_session(email) # sun sessio on nyt sun email

if __name__ == "__main__":
    app.run(debug=True)

"""Cookie check
if 'country' in request.cookies:
"""
# ^^^ ???
