from os import path
import sqlite3

# ei huolehdi virheistä, voisi olla fiksumpi
db_name = "kpedu_tira_db.sqlite" # tietokanta tiedoston nimi
main_folder = (path.dirname(path.dirname(__file__))) # ottaa aina pääkansion
tira_db = path.join(main_folder, db_name)
print(tira_db) # polu tietokantaan

tira_con = sqlite3.connect(tira_db) # yhteys tietokantaan
tira_cur = tira_con.cursor()

# import connect
# fulltable = connect.tira_cur.execute("SELECT * FROM käyttäjät")
# print(fulltable.fetchall())
