"""
tiedosto häshäys ja salasana juttuihin
kannattaa olla varma että tämä on suhteellisen
fiksu ja en tehnyt massiivisia virheitä
monien salasanoilla
"""
from hashlib import sha3_256

def häshää_salasana(salasana, salt):
    # funktio joka häshää annetun salasanan saltilla
    bytesalasana = salasana.encode("utf-8")
    häshääjä = sha3_256()
    häshääjä.update(bytesalasana)
    häshätty_string = häshääjä.hexdigest()
    return häshätty_string

def tallenna_salasana(salasana):
    """
    kun käyttäjä tekee tilin, tätä käytetään
    tee randomi salt
    pane salt ja häshätty salasana sqliteen
    """
    pass

def käytä_salasanaa(salasana, käyttäjänumero):
    """
    kun käyttäjän salasanaa käytetään
    käyttäjänumero valitsee mikä käyttäjä sqlitesta on oikee
    sen kanssa sitten ota salt ja häsh
    """
    pass

if __name__ == "__main__":
    # häshäyksen testaukseen
    häshätty_salasana = häshää_salasana("salasana", "kajnfkjwa")
    print(häshätty_salasana)
    print(type(häshätty_salasana))