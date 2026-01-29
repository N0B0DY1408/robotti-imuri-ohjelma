from datetime import datetime, timezone, timedelta

try:
    import connect
except ImportError:
    from route import connect
# kiitos tyyppi stack overflowissa

def add_code():
    pass

def use_code(code):
    """
    tämä koodi poistaa vanhentuneet koodit, tarkistaa jos sinun
    koodi on dbssä, ja sitten antaa False jos ei ole ja sinun
    emailin jos koodi on oikein, poistaa myös oikeat koodit kun käytetty
    mahdottoman pienessä mahdollisuudessa että on kaksi käyttäjää
    jolla on sama koodi samaan aikaan sinä kirjaudut ensimmäisenä
    käyttää utc aikoja ja formatoi unix aikaan
    """
    right_now = datetime.now(timezone.utc).replace(microsecond=0)
    right_now = right_now.timestamp()
    right_now_as_list = [right_now] # en vieläkään tiedä miksi tämän pitää olla list lol
    # poistaa vanhat
    connect.tira_cur.execute("DELETE FROM email_koodit WHERE loppumisaika < ?", right_now_as_list)
    connect.tira_con.commit()

    code_as_list = [code]
    email_of_code = connect.tira_cur.execute("SELECT email FROM email_koodit WHERE koodi = ?", code_as_list).fetchone()
    if email_of_code is None:
        return False
    else:
        emailstring = (email_of_code[0])
        # poistaa käytetyn koodin
        connect.tira_cur.execute("DELETE FROM email_koodit WHERE email = ?", email_of_code)
        connect.tira_con.commit()
        return emailstring


if __name__ == "__main__":
    pass
    #baba = use_code(654321)
    #if baba:
    #    print(baba)
    #else:
    #    print("väärin")