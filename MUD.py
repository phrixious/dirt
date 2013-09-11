from twisted.internet.protocol import Factory, Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.internet import task
import random
import sqlite3
import string

global c
global __name__
conn = sqlite3.connect('MUD.db')
c = conn.cursor()


class Chat(LineReceiver):

    def __init__(self, users):
        self.type = "Player"
        self.users = users
        self.name = ''
        self.password = ''
        self.spawn = True
        self.restready = True
        self.pkswitch = True
        self.pk = False
        self.pkilled = 0
        self.room = 0
        self.lastroom = self.room
        self.placement = 20
        self.classname = ''
        self.subclass = ''
        self.level = 0
        self.exp = 0
        self.exptnl = 0
        self.health = 0
        self.maxhealth = 0
        self.healthregen = 0
        self.mana = 0
        self.maxmana = 0
        self.manaregen = 0
        self.mainhand = ''
        self.mainhandid = 0
        self.mainhandvalmin = 0
        self.mainhandvalmax = 0
        self.mainhandspeed = 0
        self.offhand = ''
        self.offhandspeed = 0
        self.offhandid = 0
        self.offhandtype = ''
        self.offhandvalmin = 0
        self.offhandvalmax = 0
        self.helmet = ''
        self.helmetid = 0
        self.helmetvalue = 0
        self.body = ''
        self.bodyid = 0
        self.bodyvalue = 0
        self.lowerbody = ''
        self.lowerbodyid = 0
        self.lowerbodyvalue = 0
        self.boots = ''
        self.bootsid = None
        self.bootsvalue = 0
        self.strength = 0
        self.constitution = 0
        self.dexterity = 0
        self.agility = 0
        self.intellegence = 0
        self.wisdom = 0
        self.state = ''
        self.whisper = ""
        self.attack = 0
        self.defence = 0
        self.mattack = 0
        self.mdefence = 0
        self.dodge = 0
        self.accuracy = 0
        self.critical = 0
        self.speedmod = 0
        self.strengthdamage = 0
        self.attackspeed = 0
        self.attackready = True
        self.skillpoints = 0
        self.suicide = True
        # This is where players will access each others info through this party dictionary
        self.party = []
        self.partybool = False
        self.permission = 'Member'        # Member, Moderator, Admin, Server
        ### INVENTORY
        self.gold = 0
        self.slot1 = ''
        self.slot2 = ''
        self.slot3 = ''
        self.slot4 = ''
        self.slot5 = ''
        self.slot6 = ''
        self.slot7 = ''
        self.slot8 = ''
        self.slot9 = ''
        self.slot10 = ''
        self.slot11 = ''
        self.slot12 = ''
        self.slot13 = ''
        self.slot14 = ''
        self.slot15 = ''
        self.slot16 = ''
        self.slot17 = ''
        self.slot18 = ''
        self.slot19 = ''
        self.slot20 = ''

    def connectionMade(self):
        self.sendLine("Username :")
        self.state = "LOGINCHECK"

    def connectionLost(self, leave):
        self.SAVE()
        global c
        room = self.room
        roomc = (room,)
        c.execute('''SELECT * FROM RoomPlayers WHERE ID=?''', roomc)
        test = c.fetchone()
        count = 1
        while count <= 20:
            if test[count] not in('', None, 'None'):
                count = count + 1
            else:
                lastroom = self.lastroom
                column = "'Slot" + str(self.placement) + "'"
                c.execute("UPDATE RoomPlayers SET " + column + "=? WHERE ID=?", ('', lastroom))
                conn.commit()
                count = 30
        conn.commit()
        c.execute('''SELECT * FROM RoomPlayers WHERE ID=?''', roomc)
        test = c.fetchone()
        if self.users.has_key(self.name):
            message = "%s has disconnected" % (self.name)
            del self.users[self.name]
            print (message)
            for name, protocol in self.users.iteritems():
                protocol.sendLine(message)

# LOAD / SAVE SCRIPTS
    def LOAD(self):
        global c
        t = str(self.name)
        t = (t,)
        c.execute('SELECT * FROM Placement WHERE Name=?', t)
        test = c.fetchone()
        if(test == None):
            print self.name, "has no room placing in spawn..."
            self.room = 0
            self.lastroom = 0
            room = self.room
            roomc = (room,)
            c.execute('''SELECT * FROM RoomPlayers WHERE ID=?''', roomc)
            test = c.fetchone()
            count = 1
            while count <= 20:
                if test[count] not in('', None, 'None'):
                    count = count + 1
                else:
                    column = "'Slot" + str(count) + "'"
                    c.execute("UPDATE RoomPlayers SET " + column + "=? WHERE ID=?", (self.name, room))
                    self.lastroom = room
                    self.placement = count
                    self.room = room
                    conn.commit()
                    count = 30
            conn.commit()
            c.execute('''SELECT * FROM RoomPlayers WHERE ID=?''', roomc)
            test = c.fetchone()
        if(test != None):
            self.room = test[1]
            self.lastroom = self.room
            room = self.room
            roomc = (room,)
            c.execute('''SELECT * FROM RoomPlayers WHERE ID=?''', roomc)
            test = c.fetchone()
            count = 1
            while count <= 20:
                if test[count] not in('', None, 'None'):
                    count = count + 1
                else:
                    column = "'Slot" + str(count) + "'"
                    c.execute("UPDATE RoomPlayers SET " + column + "=? WHERE ID=?", (self.name, room))
                    self.lastroom = room
                    self.placement = count
                    self.room = room
                    conn.commit()
                    count = 30
            conn.commit()
            c.execute('''SELECT * FROM RoomPlayers WHERE ID=?''', roomc)
            test = c.fetchone()
        c.execute('SELECT * FROM Character WHERE Name=?', t)
        test = c.fetchone()
        if(test == None):
            print self.name, "has no stats, So no character? Placing in creation sequence..."
            self.handle_CLEARSCREEN
            self.sendLine("***WARNING*** Do not leave during this process! it won't take long!")
            self.CLASSLIST()
            self.state = "PSTART"
            return
        if(test != None):
            #Name, Class, Subclass Level, Exp, Exptnl, Strength, Constitution, Dexterity, Agility, Wisdom, Intellegence
            self.classname = str(test[1])
            self.subclass = str(test[2])
            if self.subclass == None:
                self.subclass = ''
            self.level = test[3]
            self.exp = test[4]
            self.exptnl = test[5]
            self.strength = test[6]
            self.constitution = test[7]
            self.dexterity = test[8]
            self.agility = test[9]
            self.wisdom = test[10]
            self.intellegence = test[11]
            self.StatCreation()
            c.execute('SELECT * FROM Vitals WHERE Name=?', t)
            test = c.fetchone()
            if(test == None):
                print self.name, "has no vitals saved, setting to max vitals"
                self.health = self.maxhealth
                self.mana = self.maxmana
            if(test != None):
                self.health = test[1]
                self.mana = test[2]
                print self.name, "is loaded and logged in at", self.room
                self.sendLine("Character Successfully Loaded")
                c.execute('SELECT * FROM Equipment WHERE Name=?', t)
                test = c.fetchone()
                if(test == None):
                    print self.name, "has no equipment!"
                if(test != None):
                    self.mainhandid = test[1]
                    self.offhandid = test[2]
                    self.helmetid = test[3]
                    self.bodyid = test[4]
                    self.lowerbodyid = test[5]
                    self.bootsid = test[6]
                    self.EQUIPSTART()
                    c.execute('SELECT * FROM Inventory WHERE Name=?', t)
                    test = c.fetchone()
                    if(test == None):
                        print self.name, "has no inventory!"
                    if(test != None):
                        self.slot1 = str(test[1])
                        self.slot2 = str(test[2])
                        self.slot3 = str(test[3])
                        self.slot4 = str(test[4])
                        self.slot5 = str(test[5])
                        self.slot6 = str(test[6])
                        self.slot7 = str(test[7])
                        self.slot8 = str(test[8])
                        self.slot9 = str(test[9])
                        self.slot10 = str(test[10])
                        self.slot11 = str(test[11])
                        self.slot12 = str(test[12])
                        self.slot13 = str(test[13])
                        self.slot14 = str(test[14])
                        self.slot15 = str(test[15])
                        self.slot16 = str(test[16])
                        self.slot17 = str(test[17])
                        self.slot18 = str(test[18])
                        self.slot19 = str(test[19])
                        self.slot20 = str(test[20])
                        self.gold = test[21]
                self.party = [self.name]
                member = self
                member = str(self)
                name = unicode(self.name)
                c.execute('''UPDATE ID SET ChatInstance=? WHERE Name=?'''(member, self.name))
                conn.commit()
                c.execute('''SELECT * FROM ID WHERE Name=?'''(self.name))
                fetch = c.fetchone()
                print fetch
                self.handle_WELCOME()

                # Name, Mainhand, Offhand, Helmet, Body, Lowerbody, Boots

    def SAVE(self):
        global c
        global conn
        r = self.room
        t = self.name
        t = (r, t,)
#        try:
        c.execute('UPDATE Placement SET Room=? WHERE Name=?', t)
        l = self.classname
        m = self.subclass
        b = self.level
        cc = self.exp
        d = self.exptnl
        e = self.strength
        f = self.constitution
        g = self.dexterity
        h = self.agility
        i = self.wisdom
        j = self.intellegence
        k = self.name
        a = (l, m, b, cc, d, e, f, g, h, i, j, k,)
        # try:
        c.execute('UPDATE Character SET Class=?, Subclass=?, Level=?, Exp=?, Exptnl=?, Strength=?, Constitution=?, Dexterity=?, Agility=?, Wisdom=?, Intellegence=? WHERE Name=?', a)
        b = self.mainhandid
        cc = self.offhandid
        d = self.helmetid
        e = self.bodyid
        f = self.lowerbodyid
        g = self.bootsid
        h = self.name
        a = (b, cc, d, e, f, g, h,)
        # try:
        c.execute('UPDATE Equipment SET Mainhand=?, Offhand=?, Helmet=?, Body=?, Lowerbody=?, Boots=? WHERE Name=?', a)
        b = self.health
        cc = self.mana
        d = self.name
        a = (b, cc, d,)
        # try:
        c.execute('UPDATE Vitals SET Health=?, Mana=? WHERE Name=?', a)
        b = self.slot1
        cc = self.slot2
        d = self.slot3
        e = self.slot4
        f = self.slot5
        g = self.slot6
        h = self.slot7
        i = self.slot8
        j = self.slot9
        k = self.slot10
        l = self.slot11
        m = self.slot12
        n = self.slot13
        o = self.slot14
        p = self.slot15
        q = self.slot16
        r = self.slot17
        s = self.slot18
        t = self.slot19
        u = self.slot20
        v = self.gold
        w = self.name
        a = (b, cc, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w)
        c.execute('UPDATE Inventory SET SLOT1=?, SLOT2=?, SLOT3=?, SLOT4=?, SLOT5=?, SLOT6=?, SLOT7=?, SLOT8=?, SLOT9=?, SLOT10=?, SLOT11=?, SLOT12=?, SLOT13=?, SLOT14=?, SLOT15=?, SLOT16=?, SLOT17=?, SLOT18=?, SLOT19=?, SLOT20=?, Gold=? WHERE Name=?', a)
        self.sendLine('Save Successful!')
        conn.commit()

    def FIRSTSAVE(self):
        global c
        global conn
        r = self.room
        t = self.name
        t = (t, r,)
#        try:
        c.execute('''INSERT INTO Placement VALUES (?,?)''', t)
        l = self.classname
        m = self.subclass
        b = self.level
        cc = self.exp
        d = self.exptnl
        e = self.strength
        f = self.constitution
        g = self.dexterity
        h = self.agility
        i = self.wisdom
        j = self.intellegence
        k = self.name
        a = (k, l, m, b, cc, d, e, f, g, h, i, j,)
        # try:
        c.execute('INSERT INTO Character VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', a)
        b = self.mainhandid
        cc = self.offhandid
        d = self.helmetid
        e = self.bodyid
        f = self.lowerbodyid
        g = self.bootsid
        h = self.name
        a = (h, b, cc, d, e, f, g,)
        # try:
        c.execute('INSERT INTO Equipment VALUES (?,?,?,?,?,?,?)', a)
        b = self.slot1
        cc = self.slot2
        d = self.slot3
        e = self.slot4
        f = self.slot5
        g = self.slot6
        h = self.slot7
        i = self.slot8
        j = self.slot9
        k = self.slot10
        l = self.slot11
        m = self.slot12
        n = self.slot13
        o = self.slot14
        p = self.slot15
        q = self.slot16
        r = self.slot17
        s = self.slot18
        t = self.slot19
        u = self.slot20
        v = self.gold
        w = self.name
        a = (w, b, cc, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v)
        c.execute('INSERT INTO Inventory VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', a)
        b = self.health
        cc = self.mana
        d = self.name
        a = (d, b, cc,)
        # try:
        c.execute('INSERT INTO Vitals VALUES (?,?,?)', a)
        self.sendLine('Creation Successful!')
        conn.commit()

    def lineReceived(self, line):
        if self.state == "CHANGEPASS":
            self.CHANGE_PASSWORD1(line)
            return
        if self.state == "CHANGEPASS2":
            self.CHANGE_PASSWORD2(line)
            return
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
            return
        if self.state == "CHAT":
            self.handle_CHAT(line)
            return
        if self.state == "ATTACK":
            self.handle_ATTACK(line)
            return
        if self.state == "SAY":
            self.handle_SAY(line)
            return
        if self.state == "WHISP":
            self.handle_WHISP_ini(line)
            return
        if self.state == "WHISPER":
            self.handle_WHISPER(line)
            return
        if self.state == "LOGINCHECK":
            self.handle_LOGINCHECK(line)
            return
        if self.state == "CREATE":
            self.handle_CREATE(line)
            return
        if self.state == "NCREATE":
            self.handle_NCREATE(line)
            return
        if self.state == "NCHECK":
            self.handle_NCHECK(line)
            return
        if self.state == "PASSWORD":
            self.handle_PASSWORD(line)
            return
        if self.state == "CPASSWORD":
            self.handle_CPASSWORD(line)
        if self.state == "LOGINPASS":
            self.handle_LOGINPASS(line)
            return
        if self.state == "CHECKPASS":
            self.handle_CHECKPASS(line)
            return
        if self.state == "DOUBLECHECK":
            self.handle_DOUBLECHECK(line)
            return
        if(self.state == "PSTART"):
            self.handle_PSTART(line)
            return
        if(self.state == "INFO"):
            self.handle_INFO(line)
            return
        if(self.state == "AddPoints"):
            self.AdditionalPoints(line)
            return
        if(self.state == "CCCHECK"):
            self.CCCHECK(line)
            return

#CREATION SEQUENCE

    def handle_NCREATE(self, name):
        global c
        na = name
        t = str(name)
        n = t
        t = (t,)
        c.execute('SELECT * FROM ID WHERE Name=?', t)
        name = c.fetchone()
        if(name == None):
            self.name = na
            self.sendLine("%s is available" % (n))
            self.sendLine("Is %s correct? (Y/N)" % (n))
            self.state = "NCHECK"

    def handle_DOUBLECHECK(self, answer):
        if answer in('yes', 'y', 'Yes', 'Y'):
            self.sendLine("Creating Account!")
            self.users[self.name] = self
            self.permission = 'Member'
            print "Created User  :", self.name
            print "With Password : **********"
            chat = str(self)
            ID = (self.name, self.password, self.permission, chat)
            c.execute('INSERT INTO ID Values (?,?,?,?)', ID)
            #c.commit()                                     #dont forget to include this!
            self.handle_CLEARSCREEN
            self.sendLine("***WARNING*** Do not leave during this process! it won't take long!")
            self.CLASSLIST()
            self.state = "PSTART"
            print self.name, "is entering character creation..."
        if answer in('n', 'no', 'N', 'No'):
            self.handle_CLEARSCREEN()
            self.state = "NCREATE"
            self.sendLine("")
            self.sendLine("Please enter your desired username")

    def CLASSLIST(self):
            self.sendLine("What class would you like to pick?")
            self.sendLine("Classes:")
            self.sendLine(" - Warrior")
            self.sendLine(" - Rogue")
            self.sendLine(" - Priest")
            self.sendLine(" - Magician")
            self.sendLine("Use /info <class> for more info")

    def Regeneration(self):
        self.health = self.health + self.healthregen
        if self.health > self.maxhealth:
            self.health = self.maxhealth
        self.mana = self.mana + self.manaregen
        if self.mana > self.maxmana:
            self.mana = self.maxmana
        reactor.callLater(15.0, self.Regeneration)

    def handle_CHECKPASS(self, answer):
        if answer in('yes', 'y', 'Yes', 'Y'):
            self.sendLine("Lets double check your info...")
            self.sendLine("Username : %s" % (self.name))
            self.sendLine("Password : %s" % (self.password))
            self.sendLine("")
            self.sendLine("Is this true?")
            self.state = "DOUBLECHECK"
        if answer in('n', 'no', 'N', 'No'):
            self.sendLine("Please enter your desired password")
            self.state = "CPASSWORD"

    def handle_CPASSWORD(self, password):
        p = str(password)
        self.password = p
        self.sendLine("Is the password... %s , correct? (Y/N)" % (p))
        self.state = "CHECKPASS"

    def handle_NCHECK(self, check):
        if check in("Y", "y"):
            self.sendLine("Please enter your desired password")
            self.state = "CPASSWORD"
        if check in("N", "n"):
            self.sendLine("Please enter the username you want, correctly")
            self.state = "NCREATE"

    def handle_CREATE(self, answer):
        if answer in('Retry', 'retry', 'r', 'R'):
            self.sendLine("Username :")
            self.state = "LOGINCHECK"
        if answer in('Create', 'C', 'create', 'c'):
            self.sendLine("Please enter your desired username")
            self.state = "NCREATE"

# LOGIN SEQUENCE
    def handle_LOGINCHECK(self, name):
        global c
        if self.users.has_key(name):  # lint:ok
            self.sendLine("User is already logged in...")
            self.sendLine("Please try another name...")
        else:
            t = name
            t = (t,)
            c.execute('SELECT * FROM ID WHERE Name=?', t)
            namecheck = c.fetchone()
            if(namecheck == None):
                self.sendLine("There is no account with that name")
                self.sendLine("Retry? or Create?")
                self.state = "CREATE"
            else:
                self.name = name
                self.sendLine("Password :")
                self.state = "LOGINPASS"

    def handle_LOGINPASS(self, password):
        global c
        t = str(self.name)
        t = (t,)
        test = password
        test = str(test)
        c.execute('SELECT * FROM ID WHERE Name=?', t)
        check = c.fetchone()
        check1 = check[1]
        if(test == check1):
            self.sendLine("Login Success!")
            self.handle_CLEARSCREEN()
            self.LOAD()
        else:
            self.sendLine("")
            self.sendLine("")
            self.sendLine("Login failed... try again")
            self.sendLine("Username :")
            self.state = "LOGINCHECK"



# ROOM HANDLING
    def displayMobs(self):
        global c
        room = (self.room,)
        c.execute('''SELECT * FROM RoomMobs where ID=?''', room)
        test = c.fetchone()
        self.sendLine("Mobs nearby...")
        count = 1
        while count <= 5:
            if test[count] in('', None):
                count = count + 1
            else:
                ID = str(test[count])
                ID = (ID,)
                c.execute('''SELECT * from ActiveMonster WHERE RandomID=?''', ID)
                test2 = c.fetchone()
                cnt = str(count)
                Name = test2[3]
                Name = str(Name)
                CR = test2[2]
                CR = float(CR)
                CR = self.level / CR
                if(CR >= 0.00):
                    Rating = 'Impossible'
                if(CR >= 0.35):
                    Rating = 'Very Hard'
                if(CR >= 0.50):
                    Rating = 'Hard'
                if(CR >= 0.66):
                    Rating = 'Normal-Hard'
                if(CR >= 1.00):
                    Rating = 'Normal'
                if(CR >= 1.50):
                    Rating = 'Normal-Easy'
                if(CR >= 2.00):
                    Rating = 'Easy'
                if(CR >= 5.00):
                    Rating = 'Very Easy'
                mobs = cnt + ")" + "" + Name + '[' + Rating +']'
                count = count + 1
                self.sendLine(mobs)

    def displayPlayers(self):
        global c
        room = (self.room,)
        c.execute('''SELECT * FROM RoomPlayers where ID=?''', room)
        test = c.fetchone()
        players = "Players nearby"
        count = 1
        while(count <= 20):
            teststr = test[count]
            teststr = str(teststr)
            if teststr in('', None):
                count = count + 1
            else:
                if teststr == self.name:
                    pass
                    count = count + 1
                else:
                    name = teststr
                    players = players + " " + name
                    count = count + 1
        if players == "Players nearby":
            pass
        else:
            self.sendLine("%s" % players)

    def moveRooms(self, answer):
        room = self.room
        room = (room,)
        c.execute("""SELECT * FROM RoomExits where ID=?""", room)
        test = c.fetchone()
        direction = answer
        if direction in ('N', 'n', 'north', 'North'):
            if test[2] not in ('', None):
                self.room = test[2]
                self.updateRoom('North', 'South')
                self.displayExits()
            else:
                self.sendLine("Cannot go this direction")
                self.displayExits()
        if direction in ('S', 's', 'south', 'South'):
            if test[4] not in ('', None):
                self.room = test[4]
                self.updateRoom('South', 'North')
                self.displayExits()
            else:
                self.sendLine("Cannot go this direction")
                self.displayExits()
        if direction in ('E', 'e', 'East', 'east'):
            if test[3] not in ('', None):
                self.room = test[3]
                self.updateRoom('East', 'West')
                self.displayExits()
            else:
                self.sendLine("Cannot go this direction")
                self.displayExits()
        if direction in ('W', 'w', 'west', 'West'):
            if test[5] not in ('', None):
                self.room = test[5]
                self.updateRoom('West', 'East')
                self.displayExits()
            else:
                self.sendLine("Cannot go this direction")
                self.displayExits()

    def updateRoom(self, direction, opposite):
        global c
        room = self.room
        roomc = (room,)
        c.execute('''SELECT * FROM RoomPlayers WHERE ID=?''', roomc)
        test = c.fetchone()
        counter = 1
        while counter <= 20:
            if test[counter] not in('', None, 'None'):
                counter = counter + 1
            else:
                lastroom = self.lastroom
                last = (lastroom,)
                c.execute('''SELECT * FROM RoomPlayers where ID=?''', last)
                test = c.fetchone()
                count = 1
                while(count <= 20):
                    teststr = test[count]
                    teststr = str(teststr)
                    if teststr in('', None):
                        count = count + 1
                    else:
                        if teststr == self.name:
                            pass
                            count = count + 1
                        else:
                            name = teststr
                            count = count + 1
                            diction = self.users
                            name = str(name)
                            atk = diction.get(name)
                            if direction in('Teleport'):
                                atk.sendLine("%s has teleported away!" % (self.name))
                            else:
                                atk.sendLine("%s has moved %s" % (self.name, direction))
                column = "'Slot" + str(self.placement) + "'"
                c.execute("UPDATE RoomPlayers SET " + column + "=? WHERE ID=?", ('', lastroom))
                conn.commit()
                c.execute('''SELECT * FROM RoomPlayers where ID=?''', roomc)
                test = c.fetchone()
                count = 1
                while(count <= 20):
                    teststr = test[count]
                    teststr = str(teststr)
                    if teststr in('', None):
                        count = count + 1
                    else:
                        if teststr == self.name:
                            pass
                            count = count + 1
                        else:
                            name = teststr
                            count = count + 1
                            diction = self.users
                            name = str(name)
                            atk = diction.get(name)
                            if direction in('Teleport'):
                                atk.sendLine("%s has teleported in" % (self.name))
                            else:
                                atk.sendLine("%s has entered from the %s" % (self.name, opposite))
                column = "'Slot" + str(counter) + "'"
                c.execute("UPDATE RoomPlayers SET " + column + "=? WHERE ID=?", (self.name, room))
                self.lastroom = room
                self.placement = counter
                self.room = room
                if self.room in (1,2,3,4,5,6,7,8,9,10,11,12):
                    self.regionname = 'Noobie Forest'
                conn.commit()
                counter = 30
#        else:
#            print "Room is full, please try again later"
        conn.commit()

    def displayExits(self):
        global c
        room = (self.room,)
        c.execute("""SELECT * FROM RoomExits where ID=?""", room)
        test = c.fetchone()
        description = str(test[1])
        self.sendLine("%s" % description)
        self.sendLine("")
        rooms = "available exits are: "
        if test[2] not in ('', None):
            rooms = rooms + " N"
        if test[4] not in ('', None):
            rooms = rooms + " S"
        if test[3] not in ('', None):
            rooms = rooms + " E"
        if test[5] not in ('', None):
            rooms = rooms + " W"
        self.sendLine("%s" % rooms)
        self.displayPlayers()
        self.displayMobs()


#COMMANDS
    def handle_CLEARSCREEN(self):
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")
        self.sendLine("")

    def handle_CPASS(self, password):
        p = str(password)
        n = self.name
#        x = (n, p)
#        try:
#            c.execute('''INSERT INTO NamePass VALUES (?,?)''', x)
#        except:
        print "Account Creation has failed!"

    def handle_EQUIP(self):
        self.sendLine("================================")
        self.sendLine("Weapons")
        self.sendLine("================================")
        self.sendLine("Mainhand   : %s" % (self.mainhand))
        self.sendLine("  Stats : %s - %s" % (self.mainhandvalmin, self.mainhandvalmax))
        self.sendLine("Offhand    : %s" % (self.offhand))
        if self.offhandtype == 'Weapon':
            self.sendLine("  Stats : %s - %s" % (self.offhandvalmin, self.offhandvalmax))
        else:
            self.sendLine("  Stats : %s" % (self.offhandvalmin))
        self.sendLine("================================")
        self.sendLine("Armor")
        self.sendLine("================================")
        self.sendLine("Helmet     : %s" % (self.helmet))
        self.sendLine("  Armor : %s" % (self.helmetvalue))
        self.sendLine("Chestpiece : %s" % (self.body))
        self.sendLine("  Armor : %s" % (self.bodyvalue))
        self.sendLine("Legpiece   : %s" % (self.lowerbody))
        self.sendLine("  Armor : %s" % (self.lowerbodyvalue))
        self.sendLine("Boots      : %s" % (self.boots))
        self.sendLine("  Armor : %s" % (self.bootsvalue))

    def EQUIPSTART(self):
        t = self.mainhandid
        t = (t,)
        c.execute('SELECT * FROM Gear WHERE ID=?', t)
        test = c.fetchone()
        if test == None:
            pass
        else:
            self.mainhand = str(test[1])
            self.mainhandvalmin = test[3]
            self.mainhandvalmax = test[4]
            self.mainhandspeed = test[5]
        t = self.offhandid
        t = (t,)
        c.execute('SELECT * FROM Gear WHERE ID=?', t)
        test = c.fetchone()
        if test == None:
            pass
        else:
            self.offhand = str(test[1])
            self.offhandtype = str(test[2])
            self.offhandvalmin = test[3]
            self.offhandvalmax = test[4]
            self.offhandspeed = test[5]
            if self.offhandtype == 'Weapon':
                att = self.mainhandspeed
                att2 = self.offhandspeed / 2.00
                attackspeed = att + att2
                self.attackspeed = attackspeed
            else:
                self.attackspeed = self.mainhandspeed
            if self.offhandtype == 'Shield':
                defence = self.offhandvalmin
                self.defence = defence + self.defence
            else:
                pass
        t = self.helmet
        t = (t,)
        c.execute('SELECT * FROM Gear WHERE ID=?', t)
        test = c.fetchone()
        if test == None:
            pass
        else:
            self.helmet = str(test[1])
            self.helmetvalue = test[3]
            defence = self.defence + self.helmetvalue
            self.defence = defence
        t = self.bodyid
        t = (t,)
        c.execute('SELECT * FROM Gear WHERE ID=?', t)
        test = c.fetchone()
        if test == None:
            pass
        else:
            self.body = str(test[1])
            self.bodyvalue = test[3]
            defence = self.defence + self.bodyvalue
            self.defence = defence
        t = self.lowerbodyid
        t = (t,)
        c.execute('SELECT * FROM Gear WHERE ID=?', t)
        test = c.fetchone()
        if test == None:
            pass
        else:
            self.lowerbody = str(test[1])
            self.lowerbodyvalue = test[3]
            defence = self.defence + self.lowerbodyvalue
            self.defence = defence
        t = self.bootsid
        t = (t,)
        c.execute('SELECT * FROM Gear WHERE ID=?', t)
        test = c.fetchone()
        if test == None:
            pass
        else:
            self.boots = str(test[1])
            self.bootsvalue = test[3]
            defence = self.defence + self.bootsvalue
            self.defence = defence
            self.sendLine("Gear Equipped! Check it with /equip")

    def STATS(self):
        self.sendLine("================================")
        self.sendLine("Name :   %s" % (self.name))
        self.sendLine("================================")
        self.sendLine("Class :   %s" % (self.classname))
        self.sendLine("Subclass: %s" % (self.subclass))
        self.sendLine("Exp :     %-5s" % (self.exp))
        self.sendLine("ExpTNL :  %-5s" % (self.exptnl))
        self.sendLine("================================")
        self.VitalBarDisplay('health', self.health, self.maxhealth)
        self.sendLine("      %3s / %3s    HPRegen : %2s" % (self.health, self.maxhealth, self.healthregen))
        self.VitalBarDisplay('mana', self.mana, self.maxmana)
        self.sendLine("      %3s / %3s    MPRegen : %2s" % (self.mana, self.maxmana, self.manaregen))
        self.sendLine("================================")
        self.sendLine("Str : %2s   Attack:   %3s" % (self.strength, self.attack))     # ++health   ++physical attack  +health regen
        self.sendLine("Con : %2s   Defence:  %3s" % (self.constitution, self.defence)) # ++health   ++health regen     +physical defence
        self.sendLine("Dex : %2s   Accuracy: %3s" % (self.dexterity, self.accuracy))    # ++accuracy                    +critical chance
        self.sendLine("Agl : %2s   Dodge:    %3s" % (self.agility, self.dodge))      # ++dodge                       +critical chance
        self.sendLine("Wis : %2s   Mag Def:  %3s" % (self.wisdom, self.mdefence))       # ++mana     ++mana regen       +magic defence
        self.sendLine("Int : %2s   Mag Atk:  %3s" % (self.intellegence, self.mattack)) # ++mana     ++magic attack     +mana regen

    def handle_PSTART(self, choice):
        choice1 = choice[0:5]
        if(choice1 == '/pick'):
            choice2 = choice[6:]
            if choice2 in('Warrior', 'warrior', 'Rogue', 'rogue', 'Priest', 'priest', 'Magician', 'magician'):
                if choice2 in('warrior', 'Warrior'):
                    self.MakeWarrior()
                    self.StatCreation()
                    self.STATS()
                    self.sendLine("Pick a stat to add a point into...")
                    self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                    self.skillpoints = 5
                    self.sendLine("%s points remaining" % self.skillpoints)
                    print self.name, "created a", self.classname
                    self.state = "AddPoints"
                if choice2 in('rogue', 'Rogue'):
                    self.MakeRogue()
                    self.StatCreation()
                    self.STATS()
                    self.sendLine("Pick a stat to add a point into...")
                    self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                    self.skillpoints = 5
                    self.sendLine("%s points remaining" % self.skillpoints)
                    print self.name, "created a", self.classname
                    self.state = "AddPoints"
                if choice2 in('priest' 'Priest'):
                    self.MakePriest()
                    self.StatCreation()
                    self.STATS()
                    self.sendLine("Pick a stat to add a point into...")
                    self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                    self.skillpoints = 5
                    self.sendLine("%s points remaining" % self.skillpoints)
                    print self.name, "created a", self.classname
                    self.state = "AddPoints"
                if choice2 in ('magician', 'Magician'):
                    self.MakeMagician()
                    self.StatCreation()
                    self.STATS()
                    self.sendLine("Pick a stat to add a point into...")
                    self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                    self.skillpoints = 5
                    self.sendLine("%s points remaining" % self.skillpoints)
                    print self.name, "created a", self.classname
                    self.state = "AddPoints"
            else:
                self.sendLine("Not a valid class choice try again")
                self.sendLine("- Warrior")
                self.sendLine("- Rogue")
                self.sendLine("- Priest")
                self.sendLine("- Magician")
        if(choice1 == '/info'):
            choice2 = choice[6:]
            if choice2 in('Warrior', 'warrior', 'Rogue', 'rogue', 'Priest', 'priest', 'Magician', 'magician'):
                self.INFO(choice2)
        if(choice1 == '/list'):
            self.CLASSLIST()
        if(choice1 == 'more'):
            self.StatCreation()
            self.STATS()
            self.sendLine("Use /pick <class>, or /info <class>, or /list to see the list again")

    def PartyDisplayStats(self):
        if self.partybool is False:
            self.sendLine('No party to display')
        else:
            diction = self.users
            count = 0
            party = self.party
            while count <=5:
                member = party[count]
                person = str(member)
                if person == self.name:
                    count = count + 1
                else:
                    member = diction.get(person)
                    self.sendLine("%s" % member.name)
                    self.VitalBarDisplay('Health :', member.health, member.maxhealth)
                    self.sendLine('%3s / %3s' % (member.health, member.maxhealth))
                    self.VitalBarDisplay('Mana   :', member.mana, member.maxmana)
                    print member.mana, '/', member.maxmana

    def PartyInvite(self, name):
        party = self.party
        if party[0] == self.name:
            pass

    def VitalBarDisplay(self, vital, value, maxvalue):
        value = float(value)
        maxvalue = float(maxvalue)
        percent = value / maxvalue
        percent = percent * 100
        percent = int(percent)
        percent = str(percent)
        if percent in('100'):
            display = '||||||||||||||||||||'
        if percent in('95', '96', '97', '98', '99'):
            display = '|||||||||||||||||||-'
        if percent in('90', '91', '92', '93', '94'):
            display = '||||||||||||||||||--'
        if percent in('85', '86', '87', '88', '89'):
            display = '|||||||||||||||||---'
        if percent in('80', '81', '82', '83', '84'):
            display = '||||||||||||||||----'
        if percent in('75', '76', '77', '78', '79'):
            display = '|||||||||||||||-----'
        if percent in('70', '71', '72', '73', '74'):
            display = '||||||||||||||------'
        if percent in('65', '66', '67', '68', '69'):
            display = '|||||||||||||-------'
        if percent in('60', '61', '62', '63', '64'):
            display = '||||||||||||--------'
        if percent in('55', '56', '57', '58', '59'):
            display = '|||||||||||---------'
        if percent in('50', '51', '52', '53', '54'):
            display = '||||||||||----------'
        if percent in('45', '46', '47', '48', '49'):
            display = '|||||||||-----------'
        if percent in('40', '41', '42', '43', '44'):
            display = '||||||||------------'
        if percent in('35', '36', '37', '38', '39'):
            display = '|||||||-------------'
        if percent in('30', '31', '32', '33', '34'):
            display = '||||||--------------'
        if percent in('25', '26', '27', '28', '29'):
            display = '|||||---------------'
        if percent in('20', '21', '22', '23', '24'):
            display = '||||----------------'
        if percent in('15', '16', '17', '18', '19'):
            display = '|||-----------------'
        if percent in('10', '11', '12', '13', '14'):
            display = '||------------------'
        if percent in('5', '6', '7', '8', '9'):
            display = '|-------------------'
        if percent in('0', '1', '2', '3', '4'):
            display = '--------------------'
        per = '%'
        if vital == 'health':
            self.sendLine('Health (%s)  %s%s' % (display, per, percent))
        if vital =='mana':
            self.sendLine('Mana   (%s)  %s%s' % (display, per, percent))

    def INFO(self, classname):
        if classname in('warrior', 'Warrior'):
            self.handle_CLEARSCREEN()
            self.sendLine("The warrior is a class which is trained in delivering heavy blows,")
            self.sendLine("and taking hits for his allies. He utilizes a higher strength and")
            self.sendLine("constitution to support these roles. Advanced classes are as follows...")
            self.sendLine("")
            self.sendLine("Subclass    Advanced Class  Requirement")
            self.sendLine("- NONE      - Berserker     30W")
            self.sendLine("                 *A strong brute with high health")
            self.sendLine("- Rogue     - Blademaster   20W/10R")
            self.sendLine("                 *Accurate and deadly strikes")
            self.sendLine("- Priest    - Paladin       20W/10P")
            self.sendLine("                 *Tank focus with healing abilities")
            self.sendLine("- Magician  - Chaos Knight  20W/10M")
            self.sendLine("                 *A strong fighter utilizing dark arts")
            self.MakeWarrior()
            self.INFO2()
            self.sendLine("")
            self.sendLine("Use 'more' for an indepth character sheet with stats")
            self.sendLine("Use /pick <class>, or /info <class>, or /list to see the list again")
        if classname in('rogue','Rogue'):
            self.handle_CLEARSCREEN()
            self.sendLine("The rogue is a class which is trained in quick, accurate strikes and,")
            self.sendLine("weakening his enemies. He utilizes a high dexterity for accuracy and")
            self.sendLine("agility to evade many incoming attacks. Advanced classes are as follows...")
            self.sendLine("")
            self.sendLine("Subclass    Advanced Class  Requirement")
            self.sendLine("- NONE      - Assassin      30R")
            self.sendLine("                 *A Master of accurate, critical strikes")
            self.sendLine("- Warrior   - Blademaster   20R/10W")
            self.sendLine("                 *Accurate and deadly strikes")
            self.sendLine("- Priest    - Ranger        20R/10P")
            self.sendLine("                 *Melee fighter with nature healing / poisons")
            self.sendLine("- Magician  - Shadow Blades 20R/10M")
            self.sendLine("                 *An agile shadow utilizing dark blades of magic")
            self.MakeRogue()
            self.INFO2()
            self.sendLine("")
            self.sendLine("Use 'more' for an indepth character sheet with stats")
            self.sendLine("Use /pick <class>, or /info <class>, or /list to see the list again")
        if classname in('priest','Priest'):
            self.handle_CLEARSCREEN()
            self.sendLine("The priest is a class which has been trained with mental and physical aptitude.")
            self.sendLine("Using its high constitution to survive and high wisdom to heal, the priest is")
            self.sendLine("a necessary companion in any starting group. Advanced classes are as follows...")
            self.sendLine("")
            self.sendLine("Subclass    Advanced Class  Requirement")
            self.sendLine("- NONE      - Templar       30P")
            self.sendLine("                 *A Magic user that focuses in group healing")
            self.sendLine("- Warrior   - Paladin       20P/10W")
            self.sendLine("                 *Tank focus with healing abilities")
            self.sendLine("- Rogue     - Ranger        20P/10R")
            self.sendLine("                 *Melee fighter with nature healing, and poisons")
            self.sendLine("- Magician  - Sage          20P/10M")
            self.sendLine("                 *A Master of magic that can heal and deal damage")
            self.MakePriest()
            self.INFO2()
            self.sendLine("")
            self.sendLine("Use 'more' for an indepth character sheet with stats")
            self.sendLine("Use /pick <class>, or /info <class>, or /list to see the list again")
        if classname in('magician', 'Magician'):
            self.handle_CLEARSCREEN()
            self.sendLine("The Magician is a class which has been trained with a magical focus. Using its")
            self.sendLine("high wisdom for mana, and high intellegence for spell damage, this class")
            self.sendLine("creates some powerful damage. Advanced classes are as follows...")
            self.sendLine("")
            self.sendLine("Subclass    Advanced Class  Requirement")
            self.sendLine("- NONE      - Arch Mage     30M")
            self.sendLine("                 *A Master of magic that can deal aoe damage")
            self.sendLine("- Warrior   - Chaos Knight  20M/10W")
            self.sendLine("                 *A strong fighter utilizing dark arts")
            self.sendLine("- Rogue     - Shadow Blade  20M/10R")
            self.sendLine("                 *An agile shadow utilizing dark blades of magic")
            self.sendLine("- Priest    - Sage          20M/10P")
            self.sendLine("                 *A Master of magic that can heal and deal damage")
            self.MakeMagician()
            self.INFO2()
            self.sendLine("")
            self.sendLine("Use 'more' for an indepth character sheet with stats")
            self.sendLine("Use /pick <class>, or /info <class>, or /list to see the list again")

    def INFO2(self):
        self.sendLine("Core Stats")
        self.sendLine("Strength     : %s" % (self.strength))
        self.sendLine("Constitution : %s" % (self.constitution))
        self.sendLine("Dexterity    : %s" % (self.dexterity))
        self.sendLine("Agility      : %s" % (self.agility))
        self.sendLine("Wisdom       : %s" % (self.wisdom))
        self.sendLine("Intellegence : %s" % (self.intellegence))

    def MakeWarrior(self):
        self.level = 1
        self.exp = 0
        self.exptnl = 1000
        self.classname = 'Warrior'
        self.strength = 16
        self.constitution = 16
        self.dexterity = 14
        self.agility = 12
        self.wisdom = 12
        self.intellegence = 10
        self.mainhandid = 1
        self.offhandid = 2
        self.helmet = None
        self.bodyid = 7
        self.lowerbodyid = 8
        self.boots = None

    def MakeRogue(self):
        self.level = 1
        self.exp = 0
        self.exptnl = 1000
        self.classname = 'Rogue'
        self.strength = 14
        self.constitution = 12
        self.dexterity = 16
        self.agility = 16
        self.wisdom = 11
        self.intellegence = 11
        self.mainhandid = 3
        self.offhandid = 4
        self.helmet = None
        self.bodyid = 9
        self.lowerbodyid = 10
        self.boots = None

    def MakePriest(self):
        self.level = 1
        self.exp = 0
        self.exptnl = 1000
        self.classname = 'Priest'
        self.strength = 14
        self.constitution = 16
        self.dexterity = 11
        self.agility = 11
        self.wisdom = 16
        self.intellegence = 12
        self.mainhandid = 5
        self.offhandid = 2
        self.helmet = None
        self.bodyid = 7
        self.lowerbodyid = 8
        self.bootsid = None

    def MakeMagician(self):
        self.level = 1
        self.exp = 0
        self.exptnl = 1000
        self.classname = 'Magician'
        self.strength = 11
        self.constitution = 12
        self.dexterity = 11
        self.agility = 14
        self.wisdom = 16
        self.intellegence = 16
        self.mainhandid = 6
        self.offhandid = None
        self.helmet = None
        self.bodyid = 11
        self.lowerbodyid = 12
        self.bootsid = None

    def CCCHECK(self, answer):
        if answer in('con', 'Con', 'Continue', 'continue'):
            self.room = 0
            self.state = "Room"
            self.handle_CLEARSCREEN()
            self.sendLine("Welcome %s to the world of Arr'Fia" % (self.name))
            self.FIRSTSAVE()
            self.EQUIPSTART()
            self.handle_WELCOME()
        if answer in('res', 'Res', 'restart', 'Restart'):
            self.CLASSLIST()
            self.state = "PSTART"

    def AdditionalPoints(self, stat):
        if stat in('str', 'Str', 'strength', 'Strength', 's', 'S'):
            if self.strength == 20:
                self.sendLine("You can only go to a stat max of 20 at creation")
                self.sendLine("Please pick a different stat")
                return
            else:
                self.strength = self.strength + 1
                self.skillpoints = self.skillpoints - 1
                self.StatCreation()
                self.STATS()
                if self.skillpoints > 0:
                    self.sendLine("Pick a stat to add a point into...")
                    self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                    self.sendLine("%s points remaining" % self.skillpoints)
                else:
                    self.state = "CCCHECK"
                    self.sendLine("These are the final results of your creation")
                    self.sendLine("Would you like to continue or restart? (con/res)")
        else:
            if stat in('dex', 'Dex', 'dexterity', 'Dexterity', 'd', 'D'):
                if self.dexterity == 20:
                    self.sendLine("You can only go to a stat max of 20 at creation")
                    self.sendLine("Please pick a different stat")
                    return
                else:
                    self.dexterity = self.dexterity + 1
                    self.skillpoints = self.skillpoints - 1
                    self.StatCreation()
                    self.STATS()
                    if self.skillpoints > 0:
                        self.sendLine("Pick a stat to add a point into...")
                        self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                        self.sendLine("%s points remaining" % self.skillpoints)
                    else:
                        self.state = "CCCHECK"
                        self.sendLine("These are the final results of your creation")
                        self.sendLine("Would you like to continue or restart? (con/res)")
            else:
                if stat in('con', 'Con', 'constitution', 'Constitution', 'c', 'C'):
                    if self.constitution == 20:
                        self.sendLine("You can only go to a stat max of 20 at creation")
                        self.sendLine("Please pick a different stat")
                        return
                    else:
                        self.constitution = self.constitution + 1
                        self.skillpoints = self.skillpoints - 1
                        self.StatCreation()
                        self.STATS()
                        if self.skillpoints > 0:
                            self.sendLine("Pick a stat to add a point into...")
                            self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                            self.sendLine("%s points remaining" % self.skillpoints)
                        else:
                            self.state = "CCCHECK"
                            self.sendLine("These are the final results of your creation")
                            self.sendLine("Would you like to continue or restart? (con/res)")
                else:
                    if stat in('agi', 'Agi', 'agility', 'Agility', 'a', 'A'):
                        if self.agility == 20:
                            self.sendLine("You can only go to a stat max of 20 at creation")
                            self.sendLine("Please pick a different stat")
                            return
                        else:
                            self.agility = self.agility + 1
                            self.skillpoints = self.skillpoints - 1
                            self.StatCreation()
                            self.STATS()
                            if self.skillpoints > 0:
                                self.sendLine("Pick a stat to add a point into...")
                                self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                                self.sendLine("%s points remaining" % self.skillpoints)
                            else:
                                self.state = "CCCHECK"
                                self.sendLine("These are the final results of your creation")
                                self.sendLine("Would you like to continue or restart? (con/res)")
                    else:
                        if stat in('wis', 'Wis', 'wisdom', 'Wisdom', 'w', 'W'):
                            if self.wisdom == 20:
                                self.sendLine("You can only go to a stat max of 20 at creation")
                                self.sendLine("Please pick a different stat")
                                return
                            else:
                                self.wisdom = self.wisdom + 1
                                self.skillpoints = self.skillpoints - 1
                                self.StatCreation()
                                self.STATS()
                                if self.skillpoints > 0:
                                    self.sendLine("Pick a stat to add a point into...")
                                    self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                                    self.sendLine("%s points remaining" % self.skillpoints)
                                else:
                                    self.state = "CCCHECK"
                                    self.sendLine("These are the final results of your creation")
                                    self.sendLine("Would you like to continue or restart? (con/res)")
                        else:
                            if stat in('int', 'Int', 'Intellegence', 'intellegence', 'i', 'I'):
                                if self.intellegence == 20:
                                    self.sendLine("You can only go to a stat max of 20 at creation")
                                    self.sendLine("Please pick a different stat")
                                    return
                                else:
                                    self.intellegence = self.intellegence + 1
                                    self.skillpoints = self.skillpoints - 1
                                    self.StatCreation()
                                    self.STATS()
                                    if self.skillpoints > 0:
                                        self.sendLine("Pick a stat to add a point into...")
                                        self.sendLine("Choices : Str, Con, Dex, Agi, Wis, Int")
                                        self.sendLine("%s points remaining" % self.skillpoints)
                                    else:
                                        self.state = "CCCHECK"
                                        self.sendLine("These are the final results of your creation")
                                        self.sendLine("Would you like to continue or restart? (con/res)")

    def StatCreation(self):
        strength = self.strength
        constitution = self.constitution
        if self.classname in('Warrior', 'Priest', 'Berserker', 'Paladin', 'Chaos Knight', 'Blademaster', 'Templar'):
            health = strength * 2
            health2 = constitution * 2
            health = int(health)
            health2 = int(health2)
        else:
            health = strength * 1.5
            health2 = constitution * 2
            health = int(health)
            health2 = int(health2)
        healthregen = strength / 8
        healthregen2 = constitution / 4
        health = health + health2
        healthregen = healthregen + healthregen2
        attack = strength * 2
        strdmg = strength / 8.0
        strdmg = int(strdmg)
        defence = constitution * 2
        self.strengthdamage = strdmg
        self.health = health
        self.maxhealth = health
        self.healthregen = healthregen
        self.attack = attack
        self.defence = defence
        dexterity = self.dexterity
        agility = self.agility
        accuracy = dexterity * 2
        accuracy = accuracy + 50
        speedmod = agility + dexterity
        if self.classname in('Shadow Blade', 'Blade Master', 'Ranger', 'Rogue'):
            speedmod = speedmod / 300.00
        else:
            speedmod = speedmod / 250.00
        speedmod = 1 - speedmod
        if self.classname in('Shadow Blade', 'Blade Master', 'Ranger', 'Rogue'):
            dodge = agility * 2
        else:
            dodge = agility * 1.5
            dodge = int(dodge)
        critical = dexterity / 4
        critical1 = agility / 4
        critical = critical + critical1
        self.speedmod = speedmod
        self.accuracy = accuracy
        self.dodge = dodge
        self.critical = critical
        wisdom = self.wisdom
        intellegence = self.intellegence
        if self.classname in('Warrior', 'Blade Master', 'Berserker', 'Paladin', 'Chaos Knight', 'Assassin' 'Ranger', 'Rogue'):
            mana = wisdom * 2
            mana2 = intellegence * 1.5
            mana2 = int(mana2)
        else:
            mana = wisdom * 2
            mana2 = intellegence * 2
            mana2 = int(mana2)
        manaregen = wisdom / 4
        manaregen2 = intellegence / 8
        mana = mana + mana2
        manaregen = manaregen + manaregen2
        mattack = intellegence * 2
        mdefence = wisdom * 2
        self.mana = mana
        self.maxmana = mana
        self.manaregen = manaregen
        self.mattack = mattack
        self.mdefence = mdefence

    def handle_CHARACTERLOOKUP(self, name):
        diction = self.users
        person = str(name)
        char = diction.get(person)
        if char != None:
            self.sendLine("================================")
            self.sendLine("Name  : %s" % (char.name))
            self.sendLine("Class : %s" % (char.classname))
            self.sendLine("Level : %s" % (char.level))
            self.sendLine("Region: %s" % (char.regionname))
            self.sendLine("================================")
            self.sendLine("HP: %s / %s" % (char.health, char.maxhealth))
            self.sendLine("MP: %s / %s" % (char.mana, char.maxmana))
            self.sendLine("================================")
            self.sendLine("Str : %s" % (char.strength))
            self.sendLine("Con : %s" % (char.constitution))
            self.sendLine("Dex : %s" % (char.dexterity))
            self.sendLine("Agl : %s" % (char.agility))
            self.sendLine("Wis : %s" % (char.wisdom))
            self.sendLine("Int : %s" % (char.intellegence))
        else:
            self.sendLine("Error : Either player is not online, or does not exist")

    def handle_WELCOME(self):
        self.sendLine("Use /help for a reference")
        name = self.name
        self.users[name] = self
        for name, protocol in self.users.iteritems():
            if protocol != self:
                message = "%s has joined" % (self.name,)
                protocol.sendLine(message)
        self.state = "CHAT"
        self.displayExits()
        self.Regeneration()

    def handle_DEATH(self, atk):
        atk.health = atk.maxhealth
        self.pkilled += 1
        atk.sendLine("%s has killed you..." % (self.name))
        atk.sendLine("You have been sent back to spawn...")
        atk.room = 1
        self.sendLine("You have killed %s! Your pk rating is now %s" % (atk.name, self.pk))

    def handle_PASSWORD(self, password):
        if(password == self.password):
            self.handle_WELCOME()
        else:
            self.sendLine("Returning to login process")
            self.handle_CLEARSCREEN()
            self.sendLine("What's your name?'")
            self.state = "GETNAME"

    def INVENTORY(self):
        self.sendLine("================================")
        self.sendLine("Inventory")
        self.sendLine("================================")
        self.sendLine("Gold : %s" % self.gold)
        self.sendLine("1]   : %s" % self.slot1)
        self.sendLine("2]   : %s" % self.slot2)
        self.sendLine("3]   : %s" % self.slot3)
        self.sendLine("4]   : %s" % self.slot4)
        self.sendLine("5]   : %s" % self.slot5)
        self.sendLine("6]   : %s" % self.slot6)
        self.sendLine("7]   : %s" % self.slot7)
        self.sendLine("8]   : %s" % self.slot8)
        self.sendLine("9]   : %s" % self.slot9)
        self.sendLine("10]  : %s" % self.slot10)
        self.sendLine("11]  : %s" % self.slot11)
        self.sendLine("12]  : %s" % self.slot12)
        self.sendLine("13]  : %s" % self.slot13)
        self.sendLine("14]  : %s" % self.slot14)
        self.sendLine("15]  : %s" % self.slot15)
        self.sendLine("16]  : %s" % self.slot16)
        self.sendLine("17]  : %s" % self.slot17)
        self.sendLine("18]  : %s" % self.slot18)
        self.sendLine("19]  : %s" % self.slot19)
        self.sendLine("20]  : %s" % self.slot20)

    def handle_GETNAME(self, name):
        if self.users.has_key(name):  # lint:ok
            self.sendLine("User is already logged in...")
            return
        else:
            self.name = name
            self.handle_WELCOME(name)

    def rest(self):
        self.health = self.maxhealth
        self.mana = self.maxmana
        self.restready = False
        self.sendLine("You rest for a while, and you vitals are now maxed")

    def handle_CHAT(self, message):
        if message in ('n', 'N', 'North', 'north'):
            message = str(message)
            self.handle_CLEARSCREEN()
            self.moveRooms(message)
            return
        if message in ('s', 'S', 'South', 'south'):
            message = str(message)
            self.handle_CLEARSCREEN()
            self.moveRooms(message)
            return
        if message in ('W', 'w', 'West', 'west'):
            message = str(message)
            self.handle_CLEARSCREEN()
            self.moveRooms(message)
            return
        if message in ('e', 'E', 'East', 'east'):
            message = str(message)
            self.handle_CLEARSCREEN()
            self.moveRooms(message)
            return
        if(message == '/help'):
            if self.permission == 'Member':
                self.sendLine("The commands available to you are...")
                self.sendLine("/a <#>            *Attack the mob assigned to that slot")
                self.sendLine("/c                *Return back to command mode")
                self.sendLine("/changepass       *Changes your password")
                self.sendLine("/clear            *clears the screen of text")
                self.sendLine("/equip            *Looks up personal gear equipped")
                self.sendLine("/exit             *exit cleanly and save properly")
                self.sendLine("/inv              *Opens your inventory")
                self.sendLine("/look             *Looks around your area")
                self.sendLine("/lookup <user>    *Looks up a users stats")
                self.sendLine("/pa <user>        *Attack a player")
                self.sendLine("/pk               *Toggles Player fighting on/off (5min wait)")
                self.sendLine("/s                *Locks say chat mode. (use /c to return)")
                self.sendLine("/say <message>    *Talks to other users")
                self.sendLine("/spawn            *Return to spawn immeadiately")
                self.sendLine("/stats            *Looks up your own stats")
                self.sendLine("/suicide          *Commits suicide")
                self.sendLine("/w <user>         *Enter private chat mode")
            if self.permission == 'Moderator':
                self.sendLine("The commands available to you are...")
                self.sendLine("/a <#>              *Attack the mob assigned to that slot")
                self.sendLine("/c                  *Return back to command mode")
                self.sendLine("/changepass         *Changes your password")
                self.sendLine("/clear              *clears the screen of text")
                self.sendLine("/equip              *Looks up personal gear equipped")
                self.sendLine("/exit               *exit cleanly and save properly")
                self.sendLine("/inv                *Opens your inventory")
                self.sendLine("/look               *Looks around the area")
                self.sendLine("/lookup <user>      *Looks up a users stats")
                self.sendLine("/pa <user>          *Attack a player")
                self.sendLine("/perm <perm> <user> *Perm choices are Member, Moderator, Admin")
                self.sendLine("/pk                 *Toggles Player fighting on/off (5min wait)")
                self.sendLine("/rest               *Heal health/mana, useable in a safe place")
                self.sendLine("/s                  *Locks say chat mode. (use /c to return)")
                self.sendLine("/say <message>      *Talks to other users")
                self.sendLine("/spawn            *Return to spawn immeadiately")
                self.sendLine("/stats              *Looks up your own stats")
                self.sendLine("/suicide            *Commits suicide")
                self.sendLine("/w <user>           *Enter private chat mode")
            return
        if(message == '/exit'):
            self.EXIT()
            return
        if(message == '/inv'):
            self.INVENTORY()
            return
        if(message == '/stats'):
            self.STATS()
            return
        if(message == '/rest'):
            if self.room in (0, 6):
                if self.restready is True:
                    self.rest()
                else:
                    self.sendLine("You cannot rest so soon")
            else:
                self.sendLine("It is too dangerous to rest here...")
        if(message == '/changepass'):
            self.sendLine("What do you want your password to be?")
            self.state = "CHANGEPASS"
        if(message[0:7] == '/lookup'):
            try:
                message = message[8:]
                if message in(None, ''):
                    self.sendLine("proper use : /lookup <name>")
                else:
                    self.handle_CHARACTERLOOKUP(message)
            except:
                print "Lookup not working"
            return
        if(message == '/look'):
            self.LOOK()
            return
        if(message == '/equip'):
            self.handle_EQUIP()
            return
        if(message == '/clear'):
            try:
                self.handle_CLEARSCREEN()
            except:
                print "Clear not working"
            return
        if(message == '/suicide'):
            try:
                self.handle_SUICIDE()
            except:
                print "Suicide Failed"
            return
        if(message[0:5] == '/perm'):
            perm = message [6:]
        if(message[0:3] == '/pa'):
            attack = message[4:]
            if attack in(None, ''):
                self.sendLine("Not a valid username")
            else:
                self.handle_PLAYERATTACK(attack)
            return
        if(message[0:6] == '/spawn'):
            if self.spawn is True:
                self.sendLine("Preparing spawn teleport...")
                reactor.callLater(5.0, self.SPAWN)
            else:
                self.sendLine("You can't teleport to spawn yet")
        if(message[0:3] == '/pk'):
            if self.pkswitch is True:
                self.togglePK()
            else:
                self.sendLine("Cannot change pk mode yet...")
        if(message[0:2] == '/s'):
            if(message[0:4] == '/say'):
                check = message[5:]
                if check in(None, ''):
                    self.state = "SAY"
                    self.sendLine("Now in chat mode : SAY")
                    self.sendLine("To leave this mode simply type /c to cancel")
                else:
                    self.handle_SAY(check)
            if(message[0:3] == '/s '):
                check = message[3:]
                if check in(None, ''):
                    self.state = "SAY"
                    self.sendLine("Now in chat mode : SAY")
                    self.sendLine("To leave this mode simply type /c to cancel")
                else:
                    self.handle_SAY(check)
            return
        if(message[0:2] == '/a'):
            try:
                check = message[3:]
                if check in(None, ''):
                    self.sendLine('Please specify which mob you would like to attack')
                else:
                    self.AttackMOB(check)
                return
            except:
                self.sendLine("Target invalid or Error occured")
        if(message[0:2] == '/w'):
            check = message[3:]
            if check in(None, ''):
                self.state = "WHISP"
                self.sendLine("Who would you like to private chat with?")
            else:
                self.handle_WHISP_ini(check)
            return

    def togglePK(self):
        self.pkswitch = False
        if self.pk is True:
            self.pk = False
            self.sendLine("PK Mode is now turned off")
            reactor.callLater(300.0, self.handle_PKTOGGLEWAIT)
            return
        if self.pk is False:
            self.pk = True
            self.sendLine("PK Mode is now turned on! Watch yourself")
            reactor.callLater(300.0, self.handle_PKTOGGLEWAIT)
            return

    def handle_PKTOGGLEWAIT(self):
        self.pkswitch = True
        self.sendLine("Can switch PK Mode again")

    def handle_ATTACKINIT(self):
        self.sendLine("Who are you attacking?")
        self.state = "ATTACK"

    def handle_ATTACKWAIT(self):
        self.attackready = True
        self.sendLine("Attack Ready")

    def handle_RESETSUICIDE(self):
        self.suicide = True

    def handle_SUICIDE(self):
        if self.suicide is True:
            self.sendLine("You have died and been reincarnated at your body")
            self.sendLine("You cannot do this again for 10 minutes")
            self.health = self.maxhealth
            self.suicide = False
            for name, protocol in self.users.iteritems():
        #       if protocol != self: #Use this if you don't want messages to be sent to self'  # lint:ok
                protocol.sendLine("%s has commited suicide..." % (self.name))
                reactor.callLater(600.0, self.handle_RESETSUICIDE)
        else:
            self.sendLine("You cannot suicide for a while still")

    def handle_PLAYERATTACK(self, target):
        diction = self.users
        if target == self.name:
            self.sendLine("You cannot attack yourself... Do you want /suicide?")
            return
        target = str(target)
        atk = diction.get(target)
        if atk.pk == False:
            self.sendLine("Player is not in pk mode... cannot attack")
            return
        if atk is None:
            self.sendLine("Attack failed : User not Found")
        else:
            if self.attackready is True:
                hitmax = 100 + atk.dodge
                hit = random.randint(1, hitmax)
                crit = random.randint(1, 100)
                attackmin = self.mainhandvalmin
                attackmax = self.mainhandvalmax
                if(self.offhandtype == 'Weapon'):
                    offhandmin = self.offhandvalmin * 0.75
                    offhandmin = int(offhandmin)
                    offhandmax = self.offhandvalmax * 0.75
                    offhandmax = int(offhandmax)
                    attackmin = self.mainhandvalmin + offhandmin
                    attackmax = self.mainhandvalmax + offhandmax
                attack = random.randint(attackmin, attackmax) + self.strengthdamage
                if(hit <= self.accuracy):
                    af = float(self.attack)
                    attackmod = af / atk.defence
                    attack = float(attack)
                    attack = attackmod * attack
                    attack = int(attack)
                    if crit <= self.critical:
                        attack = attack * 2
                        if(atk.type == 'Player'):
                            atk.sendLine("You have been critically attacked by %s!" % (self.name))
                        self.sendLine("You ***CRITICALLY HIT*** %s for %s damage!" % (atk.name, attack))
                        atk.health = atk.health - attack
                    else:
                        if(atk.type == 'Player'):
                            atk.sendLine("You have been attacked by %s!" % (self.name))
                        self.sendLine("You ***HIT*** %s for %s damage!" % (atk.name, attack))
                        atk.health = atk.health - attack
                    if(atk.health <= 0):
                        self.handle_DEATH(atk)
                    else:
                        atk.sendLine("You now %s health left..." % (atk.health,))  # lint:ok
                        self.state = "CHAT"
                        self.attackready = False
                        reactor.callLater(self.attackspeed, self.handle_ATTACKWAIT)
                else:
                    if(atk.type == 'Player'):
                        atk.sendLine("You have been attacked by %s!" % (self.name))
                        atk.sendLine("However they missed you...")
                    self.sendLine("You ***MISSED*** %s!" % (atk.name))
                    self.state = "CHAT"
                    self.attackready = False
                    reactor.callLater(self.attackspeed, self.handle_ATTACKWAIT)
            else:
                self.sendLine("You need to wait a little bit longer before attacking")

    def AttackMOB(self, target):
        global c
        slot = target
        slot = int(slot)
        room = (self.room,)
        c.execute('SELECT * FROM RoomMobs WHERE ID=?', room)
        test= c.fetchone()
        mob = test[slot]
        if mob in('', None):
            self.sendLine("Creature doesn't exist!")
            return
        mobs = (mob,)
        c.execute('SELECT * FROM ActiveMonster WHERE RandomID=?', mobs)
        test = c.fetchone()
        name = str(test[3])
        # RandomID, MobID, Level, Name, Health, MaxHealth, Mana, MaxMana, Attack, Defence, Speed, Critical, Accuracy, 13Dodge, Mattack, Mdefence
        if test is None:
            self.sendLine("Attack failed : User not Found")
        else:
            if self.attackready is True:
                hitmax = 100 + int(test[13])
                hit = random.randint(1, hitmax)
                crit = random.randint(1, 100)
                attackmin = self.mainhandvalmin
                attackmax = self.mainhandvalmax
                Critical = False
                if(self.offhandtype == 'Weapon'):
                    offhandmin = self.offhandvalmin * 0.75
                    offhandmin = int(offhandmin)
                    offhandmax = self.offhandvalmax * 0.75
                    offhandmax = int(offhandmax)
                    attackmin = self.mainhandvalmin + offhandmin
                    attackmax = self.mainhandvalmax + offhandmax
                attack = random.randint(attackmin, attackmax) + self.strengthdamage
                if(hit <= self.accuracy):
                    af = float(self.attack)
                    attackmod = af / int(test[9])
                    attack = float(attack)
                    attack = attackmod * attack
                    if crit <= self.critical:
                        attack = attack * 2
                        Critical = True
                    attack = int(attack)
                    mobhp = int(test[4])
                    mobhp = mobhp - attack
                    mob = unicode(mob)
                    c.execute('UPDATE ActiveMonster SET Health=? WHERE RandomID=?', (mobhp, mob))
                    if(int(test[4]) <= 0): # Mob health < 0 Check
                        self.handle_MOBDEATH(test[0], test[2], target)
                        self.sendLine("You have slain the %s" % (name))
                    else:
                        if Critical is True:
                            self.sendLine("You critically hit the %s for %s damage!" % (name, attack))
                            self.handle_TellRoom("%s critically hit %s for %s damage" % (self.name, name, attack))
                        else:
                            self.sendLine("You hit the %s for %s damage!" % (name, attack))
                        self.attackready = False
                        reactor.callLater(self.attackspeed, self.handle_ATTACKWAIT)
                else:
                    self.sendLine("You ***MISSED*** the %s!" % (name))
                    self.attackready = False
                    reactor.callLater(self.attackspeed, self.handle_ATTACKWAIT)
            else:
                self.sendLine("You need to wait a little bit longer before attacking")
            conn.commit()

    def handle_MOBDEATH(self, randomid, CR, slot):
        random = randomid
        mobs = (randomid,)
        c.execute('SELECT * FROM ActiveMonster WHERE RandomID=?', mobs)
        test = c.fetchone()
        CR = test[2]
        self.GiveEXP(CR)
        c.execute('''DELETE FROM ActiveMonster WHERE RandomID=?''', mobs)
        column = "'Slot" + str(slot) + "'"
        c.execute("UPDATE RoomMobs SET " + column + "=? WHERE ID=?", ('', self.room))
        conn.commit()


    def handle_TellRoom(self, line):
        global
        c.execute('''SELECT * FROM RoomPlayers where ID=?''', last)
        test = c.fetchone()
        count = 1
        while(count <= 20):
            teststr = test[count]
            teststr = str(teststr)
            if teststr in('', None):
                count = count + 1
            else:
                if teststr == self.name:
                    count = count + 1
                else:
                    name = teststr
                    count = count + 1
                    diction = self.users
                    name = str(name)
                    atk = diction.get(name)
                    atk.sendLine(line)

    def GiveEXP(self, CR):
        if self.partybool is False:
            cr = float(CR)
            expmod = cr / self.level
            exp = 100 * expmod
            self.sendLine("You have gained %s experience!" % (exp))
            curexp = self.exp
            curexp = exp + curexp
            self.exp = curexp
            self.exptnl = self.exptnl - exp
            self.sendLine("You need %s more to next level." % (self.exptnl))

    def handle_SAY(self, message):
        if(message == '/c'):
            self.state = "CHAT"
            self.sendLine("You have left chat mode : SAY")
        else:
            if self.permission in('Admin', 'Moderator',):
                message = "[%s] %s :: %s" % (self.permission, self.name, message)
            else:
                message = "%s :: %s" % (self.name, message)
            print message
            for name, protocol in self.users.iteritems():
    #           if protocol != self: #Use this if you don't want messages to be sent to self'  # lint:ok
                protocol.sendLine(message)

    def handle_WHISP_ini(self, name):
        self.whisper = name
        diction = self.users
        person = str(self.whisper)
        whisp = diction.get(person)
        if whisp != None:
            self.whisper = name
            self.state = "WHISPER"
            self.sendLine("Now in chat with %s" % (name))
        else:
            self.sendLine("No user with that name, try again...")
            self.state = 'CHAT'

    def SET_PERMISSIONS(self, name, perm):
        diction = self.users
        if self.permission in ('Moderator', 'moderator'):
            if name == self.name:
                self.sendLine("You cannot change your own permissions... Talk to an admin")
                return
            else:
                name = str(name)
                check = diction.get(name)
                if check is None:
                    self.sendLine("Permission change failed : User not Found")
                else:
                    if perm in ('Moderator', 'Member'):
                        if check.permission in ('Moderator', 'Admin', 'Server'):
                            self.sendLine("You only have permission to change people with lower ranked permissions")
                        else:
                            check.permission = perm
                    else:
                        self.sendLine("Valid choices are : Moderator, and Member")
        if self.permission in ('Admin', 'admin'):
            if name == self.name:
                self.sendLine("You cannot change your own permissions... Talk to the server host")
                return
            else:
                name = str(name)
                check = diction.get(name)
                if check is None:
                    self.sendLine("Permission change failed : User not Found")
                else:
                    if perm in ('Admin', 'Moderator', 'Member'):
                        if check.permission in ('Admin', 'Server'):
                            self.sendLine("You only have permission to change people with lower ranked permissions")
                        else:
                            check.permission = perm
                    else:
                        self.sendLine("Valid choices are : Admin, Moderator, and Member")

    def CHANGE_PASSWORD1(self, password):
        self.password = password
        self.state = "CHANGEPASS2"
        self.sendLine("Is the password, %s, correct? (y/n)" % self.password)

    def CHANGE_PASSWORD2(self, answer):
        if answer in("y", "Y", "yes", "Yes"):
            entry = (self.password, self.name)
            c.execute('''UPDATE ID SET Password=? WHERE Name=?''', entry)
            self.sendLine("Password changed!")
            conn.commit()
            self.state = "CHAT"
        if answer in("n", "N", "no", "No"):
            self.sendLine("What do you want your password to be?")
            self.state = "CHANGEPASS"
            return

    def LOOK(self):
        self.displayExits()

    def SPAWN(self):
        self.handle_CLEARSCREEN()
        self.sendLine("You have teleported to spawn")
        self.room = 0
        self.updateRoom('Teleport', 'Teleport')
        self.displayExits()
        self.spawn = False
        reactor.callLater(300.0, self.SpawnReset)
        pass

    def SpawnReset(self):
        self.spawn = True
        self.sendLine("Spawn teleport has been refreshed")

    def EXIT(self):
        leave = "Disconnected"
        self.handle_CLEARSCREEN()
        self.sendLine("You may now close the window safely")
        self.connectionLost(leave)

    def handle_WHISPER(self, message1):
        try:
            if(message1 == '/c'):
                self.state = "CHAT"
                self.sendLine("You have left your private chat")
            else:
                message = "(Private)<---[ %s ] : %s" % (self.name, message1)
                diction = self.users
                person = str(self.whisper)
                whisp = diction.get(person)
                if whisp == None:
                    self.sendLine("Person doesn't exist, or is offline please type /c and try again")
                else:
                    print "[PM] (", self.name, ") -->", "(", person, ")", message1
                    whisp.sendLine(message)
                    message = "(Private)--->[ %s ] : %s" % (whisp.name, message1)
                    self.sendLine(message)
        except:
            print "Whisper failed by", self.name
            self.sendLine("Whisper failed, please type /c and try again")

#    def ExperienceReward(self):
#        global c
#        atk.
#        c.execute('''SELECT * from ActiveMonster WHERE RandomID=?''', ):
#        modifier = atk.

    def threatCalculator(self, damage, multi, target):
        dam = damage
        mult = multi
        dam = dam * 2
        threat = dam * mult


class ChatFactory(Factory):

    def __init__(self):
        self.users = {}  # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)


class MobSpawner():

    def __init__(self):
        global c
        self.NoobieForestMobMax = 10
        self.NoobieForestSpawnRate = 3
        self.NoobieForestRooms = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]
        self.NoobieForestMobs = [1, 2, 3, 4, 18]
        self.NoobieForestRoomMax = 3
        name = ('NoobieForest',)
        c.execute('''SELECT * FROM Regions WHERE Name=?''', name)
        test= c.fetchone()
        self.NoobieForestMobcount = test[1]
        self.NoobieForest_generator()

        # For Mob Spawning
        self.health = 0
        self.mana = 0
        self.strdmg = 0
        self.attack = 0
        self.defence = 0
        self.accuracy = 0
        self.speed = 0
        self.dodge = 0
        self.mattack = 0
        self.mdefence = 0
        self.critical = 0
        self.name = ''

    def StatCreation(self, strength, constitution, dexterity, agility, wisdom, intellegence):
        health = strength * 2
        health2 = constitution * 2
        health = int(health)
        health2 = int(health2)
        health = health + health2
        attack = strength * 2
        strdmg = strength / 8.0
        strdmg = int(strdmg)
        defence = constitution * 2
        self.strdmg = strdmg
        self.health = health
        self.attack = attack
        self.defence = defence
        dexterity = dexterity
        agility = agility
        accuracy = dexterity * 2
        accuracy = accuracy + 50
        speedmod = agility + dexterity
        speedmod = speedmod / 250.00
        speedmod = 1 - speedmod
        dodge = agility * 2
        critical = dexterity / 4.0
        critical1 = agility / 4.0
        critical = critical + critical1
        critical = int(critical)
        self.speed = speedmod
        self.accuracy = accuracy
        self.dodge = dodge
        self.critical = critical
        wisdom = wisdom
        intellegence = intellegence
        mana = wisdom * 2
        mana2 = intellegence * 2
        mana2 = int(mana2)
        mana = mana + mana2
        mattack = intellegence * 2
        mdefence = wisdom * 2
        self.mana = mana
        self.mattack = mattack
        self.mdefence = mdefence

    def CreateMob(self, Randid, Mobtype, room):
        Randid = Randid
        Mobtype = Mobtype
        Randidsql = (Randid,)
        Mobtypesql = (Mobtype,)
        c.execute('''SELECT * From Monsters WHERE ID=?''', Mobtypesql)
        mob = c.fetchone()
        self.name = mob[1]
        level = mob[2]
        stren = mob[3]
        con = mob[4]
        dex = mob[5]
        agi = mob[6]
        wis = mob[7]
        intel = mob[8]
        self.StatCreation(stren, con, dex, agi, wis, intel)
        mob = (Randid, Mobtype, level, self.name, self.health, self.health, self.mana, self.mana, self.attack, self.defence, self.speed, self.critical, self.accuracy, self.dodge, self.mattack, self.mdefence, room)
        c.execute('''INSERT INTO ActiveMonster VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', mob)

    def NoobieForest_generator(self):
        global c
        regionname = ('NoobieForest',)
        c.execute('''SELECT * FROM Regions WHERE Name=?''', regionname)
        mobcount = c.fetchone()
        mobcount = int(mobcount[1])
        spawn = self.NoobieForestSpawnRate
        if mobcount >= self.NoobieForestMobMax:
            return
        while spawn > 0:
            regionname = ('NoobieForest',)
            room = random.choice(self.NoobieForestRooms)
            roomc = (room,)
            c.execute('''SELECT * From RoomMobs WHERE ID=?''', roomc)
            test = c.fetchone()
            if test[1] in ('', None, 'dead'):
                size = 6
                chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
                id0 = ''.join(random.choice(chars) for x in range(size))
                mon = random.choice(self.NoobieForestMobs)
                self.CreateMob(id0, mon, room)
                # print "Created Mob,", self.name, "in room,", room, "in slot1"
                c.execute('''SELECT * FROM Regions WHERE Name=?''', regionname)
                mobcount = c.fetchone()
                mobcount = mobcount[1]
                mobcount = int(mobcount) + 1
                mobcount = str(mobcount)
                regionname = 'NoobieForest'
                c.execute('''UPDATE Regions SET Mobcount=? WHERE Name=?''', (mobcount, regionname))
                c.execute('''UPDATE RoomMobs SET Slot1=? WHERE ID=?''', (id0, room))
                conn.commit()
                spawn -= 1
            else:
                if test[2] in ('', None, 'dead'):
                    size = 6
                    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
                    id0 = ''.join(random.choice(chars) for x in range(size))
                    mon = random.choice(self.NoobieForestMobs)
                    self.CreateMob(id0, mon, room)
                    # print "Created Mob,", self.name, "in room,", room, "in slot2"
                    c.execute('''SELECT * FROM Regions WHERE Name=?''', regionname)
                    mobcount = c.fetchone()
                    mobcount = mobcount[1]
                    mobcount = int(mobcount) + 1
                    mobcount = str(mobcount)
                    regionname = 'NoobieForest'
                    c.execute('''UPDATE Regions SET Mobcount=? WHERE Name=?''', (mobcount, regionname))
                    c.execute('''UPDATE RoomMobs SET Slot2=? WHERE ID=?''', (id0, room))
                    conn.commit()
                    spawn -= 1
                else:
                    if test[3] in ('', None, 'dead'):
                        size = 6
                        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
                        id0 = ''.join(random.choice(chars) for x in range(size))
                        mon = random.choice(self.NoobieForestMobs)
                        self.CreateMob(id0, mon, room)
                        # print "Created Mob,", self.name, "in room,", room, "in slot3"
                        c.execute('''SELECT * FROM Regions WHERE Name=?''', regionname)
                        mobcount = c.fetchone()
                        mobcount = mobcount[1]
                        mobcount = int(mobcount) + 1
                        mobcount = str(mobcount)
                        regionname = 'NoobieForest'
                        c.execute('''UPDATE Regions SET Mobcount=? WHERE Name=?''', (mobcount, regionname))
                        c.execute('''UPDATE RoomMobs SET Slot3=? WHERE ID=?''', (id0, room))
                        conn.commit()
                        spawn -= 1
                    else:
                        pass


class MobFight():

    def __init__(self, rand):
        global c
        self.id = rand
        mob = (rand,)
        c.execute('SELECT * FROM ActiveMonster WHERE RandomID=?', mob)
        result = c.fetchone()
        self.room = result[16]
        self.Fight()

    def Fight():
        global c
        slot = target
        slot = int(slot)
        room = (self.room,)
        c.execute('SELECT * FROM RoomMobs WHERE ID=?', room)
        test= c.fetchone()
        mob = test[slot]
        if mob in('', None):
            self.sendLine("Creature doesn't exist!")
            return
        mobs = (mob,)
        c.execute('SELECT * FROM ActiveMonster WHERE RandomID=?', mobs)
        test = c.fetchone()
        name = str(test[3])
        # RandomID, MobID, Level, Name, Health, MaxHealth, Mana, MaxMana, Attack, Defence, Speed, Critical, Accuracy, 13Dodge, Mattack, Mdefence
        if test is None:
            self.sendLine("Attack failed : User not Found")
        else:
            if self.attackready is True:
                hitmax = 100 + int(test[13])
                hit = random.randint(1, hitmax)
                crit = random.randint(1, 100)
                attackmin = self.mainhandvalmin
                attackmax = self.mainhandvalmax
                Critical = False
                if(self.offhandtype == 'Weapon'):
                    offhandmin = self.offhandvalmin * 0.75
                    offhandmin = int(offhandmin)
                    offhandmax = self.offhandvalmax * 0.75
                    offhandmax = int(offhandmax)
                    attackmin = self.mainhandvalmin + offhandmin
                    attackmax = self.mainhandvalmax + offhandmax
                attack = random.randint(attackmin, attackmax) + self.strengthdamage
                if(hit <= self.accuracy):
                    af = float(self.attack)
                    attackmod = af / int(test[9])
                    attack = float(attack)
                    attack = attackmod * attack
                    if crit <= self.critical:
                        attack = attack * 2
                        Critical = True
                    attack = int(attack)
                    mobhp = int(test[4])
                    mobhp = mobhp - attack
                    mob = unicode(mob)
                    c.execute('UPDATE ActiveMonster SET Health=? WHERE RandomID=?', (mobhp, mob))
                    if(int(test[4]) <= 0): # Mob health < 0 Check
                        self.handle_MOBDEATH(test[0], test[2], target)
                        self.sendLine("You have slain the %s" % (name))
                    else:
                        if Critical is True:
                            self.sendLine("You critically hit the %s for %s damage!" % (name, attack))
                        else:
                            self.sendLine("You hit the %s for %s damage!" % (name, attack))
                        self.attackready = False
                        reactor.callLater(self.attackspeed, self.handle_ATTACKWAIT)
                else:
                    self.sendLine("You ***MISSED*** the %s!" % (name))
                    self.attackready = False
                    reactor.callLater(self.attackspeed, self.handle_ATTACKWAIT)
            else:
                self.sendLine("You need to wait a little bit longer before attacking")
            conn.commit()


#size = 6
#chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
#id0 = ''.join(random.choice(chars) for x in range(size))
#mobspawner = {id0: task.LoopingCall(MobSpawner)}
#a = mobspawner.get(id0)
#a.start(10.0)
l = task.LoopingCall(MobSpawner)
l.start(30.0)
#k = task.LoopingCall(MobKill)
#k.start(12.0)
print "Server Started at localhost on Port : 8123"
reactor.listenTCP(8123, ChatFactory())
reactor.run()
c.close()