import sqlite3

conn = sqlite3.connect('MUD.db')
c = conn.cursor()
c.execute('''CREATE TABLE ID (Name, Password, Permission, ChatInstance)''')
c.execute('''CREATE TABLE Placement (Name, Room)''')
c.execute('''CREATE TABLE Character (Name, Class, Subclass, Level, Exp, Exptnl, Strength, Constitution, Dexterity, Agility, Wisdom, Intellegence)''')
c.execute('''CREATE TABLE Inventory (Name, SLOT1, SLOT2, SLOT3, SLOT4, SLOT5, SLOT6, SLOT7, SLOT8, SLOT9, SLOT10, SLOT11, SLOT12, SLOT13, SLOT14, SLOT15, SLOT16, SLOT17, SLOT18, SLOT19, SLOT20, Gold)''')
c.execute('''CREATE TABLE Equipment (Name, Mainhand, Offhand, Helmet, Body, Lowerbody, Boots)''')
c.execute('''CREATE TABLE Vitals (Name, Health, Mana)''')
c.execute('''CREATE TABLE Regions (Name, Mobcount)''')
c.execute('''CREATE TABLE RoomExits (ID, Description, North, East, South, West)''')
c.execute('''CREATE TABLE RoomMobs (ID, Slot1, Slot2, Slot3, Slot4, Slot5, Slot6, Slot7, Slot8, Slot9, Slot10)''')
c.execute('''CREATE TABLE RoomItems (ID, Slot1, Slot2, Slot3, Slot4, Slot5, Slot6, Slot7, Slot8, Slot9, Slot10, Slot11, Slot12, Slot13, Slot14, Slot15, Slot16, Slot17, Slot18, Slot19, Slot20)''')
c.execute('''CREATE TABLE RoomPlayers (ID, Slot1, Slot2, Slot3, Slot4, Slot5, Slot6, Slot7, Slot8, Slot9, Slot10, Slot11, Slot12, Slot13, Slot14, Slot15, Slot16, Slot17, Slot18, Slot19, Slot20)''')
c.execute('''CREATE TABLE Monsters (ID, Name, Level, Strength, Constitution, Dexterity, Agility, Wisdom, Intellegence)''')
c.execute('''CREATE TABLE MonsterAttacks (ID, Attack1, Min1, Max1, Attack2, Min2, Max2, Attack3, Min3, Max3, Attack4, Min4, Max4)''')
c.execute('''CREATE TABLE MonsterLoot (ID, Goldmin, Goldmax, Item1, Item2, Item3, Item4, Item5, Item6, Item7)''')
c.execute('''CREATE TABLE ActiveMonster (RandomID, MobID, Level, Name, Health, MaxHealth, Mana, MaxMana, Attack, Defence, Speed, Critical, Accuracy, Dodge, Mattack, Mdefence, Room)''')
c.execute('''CREATE TABLE MonsterThreat (RandomID, Player1, Threat1, Player2, Threat2, Player3, Threat3)''')
c.execute('''CREATE TABLE Gear (ID, Name, Slot, MinValue, MaxValue, Attackspeed)''')
cursor = conn.execute('SELECT * from Gear')
equipment = [(1, 'Rusty Sword', 'Main', 1, 6, 3.0),
             (2, 'Rusty Shield', 'Shield', 4, 4, 0.0),
             (3, 'Rusty Dagger', 'Main', 1, 4, 2.0),
             (4, 'Rusty Dirk', 'Weapon', 1, 3, 2.0),
             (5, 'Rusty Mace', 'Main', 1, 5, 2.5),
             (6, 'Knobbed Staff', 'Main', 1, 6, 3.0),
             (7, 'Chain Shirt', 'Body', 4, 4, 0),
             (8, 'Chain Pants', 'Lowerbody', 3, 3, 0),
             (9, 'Leather Shirt', 'Body', 3, 3, 0),
             (10, 'Leather Pants', 'Lowerbody', 2, 2, 0),
             (11, 'Cloth Shirt', 'Body', 2, 2, 0),
             (12, 'Cloth Pants', 'Lowerbody', 1, 1, 0)
            ]

#admin = [('Admin', 'Admin', 'Admin'),
#         ('Server', 'Password', 'Admin')
#        ]

regions = [('NoobieForest', 0)
    ]

# ID, Description, N, E, S, W
rooms = [(0, 'This is spawn. You are safe here, and can rest around here. You see a forest to the south that looks like a good place to start adventuring.', None, None, 1, None),
         (1, 'You are at the entrance of a small forest.', 0, 3, 6, 2),
         (2, 'You see a deadening tree, with moss on it.', None, 1, 5, None),
         (3, 'The forest is quiet and creepy.', None, None, 7, 1),
         (4, 'A small spring is making a gentle noise.', None, 5, None, None),
         (5, 'You spot a small spring to the west, but something makes you unconfortable.', 2, 6, 9, 4),
         (6, 'You are at the center of the small forest. You could probably rest here.', 1, 7, 10, 5),
         (7, 'Some green moss nearby is rotting, and the corpse of a deer lies to the east.', 3, 8, 11, 6),
         (8, 'A corpse of a deer is laying in the middle of a small clearing touching a creek. It looks like it was killed recently as blood flows through the creek to the south...', None, None, None, 7),
         (9, 'You feel like someone or something is watching you...', 5, 10, None, None),
         (10, 'A babbling brook leads southward. It is tinted red with blood.', 6, 11, 12, 9),
         (11, 'A small creek flows South/Southwest, It seems tainted with blood', 7, None, None, 10),
         (12, 'The edge of the small forest. A Large Gate with a sign blocks your path... "NO ADVENTURES THIS WAY"', 10, None, None, None)
    ]

# ID, Slot1, Slot2, Slot3, Slot4, Slot5
roommobs = [(0, '', '', '', '', '', '', '', '', '', ''),
            (1, '', '', '', '', '', '', '', '', '', ''),
            (2, '', '', '', '', '', '', '', '', '', ''),
            (3, '', '', '', '', '', '', '', '', '', ''),
            (4, '', '', '', '', '', '', '', '', '', ''),
            (5, '', '', '', '', '', '', '', '', '', ''),
            (6, '', '', '', '', '', '', '', '', '', ''),
            (7, '', '', '', '', '', '', '', '', '', ''),
            (8, '', '', '', '', '', '', '', '', '', ''),
            (9, '', '', '', '', '', '', '', '', '', ''),
            (10, '', '', '', '', '', '', '', '', '', ''),
            (11, '', '', '', '', '', '', '', '', '', ''),
            (12, '', '', '', '', '', '', '', '', '', ''),
            ]
roomplayers = [(0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (1, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (2, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (3, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (4, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (5, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (6, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (7, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (8, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (9, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (10, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (11, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (12, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            ]

roomitems = [(0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (1, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (2, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (3, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (4, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (5, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (6, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (7, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (8, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (9, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (10, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (11, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            (12, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''),
            ]

# ID, Attack1, Min1, Max1, Attack2, Min2, Max2, Attack3, Min3, Max3, Attack4, Min4, Max4
mobattacks = [(1, 'Morningstar', 1, 8, 'Javelin', 1, 6, '', 0, 0, '', 0, 0),
              (2, 'Shortsword', 1, 6, 'Light Crossbow', 1, 8, '', 0, 0, '', 0, 0),
              (3, 'Half Spear', 1, 6, 'Light Crossbow', 1, 8, '', 0, 0, '', 0, 0),
              (4, 'Great Axe', 4, 15, 'Javelin', 3, 9, '', 0, 0, '', 0, 0)
              ]

spawnmob = [(1, 'Goblin', 0.50, 8, 11, 13, 12, 11, 10),
            (2, 'Gnome', 0.50, 8, 12, 10, 11, 11, 11),
            (3, 'Kobold', 0.40, 6, 11, 13, 14, 10, 10),
            (4, 'Orc', 0.75, 15, 11, 10, 9, 8, 9),
            (5, 'Choker', 2, 16, 13, 10, 10, 13, 4),
            (6, 'Dark Mantle', 1, 16, 13, 10, 10, 10, 2,),     # Water Creature
            (7, 'Small Rat', 0.35, 10, 12, 17, 17, 12, 1),
            (8, 'Weasel', 2, 14, 10, 19, 17, 12, 2),
            (9, 'Badger', 2, 14, 19, 17, 17, 12, 2),
            (10, 'Large Bat', 2, 17, 17, 22, 20, 14, 2),
            (11, 'Ape', 3, 22, 14, 15, 14, 12, 2),
            (12, 'Wolverine', 4, 22, 19, 17, 19, 12, 2),
            (13, 'Abyssal Creature', 4, 18, 16, 15, 14, 12, 5),
            (14, 'Wolf', 3, 25, 17, 15, 16, 12, 2),
            (15, 'Boar', 4, 27, 17, 10, 12, 13, 2),
            (16, 'Lion', 5, 25, 17, 15, 15, 12, 2),
            (17, 'Doppelganger', 3, 12, 12, 13, 16, 14, 13),    # Shadow, likes swamps
            (18, 'Dryad', 1, 10, 11, 15, 15, 15, 14),
            (19, 'Dwarf', 0.50, 11, 13, 10, 10, 10, 10),
            (20, 'Elf', 0.50, 10, 8, 13, 12, 11, 11),
            (21, 'Etheral Filcher', 3, 10, 11, 18, 17, 12, 7)
        ]

#c.execute('''DELETE FROM Gear WHERE ID = 1''')
#c.executemany('''INSERT INTO ID VALUES (?,?,?)''', admin)
#print "Admin, and Server Accounts Made"
c.executemany('''INSERT INTO Gear VALUES (?,?,?,?,?,?)''', equipment)
print "Gear Created"
c.executemany('''INSERT INTO Monsters VALUES (?,?,?,?,?,?,?,?,?)''', spawnmob)
c.executemany('''INSERT INTO MonsterAttacks VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', mobattacks)
print "Monsters Entered"
c.executemany('''INSERT INTO RoomExits VALUES (?,?,?,?,?,?)''', rooms)
c.executemany('''INSERT INTO RoomMobs VALUES (?,?,?,?,?,?,?,?,?,?,?)''', roommobs)
c.executemany('''INSERT INTO RoomPlayers VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', roomplayers)
c.executemany('''INSERT INTO RoomItems VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', roomitems)
print "Rooms 0-12 Made"
c.executemany('''INSERT INTO Regions VALUES (?,?)''', regions)
print "1 Region made"

#for row in c.execute('''SELECT * from Monsters ORDER BY ID'''):
#    print row
#c.execute('''UPDATE Gear SET Slot='Weapon' WHERE ID=4''')

print ""
print ""
print "Hit Enter to complete"
raw_input()
conn.commit()
conn.close()