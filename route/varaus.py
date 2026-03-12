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

def remove_ticket_varaus(laite="testilaite"):
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
    history_update = [right_now, device_id]
    connect.tira_cur.execute("UPDATE History SET end = ? WHERE device_id = ? AND end = 0", history_update)
    connect.tira_con.commit()

def varaus_history_info():
    # ottaa kaikki infot jota tarvitsetaan historia taulukkoon sivulla
    # käyttäjä, aika varauksesta, pvm, huone
    info = connect.tira_cur.execute("SELECT * FROM History").fetchall()
    formatted_history = []
    # lista johon pannaan oikein formatoitu historia
    right_now = datetime.now().replace(microsecond=0)
    for entry in info:
        # entry on tuple yhdestä varauksesta, infon järjestys on sama kun sqlitessä
        # esim user id on entry[0] ja start on entry[2]
        name = connect.tira_cur.execute("SELECT name FROM Users WHERE user_id = ?", [entry[0]]).fetchone()
        # käyttäjän nimi
        pvm = datetime.fromtimestamp(entry[2])
        time_since = str(right_now - pvm)
        # ylhällä otetaan päivämäärä ja aika siitä varauksesta
        formatted_history.append((name[0],time_since,str(pvm),entry[5]))
    return formatted_history


def varaus_info(item=None): # kuinka mones juttu haluat
    # ottaa viime varauksesta infoa
    info = connect.tira_cur.execute("SELECT * FROM History WHERE end = 0").fetchone()
    if info is None:
        return False
    if item is not None:
        info = info[item]
    return info
    # palauttaa infon listana järjestyksessä missä on sqlitessä (esim user id eka)
    # tee esim varaus_info(5) jos haluat huoneen

def varaus_name():
    user_id = [varaus_info(0)]
    username = connect.tira_cur.execute("SELECT name FROM Users WHERE user_id= ?", user_id).fetchone()
    return(username[0])

if __name__ == "__main__":
    #ticket_varaus(220)
    #remove_ticket_varaus()
    #print(varaus_info())
    #print(varaus_name())
    print(varaus_history_info())