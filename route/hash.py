# tiedosto häshäys ja salasana juttuihin
# kannattaa olla varma että tämä on suhteellisen
# fiksu ja en tehnyt massiivisia virheitä
# monien salasanoilla

import connect # connect.py
import bcrypt

def save_password(password):
    # käytetty kun käyttäjä tekee tilin
    bytepassword = password.encode("utf-8")
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytepassword, user_salt)
    return user_salt, hashed_password
    # salt, häsh = tallenna_salasana("salasana")

def use_password(password, username): # username on vaan että tietää mikä tili on
    # käytetty kun käyttäjä menee tiliin
    bytepassword = password.encode("utf-8")
    saved_salt, saved_hash = connect.tira_cur.execute(f"""
        SELECT salasana_salt, salasana_hash FROM käyttäjät WHERE käyttäjänimi='{username}'
    """).fetchone()

    byte_salt = saved_salt.encode("utf-8")
    new_hash = bcrypt.hashpw(bytepassword, byte_salt)
    string_new_hash = new_hash.decode("utf-8")
    # bcrypt hashpw tekee byte häshin, se pitää muuttaa stringiksi jotta voi tallentaa tietokantaan
    return (saved_hash == string_new_hash) # jos on oikea salasana tulee True

#    testvalue = use_password("pingas", "rordon gamsay")
#    print(testvalue)
