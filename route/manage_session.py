from flask import session
from flask_session import Session
try:
    import connect
except ImportError:
    from route import connect

def isloggedin():
    """
    tämä functio tarkistaa jos käyttäjä on kirjautunut
    None tarkoittaa että ei ole
    """
    if not session.get("email"):
        return None
    return session["email"]

def set_session(user_email=None):
    """
    tämä functio asettaa käyttäjän session, sessio käyttää emailii
    jos ei pane mitään user_mail kohtaan tämä on logout juttu
    """
    session["email"] = user_email

def user_info(item=None): # kuinka mones juttu haluat
    # helppo functio joka ottaa kaikki infot käyttäjästä sqlitestä käyttämällä sessiota
    email = isloggedin()
    if email is None:
        return False
    email_as_list = [email]
    info = connect.tira_cur.execute("SELECT * FROM Users WHERE email= ?", email_as_list).fetchone()
    # palauttaa infon listana järjestyksessä missä on sqlitessä (esim user id eka)
    # tee esim user_info(2) jos haluat käyttäjänimen
    if item is not None:
        info = info[item]
    return info
