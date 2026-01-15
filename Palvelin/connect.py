from os import path
import sqlite3

# ei huolehdi virheistä, voisi olla fiksumpi

tira_db = path.abspath("../kpedu_tira_db.sqlite") # koko polu tietokantaan
tira_con = sqlite3.connect(tira_db) # yhteys tietokantaan
tira_cur = tira_con.cursor()

# import connect
# fulltable = connect.tira_cur.execute("SELECT * FROM käyttäjät")
# print(fulltable.fetchall())
