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
from route import connect, manage_session, login_logic, varaus

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
    room_display, time_since = reserve_page_info()
    varaus_name = varaus.varaus_name()
    varaus_room = varaus.varaus_info(5)
    history = varaus.varaus_history_info()
    # otetaan huone valikko ja aika viime varauksesta

    if request.method == "POST":

        email = request.json.get("email")

        if not email or "@student.kpedu.fi" not in email:
            return jsonify({"success": False, "message": "Syötä kpedu-sähköposti"})

        email_as_list = [email]

        code = id_generator()
        login_logic.add_code(email, code)

        # lisää käyttäjä jos ei ole
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

        # email lähetys
        subject = f"Koodisi on: [{code}]"
        body = f"""
        <html>
        <body>
        <p>Koodisi on:</p>
        <b>[{code}]</b>
        </body>
        </html>
        """

        html_message = MIMEText(body, 'html')
        html_message['Subject'] = subject
        html_message['From'] = euser
        html_message['To'] = email

        try:
            with smtplib.SMTP(ehost, eport) as server:
                server.starttls(context=context)
                server.login(euser, epassword)
                server.sendmail(euser, email, html_message.as_string())
        except:
            return jsonify({"success": False})

        return jsonify({"success": True})

    # -------- GET --------

    users = connect.tira_cur.execute(
        "SELECT email FROM Users"
    ).fetchall()

    users = connect.r_sqlite_of(users)

    return render_template(
        "index.html",
        users=users,
        room_display=room_display,
        time_since=time_since,
        varaus_name=varaus_name,
        varaus_room=varaus_room,
        history = history
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

def reserve_page_info():
    # ottaa vähän infoa pääsivun varausnappiin
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
    for num, nam in zip(rooms_numbers, room_names):
        if nam is None:
            room_display.append(num)
        else:
            room_display.append(str(num) + " " + nam)

    return room_display, time_since

def login(email): #tämä kohta nyt tarkistaa tietokannan onko email jo siellä ja jos ei niin lisää sen
    email_as_list = [email]

    manage_session.set_session(email)

def add_room(room_number, room_name=None):
    # funktio joka tekee huoneen jos se ei ole olemassa
    existing_room = connect.tira_cur.execute("SELECT number FROM Rooms WHERE number = ?", [room_number]).fetchone()
    if existing_room is not None:
        return False
    # jos huone jota pannaan on olemassa palauttaa False
    if room_name is None:
        connect.tira_cur.execute(
        "INSERT INTO Rooms(number) VALUES (?)", 
        [room_number]
        )
    else:
        connect.tira_cur.execute(
        "INSERT INTO Rooms VALUES (?,?)",
        [room_number, room_name]
        )
    # tallentaa huone numeron, jos annoit nimen se tallennetaan myös
    connect.tira_con.commit()
    return True

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


