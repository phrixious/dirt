import sqlite3
conn = sqlite3.connect('MUD.db')
c = conn.cursor()
for row in c.execute('''SELECT * from ActiveMonster ORDER BY RandomID'''):
    print row

raw_input("End")