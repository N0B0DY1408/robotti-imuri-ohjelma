from datetime import datetime, timezone
try:
    import connect
    import manage_session
except ImportError:
    from route import connect
    from route import manage_session

def ticket_varaus(huone, laite = "testilaite"):
    """
    varaa nykyhetkestä siihen että itse lopetat
    1. devices availability = False
    2. uusi historia entry
        laite = valittu robotti (id muodossa)
        käyttäjä = sessio email (id muodossa)
        start = nykyaika (timestamp)
        end = 0
    """

    # ottaa session emailin
    try:
        email = manage_session.isloggedin()
    except RuntimeError:
        print("ei yhteys serveriin")
        return False
        #email = "goldenbaba"

    # tässä me asetetaan devices availability = 0 ja otetaan id
    device_as_list = [laite]
    connect.tira_cur.execute("UPDATE Devices SET availability = 0 WHERE device = ?", device_as_list)
    device_id = connect.tira_cur.execute("SELECT device_id FROM Devices WHERE device= ?", device_as_list).fetchone()
    device_id = device_id[0]

    # tässä me otetaan käyttäjä id
    email_as_list = [email]
    user_id = connect.tira_cur.execute("SELECT user_id FROM Users WHERE email= ?", email_as_list).fetchone()
    user_id = user_id[0]

    # tässä me asetetaan alku aika
    right_now = datetime.now(timezone.utc).replace(microsecond=0)
    right_now_timestamp = right_now.timestamp()

    history_entry = [user_id,device_id,right_now_timestamp,0, "varaus", huone]
    connect.tira_cur.execute("INSERT INTO History VALUES(?,?,?,?,?,?)", history_entry)
    connect.tira_con.commit()

def remove_ticket_varaus(huone, laite="testilaite"):
    """ 
    poistaa tiketti varauksen
    1. devices availability = True
    2. Historia entry jossa loppu on 0 ja device id on oikea
        end = nykyaika
    """
    try:
        email = manage_session.isloggedin()
        if email is None:
            print("ei kirjautunut sisään")
            return False
    except RuntimeError:
        print("ei yhteys serveriin")
        return False
        #email = "goldenbaba"
    # tässä me asetetaan devices availability = 1 ja otetaan myös id
    device_as_list = [laite]
    connect.tira_cur.execute("UPDATE Devices SET availability = 1 WHERE device = ?", device_as_list)
    device_id = connect.tira_cur.execute("SELECT device_id FROM Devices WHERE device= ?", device_as_list).fetchone()
    device_id = device_id[0]

    # tässä me päivitetään oikeat historia kohdat nykyaikaan
    right_now = datetime.now(timezone.utc).replace(microsecond=0)
    right_now = right_now.timestamp()
    history_update = [right_now, device_id, huone]
    connect.tira_cur.execute("UPDATE History SET end = ? WHERE device_id = ? AND room = ? AND end = 0", history_update)
    connect.tira_con.commit()


if __name__ == "__main__":
    #ticket_varaus(219)
    #remove_ticket_varaus(219)
