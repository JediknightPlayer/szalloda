from abc import ABC, abstractmethod
from datetime import datetime

class Szoba(ABC):
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam

    @abstractmethod
    def ar_szamolas(self):
        pass

    @abstractmethod
    def tipus(self):
        pass

class EgyagyasSzoba(Szoba):
    def ar_szamolas(self):
        return self.ar
    
    def tipus(self):
        return "egyágyas"

class KetagyasSzoba(Szoba):
    def ar_szamolas(self):
        return self.ar * 1.5
    
    def tipus(self):
        return "kétágyas"

class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum

class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def add_szoba(self, szoba):
        self.szobak.append(szoba)

    def add_foglalas(self, foglalas):
        self.foglalasok.append(foglalas)

    def foglalas_ar(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                return szoba.ar_szamolas()  
        return None

    def lemondas(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return True
        return False

    def listaz_foglalasok(self):
        if not self.foglalasok:
            print("Nincs foglalás.")
        for foglalas in self.foglalasok:
            print(f"Szoba száma: {foglalas.szoba.szobaszam}, Dátum: {foglalas.datum}")

# Szálloda, szobák és foglalások létrehozása
szalloda = Szalloda("Szállide Szálloda")

szoba1 = EgyagyasSzoba(50, "101")
szoba2 = EgyagyasSzoba(60, "102")
szoba3 = KetagyasSzoba(100, "201")

szalloda.add_szoba(szoba1)
szalloda.add_szoba(szoba2)
szalloda.add_szoba(szoba3)

foglalas1 = Foglalas(szoba1, datetime(2024, 5, 10))
foglalas2 = Foglalas(szoba2, datetime(2024, 5, 12))
foglalas3 = Foglalas(szoba3, datetime(2024, 5, 15))
foglalas4 = Foglalas(szoba1, datetime(2024, 5, 20)) 
foglalas5 = Foglalas(szoba3, datetime(2024, 5, 25))  

szalloda.add_foglalas(foglalas1)
szalloda.add_foglalas(foglalas2)
szalloda.add_foglalas(foglalas3)
szalloda.add_foglalas(foglalas4)
szalloda.add_foglalas(foglalas5)

# Felhasználói interfész
while True:
    print("\n1 - Foglalás\n2 - Lemondás\n3 - Foglalások listázása\n4 - Kilépés")
    valasztas = input("Válassz egy műveletet: ")

    if valasztas == "1":
        datum_input = input("Add meg a foglalás dátumát (év-hónap-nap formátumban): ")
        datum = datetime.strptime(datum_input, "%Y-%m-%d")

        if datum < datetime.now():
            print("Hibás dátum! Csak jövőbeli dátum foglalható.")
            continue

        elerheto_szobak = []
        for szoba in szalloda.szobak:
            foglalt = False
            for foglalas in szalloda.foglalasok:
                if foglalas.szoba.szobaszam == szoba.szobaszam and foglalas.datum == datum:
                    foglalt = True
                    break
            if not foglalt:
                elerheto_szobak.append(szoba)

        if not elerheto_szobak:
            print("Sajnálom, de nincs szabad szoba az adott időpontban.")
        else:
            print("Elérhető szobák az adott időpontban:")
            for szoba in elerheto_szobak:
                print(f"Szobaszám: {szoba.szobaszam}, Ár: {szoba.ar_szamolas()}, Típus: {szoba.tipus()}")

            szobaszam = input("Válassz egy szobát és add meg a szoba számát: ")
            szoba = None
            for s in szalloda.szobak:
                if s.szobaszam == szobaszam:
                    szoba = s
                    break

            szalloda.add_foglalas(Foglalas(szoba, datum))
            print("Sikeresen foglaltál!")     
   
    elif valasztas == "2":
        szobaszam = input("Add meg a szoba számát: ")
        datum_input = input("Add meg a lemondás dátumát (év-hónap-nap formátumban): ")
        datum = datetime.strptime(datum_input, "%Y-%m-%d")

        if szalloda.lemondas(szobaszam, datum):
            print("A foglalás sikeresen le lett mondva.")
        else:
            print("Hibás szobaszám vagy dátum! Kérlek, ellenőrizd az adatokat.")

    elif valasztas == "3":
        szalloda.listaz_foglalasok()

    elif valasztas == "4":
        break
    
    else:
        print("Érvénytelen választás! Kérlek, válassz az elérhető műveletek közül.")

