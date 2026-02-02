from os import path
import sqlite3

# ei huolehdi virheistä, voisi olla fiksumpi
main_folder = (path.dirname(path.dirname(__file__))) # ottaa aina pääkansion
tira_db = path.join(main_folder, "kpedu_tira_db.sqlite") # tira db tiedosto
template_folder = path.join(main_folder, "templates") # templates kansio

tira_con = sqlite3.connect(tira_db, check_same_thread=False) # yhteys tietokantaan
tira_cur = tira_con.cursor()

# import connect
# fulltable = connect.tira_cur.execute("SELECT * FROM käyttäjät")
# print(fulltable.fetchall())
