#muutuja_esimerkki
import code
import datetime
import email
import smtplib
import ssl
from dotenv import load_dotenv
import re
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
            login_logic.add_code(email, code)
            #Sähköposti Vahvistus
            subject = f"Koodisi on: [{code}]"
            body = f"""
            <html>
            <body>
            <div style="width: 200px;">
            <p>kpedu robotti varaus</p>
            <p>automaattinen koodi kirjautua palveluun</p>
            <p>koodisi on</p>
            <div style="background-color: rgb(234, 234, 234); border-radius: 10px; width: 90px;">
            <p style="text-align: center;">[{code}]</p>
            </div>
            </div>
            </body>
            </html>
            """
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

    if not user_code:
        return jsonify({"success": False, "message": "Koodi puuttuu"})

    email = login_logic.use_code(user_code)

    if not email:
        return jsonify({"success": False, "message": "Väärä tai vanhentunut koodi"})

    login(email)
    return jsonify({"success": True})
    


@app.route("/logincheck", methods=["GET", "POST"])
def logincheck():
    # debug sivu ennen kun missään muualla on tätä infoo
    baba = manage_session.user_info()
    return f"<p>{baba}</p>"

@app.route("/logout", methods=["GET", "POST"])
def logout(): # jos menee /logout sivulle kirjaudut ulos
    manage_session.set_session()
    return redirect("/")

@app.route("/varaus", methods=["GET", "POST"])
def reserve_page():
    time_since = connect.tira_cur.execute("SELECT start FROM History WHERE device_id = 1 AND end = 0").fetchone()
    if time_since is None:
        time_since = "vapaa"
    else:
        time_since = time_since[0]
        time_since = datetime.datetime.fromtimestamp(int(time_since))
    # yllä me otetaan tietokannasta viime varauksen alun

    room_numbers = connect.tira_cur.execute("SELECT number FROM Rooms").fetchall()
    room_names = connect.tira_cur.execute("SELECT name FROM Rooms").fetchall()
    rooms_numbers = connect.r_sqlite_of(room_numbers)
    room_names = connect.r_sqlite_of(room_names)
    # yllä me otetaan huone infoa sqlitestä ja vähän formatoidaan

    room_display = []
    for num, nam in zip(room_numbers, room_names):
        if nam is None:
            room_display.append(num[0])
        else:
            room_display.append(str(num[0]) + " " + nam)
    # lisää huone info formatointia

    if request.method == "POST":
        #jotain = request.form.get("jotain")
        pass
        # jotta voi saada infoo sivulta
    return render_template(
        "varaus.html", room_display=room_display, time_since=time_since
    ) # pannaan tarvittu info sivulle ja ladataan se

def login(email): #tämä kohta nyt tarkistaa tietokannan onko email jo siellä ja jos ei niin lisää sen
    email_as_list = [email]

    accountcheck = connect.tira_cur.execute(
        "SELECT email FROM Users WHERE email = ?", 
        email_as_list
    )

    if accountcheck.fetchone() is None:
        connect.tira_cur.execute(
            "INSERT INTO Users(email) VALUES (?)", 
            email_as_list
        )
        connect.tira_con.commit()

    manage_session.set_session(email)

def favroom_selector(room_number):
    # tämä skripti käytetään jotta voi asettaa jonkun hunoeen käyttäjän oletushuoneeksi
    # pane room_number kohtaan huoneen numero esim 218
    # palauttaa False jos ei toiminut, palauttaa True jos toimi
    try:
        email = manage_session.isloggedin()
        if email is None:
            print("ei kirjautunut sisään")
            return False
    except RuntimeError:
        print("ei yhteys serveriin")
        return False
    # ^ ottaa käyttäjän emailin sessiosta
    favroom_update = [room_number, email]
    connect.tira_cur.execute("UPDATE Users SET favroom = ? WHERE email = ?", favroom_update)
    connect.tira_con.commit()
    # ^ asettaa käyttäjän lempihuoneen sqlitessä
    return True

if __name__ == "__main__":
    app.run(debug=True)

"""Cookie check
if 'country' in request.cookies:
"""
# ^^^ ???
