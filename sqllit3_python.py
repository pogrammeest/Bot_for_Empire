import sqlite3

con = sqlite3.connect('sql.db')
curs = con.cursor()

curs.execute("DROP TABLE IF EXISTS humans")
curs.execute("create table humans(id integer PRIMARY KEY autoincrement, name varchar(255));")

con.commit()

entities = 'Misha'
for i in entities:
    curs.execute(f"INSERT INTO humans(name) values('{entities}')")



def sql_fetch(con):

    curs = con.cursor()

    curs.execute('SELECT * FROM humans')

    rows = curs.fetchall()

    for row in rows:

        print(row)

sql_fetch(con)
