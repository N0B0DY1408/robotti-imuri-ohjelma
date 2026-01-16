# tiedosto häshäys ja salasana juttuihin
# kannattaa olla varma että tämä on suhteellisen
# fiksu ja en tehnyt massiivisia virheitä
# monien salasanoilla

import connect # connect.py
import bcrypt

# minulle on ilmoitettu että tämä tiedosto on mahdollisesti turha yippii!

def save_password(password):
    # käytetty kun käyttäjä tekee tilin
    bytepassword = password.encode("utf-8")
    user_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytepassword, user_salt)
    return user_salt, hashed_password
    # salt, häsh = tallenna_salasana("salasana")

def use_password(password, username):
    # käytetty kun käyttäjä menee tiliin
    bytepassword = password.encode("utf-8")
    saved_hash = "placeholder"
    saved_salt = "placeholder"
    new_hash = bcrypt.hashpw(bytepassword, saved_salt)
    return (new_hash == saved_hash) # jos on oikea salasana tulee True
    # ei vielä valmis
