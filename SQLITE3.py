import sqlite3
import time

conn = sqlite3.connect('MUD.db')
c = conn.cursor()
cursor = conn.execute('SELECT * from Gear')
#c.execute('''CREATE TABLE ID (Name, Password)''')
#c.execute('''CREATE TABLE Placement (Name, Room)''')
#c.execute('''CREATE TABLE Character (Name, Level, Exp, Exptnl, Strength, Constitution, Dexterity, Agility, Wisdom, Intellegence)''')
#c.execute('''CREATE TABLE Vitals (Name, Health, MaxHealth, HealthRegen, Mana, MaxMana, ManaRegen)''')
#c.execute('''CREATE TABLE Equipment (Name, Mainhand, Offhand, Helmet, Body, Lowerbody, Boots)''')
#c.execute('''CREATE TABLE Rooms (ID, Description, North, East, South, West)''')
#c.execute('''CREATE TABLE Monsters (Name, Strength, Constitution, Dexterity, Agility, Wisdom, Intellegence)''')
#c.execute('''CREATE TABLE Gear (ID, Name, Slot, MinValue, MaxValue, Attackspeed)''')
#t = (1, 'Rusty Sword', 'Main', 1, 6, 3.0)
#t = (2, 'Rusty Shield', 'Shield', 4, 4, 0.0)
#t = (3, 'Rusty Dagger', 'Main', 1, 4, 2.0)
#t = (4, 'Rusty Dirk', 'Weapon', 1, 3, 2.0)
#t = (5, 'Rusty Mace', 'Main', 1, 5, 2.5)
#t = (6, 'Knobbed Staff', 'Main', 1, 6, 3.0)
#t = (7, 'Chain Shirt', 'Body', 4, 4, 0)
#t = (8, 'Chain Pants', 'Lowerbody', 3, 3, 0)
#t = (9, 'Leather Shirt', 'Body', 3, 3, 0)
#t = (10, 'Leather Pants', 'Lowerbody', 2, 2, 0)
#t = (11, 'Cloth Shirt', 'Body', 2, 2, 0)
#t = (12, 'Cloth Pants', 'Lowerbody', 1, 1, 0)
#c.execute('''DELETE FROM Gear WHERE ID = 1''')
#c.execute('''INSERT INTO Gear VALUES (?,?,?,?,?,?)''', t)
#c.execute('''UPDATE Gear SET Slot='Weapon' WHERE ID=4''')
names = list(map(lambda x: x[0], cursor.description))
print names
for row in c.execute('Select * from Gear order by ID'):
    print row

raw_input()
conn.commit()
conn.close()