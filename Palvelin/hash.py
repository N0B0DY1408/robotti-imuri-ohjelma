"""
tiedosto häshäys ja salasana juttuihin
kannattaa olla varma että tämä on suhteellisen
fiksu ja en tehnyt massiivisia virheitä
monien salasanoilla
"""
import connect # connect.py
import bcrypt


def tallenna_salasana(salasana):
    # käytetty kun käyttäjä tekee tilin
    bytesalasana = salasana.encode("utf-8")
    käyttäjän_salt = bcrypt.gensalt()
    häshätty_salasana = bcrypt.hashpw(bytesalasana, käyttäjän_salt)
    return käyttäjän_salt, häshätty_salasana
    # salt, häsh = tallenna_salasana("salasana")

def käytä_salasanaa(salasana, käyttäjänimi):
    # käytetty kun käyttäjä menee tiliin
    bytesalasana = salasana.encode("utf-8")
    tallennettu_hash = "placeholder"
    tallennettu_salt = "placeholder"
    häshätty_salasana = bcrypt.hashpw(bytesalasana, tallennettu_salt)
    return (häshätty_salasana == tallennettu_hash) # jos on oikea salasana tulee True
    # ei vielä valmis

if __name__ == "__main__":
    # häshäyksen testaukseen
    tallennettava_salt, tallennettava_häsh = tallenna_salasana("slasana")
    print(tallennettava_salt, "salt")
    print(tallennettava_häsh, "häsh")
