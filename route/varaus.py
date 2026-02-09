from datetime import datetime, timezone, timedelta, date
try:
    import connect
except ImportError:
    from route import connect

def pvm_aika_pituus_format(pvm, aika, pituus):
    """
    formatoi datetime.strptimen avulla pvm, aika, ja pituus
    utc formatoituihin alku ja loppu aikoihin
    """
    uus_alku = datetime.strptime(f"{pvm};{aika}", "%Y-%m-%d;%H:%M").astimezone(timezone.utc)
    pituus = timedelta(hours=pituus)
    uus_lop = (uus_alku + pituus)
    return uus_alku, uus_lop


def varaus_check(laite, pvm, aika, pituus): # ottaa local aikana pvm, aika, ja pituus loppuun
    # tarkistaa että ei varaa muitten aikojen päälle

    if pituus > 10:
        return "Liian pitkä"
    # jos varaus kestää >10h ei pysty, koska kuka käyttää robottia 11 tuntia :clueless:
    # ok mutta joo kommentoi pois tai pane vaihtoehto tai vaihda max pituutta jos pitää

    uus_alku, uus_lop = pvm_aika_pituus_format(pvm, aika, pituus)

    uus_alku2 = uus_alku.timestamp()
    uus_lop2 = uus_lop.timestamp()

    device_as_list = [laite]
    device_id = connect.tira_cur.execute("SELECT device_id FROM Devices WHERE device = ?", device_as_list).fetchone()
    db_times = connect.tira_cur.execute("SELECT start, end FROM History WHERE device_id = ?", device_id).fetchall()
    # ^^^ ottaa laitteen nimen, vaihtaa sen laitteen id, sitten ottaa sillä tärkeät ajat
    for vara_alku, vara_lop in db_times:
        # jos vanhan varauksen loppu on uuden aloituksen jälkeen
        # mutta uuden loppu on ennen vanhaan varauksen aloitusta
        if vara_lop > uus_alku2 and  uus_lop2 > vara_alku:
            return "Varaisi päälle"

    # jos varaus toimii palauttaa True jos ei toimi palauttaa stringin joka selittää
    # pitää muualla panna sqliteen ja mitälie
    return True

if __name__ == "__main__":
    baba = varaus_check("testilaite", "2026-02-12", "12:30", 4.3)
    print(baba)
