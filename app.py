import datetime
import smtplib
import ssl
import os
from email.mime.text import MIMEText
import random
import string
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, jsonify
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

def email_to_name(user_email):
    name_part = user_email.split("@")[0]
    name_part = name_part.replace(".", " ")
    name_part = name_part.title()
    return name_part

app.config["SESSION_TYPE"] = "filesystem" # Väliaikainen vaihta db jossain vaiheesa
# mahdollisesti voisi tehdä erillisen tiedoston app.configeille
# https://flask.palletsprojects.com/en/stable/config/

Session(app) # tämä on mihin tarvittiin flask_session

def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    # id generator email koodeihin

@app.route("/apua")
def helpsite():
    return render_template("help.html")


@app.route("/", methods=["GET", "POST"])
def email_login():
    room_display, time_since, favroom = reserve_page_info()
    varaus_name = varaus.varaus_name()
    varaus_room = varaus.varaus_info(5)
    viime_varaus = {
        "name": varaus_name,
        "room": varaus_room
    }
    history = varaus.varaus_history_info()
    # otetaan huone valikko ja aika viime varauksesta

    if request.method == "POST":

        user_email = request.json.get("email")
        if not user_email or "@student.kpedu.fi" not in user_email:
            return jsonify({"success": False, "message": "Syötä kpedu-sähköposti"})
            # palauttaa script.js että ei toiminut ja näyttää viestin


        code = id_generator()
        login_logic.add_code(user_email, code)

        # lisää käyttäjä jos ei ole
        accountcheck = connect.tira_cur.execute(
            "SELECT email FROM Users WHERE email = ?", 
            [user_email]
        )

        if accountcheck.fetchone() is None:

            name = email_to_name(user_email)

            connect.tira_cur.execute(
                "INSERT INTO Users(email, name) VALUES (?, ?)", 
                [user_email, name]
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
        html_message['To'] = user_email
        
        try:
            with smtplib.SMTP(ehost, eport) as server:
                server.starttls(context=context)
                server.login(euser, epassword)
                server.sendmail(euser, user_email, html_message.as_string())
        except:
            return jsonify({"success": False, "message": "Sähköpostin lähettämisellä oli meidän puolella ongelma"})
            # palauttaa script.js että ei toiminut ja näyttää viestin
        
        return jsonify({"success": True})
        # palauttaa script.js infon että python tiedosto on valmis
    # -------- GET --------

    users = connect.tira_cur.execute(
        "SELECT email FROM Users"
    ).fetchall()

    users = connect.r_sqlite_of(users)

    user = manage_session.user_info(2)
    # tarkistaa jos on kirjautunut jotta voi piilottaa juttuja

    return render_template(
        "index.html",
        users=users,
        room_display=room_display,
        time_since=time_since,
        viime_varaus=viime_varaus,
        history=history,
        user=user,
        favroom=favroom
    )

@app.route("/send_code", methods=["POST"])
def send_code():

    user_email = request.json.get("email")
    number = request.json.get("number")

    if not user_email:
        return jsonify({"success": False, "message": "Email puuttuu"})

    if not number:
        return jsonify({"success": False, "message": "Huone puuttuu"})

    accountcheck = connect.tira_cur.execute(
        "SELECT email FROM Users WHERE email = ?",
        [user_email]
    )

    name = email_to_name(user_email)

    connect.tira_cur.execute(
        "INSERT INTO Users(email, name) VALUES (?, ?)", 
        [user_email, name]
    )
    connect.tira_con.commit()

    # lähetä koodi
    code = id_generator()
    login_logic.add_code(user_email, code)

    return jsonify({"success": True})

@app.route("/verify", methods=["POST"])
def verify():
    # huomioi että käyttäjä voi mennä manuaalisesti tälle sivulle mutta tulee vaan "method not allowed"
    user_code = request.json.get("code")
    # ottaa js code submit kohdasta code constin

    if not user_code:
        return jsonify({"success": False, "message": "Koodi puuttuu"})
        # palauttaa script.js että ei toiminut ja näyttää viestin
        # ei normaalisti näy koska kohta johon koodi pannaan on required


    user_email = login_logic.use_code(user_code)
    # tarkistaa jos koodi on dbssä ja ei vanheentunut

    if not user_email:
        return jsonify({"success": False, "message": "Väärä tai vanhentunut koodi"})
        # palauttaa script.js että ei toiminut ja näyttää viestin

    login(user_email)
    return jsonify({"success": True})

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
    
    favroom = manage_session.user_info(5)
    room_numbers = connect.tira_cur.execute("SELECT number FROM Rooms").fetchall()
    rooms_numbers = connect.r_sqlite_of(room_numbers)
    # yllä me otetaan huone infoa sqlitestä ja vähän formatoidaan

    # alhalla me tehdään kaikki listat ja dictit ja intit jota tarvitaan seuraavaan kohtaan
    if favroom:
        entry = 1
    else:
        entry = 0
    room_list = []
    lower_room_list = []
    room_dict = {}
    favroom_dict = {}
    # tämä koodipätkä formatoi huoneet oikein 4 pituiseen html pöytään
    # ja oikein formatoi jos on lempihuone käyttäjällä
    for num in rooms_numbers:
        # entry päättää million seuraava tr alkaa html sisällä
        nam = connect.tira_cur.execute("SELECT name FROM Rooms WHERE number =(?)",[num]).fetchone()
        nam = nam[0]
        if num == favroom:
            favroom_dict.update({"num": num})
            if nam is not None:
                favroom_dict.update({"nam": nam})
        else:
            entry += 1
            room_dict.update({"num": num})

            if nam is not None:
                room_dict.update({"nam": nam})
            lower_room_list.append(room_dict.copy())
            room_dict.clear()
            if entry % 4 == 0: # i <3 modulo
                room_list.append(lower_room_list.copy())
                lower_room_list.clear()
            # me tehdään lista jossa on 4 pituisia listoja dictejä
    if entry % 4 != 0:
        room_list.append(lower_room_list.copy())
        lower_room_list.clear()
    return room_list, time_since, favroom_dict

def login(user_email): # functio joka aktivoituu kun kirjautuu, asettaa käyttäjälle session
    manage_session.set_session(user_email)

@app.route("/room_thing", methods=["POST"])
def room_thing():
    user_email = manage_session.isloggedin()
    if user_email is None:
        return jsonify({"success": False, "message": "Et ole kirjautunut sisään"})

    new_room_num = request.json.get("num")

    new_fav = request.json.get("new_fav")
    room_success = add_room(new_room_num)
    if new_fav:
        favroom_selector(new_room_num)
    
    # viesti käyttäjälle
    if room_success and new_fav:
        return jsonify({"success": True, "message": "Uusi huone tehty ja asetettu oletukseksi"})
    if room_success and not new_fav:
        return jsonify({"success": True, "message": "Uusi huone tehty"})
    if new_fav:
        return jsonify({"success": True, "message": "Huone olemassa, asetettu oletukseksi"})
    if not new_fav:
        return jsonify({"success": False, "message": "Huone jo olemassa"})



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
        user_email = manage_session.isloggedin()
        if user_email is None:
            print("ei kirjautunut sisään")
            return False
    except RuntimeError:
        print("ei yhteys serveriin")
        return False
    # ^ ottaa käyttäjän emailin sessiosta
    favroom_update = [room_number, user_email]
    connect.tira_cur.execute("UPDATE Users SET favroom = ? WHERE email = ?", favroom_update)
    connect.tira_con.commit()
    # ^ asettaa käyttäjän lempihuoneen sqlitessä
    return True

@app.route("/reserve", methods=["POST"])
def reserve():
    user_email = manage_session.isloggedin()

    if user_email is None:
        return jsonify({"success": False, "message": "Kirjaudu ensin"})

    room = request.json.get("room")

    if not room:
        return jsonify({"success": False, "message": "Huone puuttuu"})
    varaus.remove_ticket_varaus()
    varaus.ticket_varaus(room)


    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
