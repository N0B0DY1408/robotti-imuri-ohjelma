#muutuja_esimerkki
import smtplib
from email.mime.text import MIMEText
import random
import string
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from route import connect, manage_session, login_logic


app = Flask(__name__,
template_folder=connect.template_folder)

app.config["SESSION_TYPE"] = "filesystem" # Väliaikainen vaihta db jossain vaiheesa
# mahdollisesti voisi tehdä erillisen tiedoston app.configeille
# https://flask.palletsprojects.com/en/stable/config/

app.secret_key = "super-secret-key-change-this"

Session(app) # tämä on mihin tarvittiin flask_session

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    # id generator email koodeihin

verify_code = id_generator()

@app.route("/", methods=["GET", "POST"])
def email_login():
    
    email = None

    if request.method == "POST":
        email = request.json.get("email")

        # email muuttuja on minne sähköposti lähetetään
        # pitää saada html inputista sähköposti
        print("POST tuli perille")
        print(email)

        if not email or "@student.kpedu.fi" not in email:
            return jsonify({"status": "error", "message": "Syötä kpedu-sähköposti"})
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

            

        return jsonify({"status": "sent"})

    return render_template(
        "index.html",
        email=email
    )

@app.route("/verify", methods=["POST"])
def verify():
    user_code = request.json.get("code")

    if user_code == session.get("verify_code"):
        login(user_code)
        return {"status": "ok"}

    return {"status": "error"}


@app.route("/logincheck", methods=["GET", "POST"])
def logincheck():
    # debug sivu ennen kun missään muualla on tätä infoo
    baba = manage_session.isloggedin()
    return f"<p>{baba}</p>"

@app.route("/logout", methods=["GET", "POST"])
def logout(): # jos menee /logout sivulle kirjaudut ulos
    manage_session.set_session()
    return redirect("/")

@app.route("/lol", methods=["GET", "POST"])
def code_login():
    # debug sivu joka koittaa login tällä koodilla
    login("80085")
    return redirect ("/logincheck")

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
