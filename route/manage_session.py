from flask import session
from flask_session import Session

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
