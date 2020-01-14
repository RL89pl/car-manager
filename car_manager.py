import os
import sqlite3
from sqlite3 import Error
from pick import pick
import sys
from datetime import date
import configparser

def create_table(connection):
    sql_create_car_table = """ CREATE TABLE IF NOT EXISTS car (
                                        id integer PRIMARY KEY AUTOINCREMENT UNIQUE,
                                        nazwa text NOT NULL,
                                        marka text,
                                        rocznik text
                                    ); """
 
    sql_create_stats_table = """CREATE TABLE IF NOT EXISTS stats (
                                    id integer PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    data text,
                                    godzina text,
                                    licznik_km integer,
                                    cena numeric, 
                                    ilosc_litrow integer,
                                    koszt integer,
                                    do_pelna integer,
                                    car_id integer NOT NULL,
                                    FOREIGN KEY (car_id) REFERENCES car (id)
                                );"""
    try:
        cursor = connection.cursor()
        cursor.execute(sql_create_car_table)
        cursor.execute(sql_create_stats_table)
        cursor.close()
    except Error as e:
        print(e)
    finally:
        if (connection):
            connection.close()
            

def showStats(database, car_id):
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        print(car_id)
        select_query = """SELECT * from stats WHERE car_id = {}""".format(car_id)
        cursor.execute(select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            print("Id: ", row[0])
            print("Data: ", row[1]) 
            print("Godzina: ", row[2])
            print("Licznik KM: ", row[3])
            print("Cena: ", row[4])
            print("Ilość litrów: ", row[5])
            print("Koszt: ", row[6])
            print("Do pełna: ", row[7])
            print("\n")
        cursor.close()


    except sqlite3.Error as error:
        print("Błąd odczytu danych z bazy", error)
    finally:
        if (connection):
            connection.close()

def showAuto(database):
    try:
        connection = sqlite3.connect(database)
        cursor = connection.cursor()
        select_query = """SELECT * from car"""
        cursor.execute(select_query)
        records = cursor.fetchall()
        print("Ilość rekordów:  ", len(records))
        for row in records:
            print("Id: ", row[0])
            print("Nazwa: ", row[1]) 
            print("Marka: ", row[2])
            print("Rocznik: ", row[3])
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Błąd odczytu danych z bazy", error)
    finally:
        if (connection):
            connection.close()

def addStatDatabase(database,auto = 1):
    wybor_daty = False
    wybor_do_pelna = False
    while wybor_daty == False:
        data_dzis = input("Wstawić dzisiejszą datę? T/N")
        if data_dzis == "t" or data_dzis == "T":
            data = date.today()
            wybor_daty = True
        elif data_dzis == "n" or data_dzis == "N":
            data = input("Podaj datę tankowania: ")
            wybor_daty = True
        else:
            wybor_daty = False
    godzina = input("Podaj godzinę: ")
    licznik_km = input("Podaj stan licznika kilometrów: ")
    cena = float(input("Podaj cenę: "))
    ilosc_litrow = float(input("Podaj ilość zatankowanego paliwa: "))
    while wybor_do_pelna == False:
        do_pelna = input("Czy zatankowałeś do pełna? T/N")
        if do_pelna == "t" or do_pelna == "T":
            do_pelna = 1
            wybor_do_pelna = True
        elif do_pelna == "n" or do_pelna == "N":
            do_pelna = 0
            wybor_do_pelna = True
        else:
            wybor_do_pelna = False

    print(data, godzina, licznik_km, cena, ilosc_litrow,do_pelna)
    print(type(ilosc_litrow))
    koszt = cena * ilosc_litrow
    #do_pelna = 1
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = """INSERT INTO `stats`
                            ('data', 'godzina', 'licznik_km', 'cena', 'ilosc_litrow', 'koszt', 'do_pelna', 'car_id') 
                            VALUES 
                            ('{}','{}',{},{},{},{},{},{})""".format(data, godzina, licznik_km, cena, ilosc_litrow, koszt,do_pelna, auto)

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Dodano wpis do bazy danych ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Błąd przy dodawaniu wpisu do bazy danych", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
            
def addAutoToDatabase(database):
    nazwa = input("Podaj nazwę auta: ")
    marka = input("Podaj markę auta: ")
    rocznik = input("Podaj rocznik auta: ")
    
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()

        sqlite_insert_query = """INSERT INTO `car`
                            ('nazwa', 'marka', 'rocznik') 
                            VALUES 
                            ('{}','{}',{})""".format(nazwa, marka, rocznik)

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Dodano wpis do bazy danych ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Błąd przy dodawaniu wpisu do bazy danych", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
    domyslne_auto = input("\nDodać jako auto domyślne?: ")
    if domyslne_auto == "t" or domyslne_auto == "T":
        config = configparser.ConfigParser()
        config['DEFAULT'] = {}
        config['DEFAULT']['CAR_ID'] = str(cursor.lastrowid)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

def main():
    database = "carmng.db"
    conf = "config.ini"
    config = configparser.ConfigParser()
    car_id = 1
    clear = lambda: os.system('cls')
    if not os.access(database, os.R_OK):
        #tworzy bazę danych i dwie tabele
        connection = sqlite3.connect(database)
        create_table(connection)
    if os.access(conf, os.R_OK):
        config.read(conf)
        config.sections()
        if 'DEFAULT' in config:
            car_id = int(config['DEFAULT']['CAR_ID'])
    clear()

    showStats(database, car_id)
    wybor = input("\nWciśnij 'Q', by wyjść, lub inny dowolny klawisz by przejść dalej...")
    clear()
    if wybor == "q" or wybor == "Q":
        sys.exit()
    wyjscie = False
    while wyjscie == False:

        title = 'Wybierz rodzaj: '
        options = ['Ekran główny','Dodaj wpis','Auta','Wyjście']
        option1, index = pick(options, title)
        print(index)
        if index == 0:
            showStats(database, car_id)
            wybor = input("\nWciśnij 'Q', by wyjść, lub inny dowolny klawisz by przejść dalej...")
            clear()
            if wybor == "q" or wybor == "Q":
                wyjscie = True
        elif index == 1:
            addStatDatabase(database,car_id)
            wybor = input("\nWciśnij 'Q', by wyjść, lub inny dowolny klawisz by przejść dalej...")
            clear()
            if wybor == "q" or wybor == "Q":
                wyjscie = True
        elif index == 2:
            connection = sqlite3.connect(database)
            cursor = connection.cursor()
            select_query = """SELECT * from car"""
            cursor.execute(select_query)
            records = cursor.fetchall()
            if len(records) <= 0:
                addAutoToDatabase(database)
            else:
                showAuto(database)
                dodaj_auto = input("\nDodać auto?: ")
                if dodaj_auto == "t" or dodaj_auto == "T":
                    addAutoToDatabase(database)
            wybor = input("\nWciśnij 'Q', by wyjść, lub inny dowolny klawisz by przejść dalej...")
            clear()
            if wybor == "q" or wybor == "Q":
                wyjscie = True
        elif index == 3:
            wyjscie = True

    ## po wszystkim
    try:
        if (connection):
            connection.close()
        clear()
    except:
        clear()
        


if __name__ == '__main__':
    main()