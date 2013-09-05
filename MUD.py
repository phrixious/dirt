from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import random
import sqlite3

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
        self.pk = 0
        self.room = 1
        self.classname = ''
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
        self.party = {}

    def connectionMade(self):
        self.sendLine("Username :")
        self.state = "LOGINCHECK"

    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            message = "%s has disconnected" % (self.name)
            print message
            for name, protocol in self.users.iteritems():
                protocol.sendLine(message)
            del self.users[self.name]

    def LOAD(self):
        global c
        t = self.name
        t = (t,)
        c.execute('SELECT * FROM Placement WHERE Name=?', t)
        test = c.fetchone()
        if(test == None):
            print self.name, "has no room placing in spawn..."
            self.state = "Room1"
        if(test != None):
            print self.name, "has logged in at room", self.room
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
            #Name, Level, Exp, Exptnl, Strength, Constitution, Dexterity, Agility, Wisdom, Intellegence
            self.level = test[1]
            self.exp = test[2]
            self.exptnl = test[3]
            self.strength = test[4]
            self.constitution = test[5]
            self.dexterity = test[6]
            self.agility = test[7]
            self.wisdom = test[8]
            self.intellegence = test[9]
            c.execute('SELECT * FROM Vitals WHERE Name=?', t)
            test = c.fetchone()
            if(test == None):
                print self.name, "has no vitals"
                print "This should have been caught in the character process... creating character now"
                self.handle_CLEARSCREEN
                self.sendLine("***WARNING*** Do not leave during this process! it won't take long!")
                self.CLASSLIST()
                self.state = "PSTART"
                return
            if(test != None):
                #Name, Health, MaxHealth, HealthRegen, Mana, MaxMana, ManaRegen
                self.health = test[1]
                self.maxhealth = test[2]
                self.healthregen = test[3]
                self.mana = test[4]
                self.maxmana = test[5]
                self.manaregen = test[6]
                print self.name, "is loaded and logged in"
                self.sendLine("Character Successfully Loaded")
                self.sendLine("Loading Equipment...")
                # Name, Mainhand, Offhand, Helmet, Body, Lowerbody, Boots

    def SAVE(self):
        global c
        r = self.room
        t = self.name
        t = (r,t,)
        try:
            c.execute('UPDATE Placement SET Room=? WHERE Name=?', t)
            try:
                c.execute('UPDATE Character SET Level=? Exp=? Exptnl=? Strength=? Constitution=? Dexterity=? Agility=? Wisdom=? Intellegence=? WHERE Name=?', t)
                try:
                    c.execute('UPDATE Vitals SET Health=? MaxHealth=? HealthRegen=? Mana=? MaxMana=? ManaRegen=? WHERE Name=?', t)
                except:
                    print 'Vitals save failed for', self.name
            except:
                print "Character save failed for", self.name
        except:
            print "Room save failed for", self.name

    def lineReceived(self, line):
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
            print "Created User  :", self.name
            print "With Password : **********"
            ID = (self.name, self.password,)
            c.execute('INSERT INTO ID Values (?,?)', ID)
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

    def handle_LOGINCHECK(self, name):
        global c
        if self.users.has_key(name):  # lint:ok
            self.sendLine("User is already logged in...")
            self.sendLine("Please try another name...")
        else:
            t = str(name)
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
        print t
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
            self.sendLine("Login failed... try again")
            self.handle_CLEARSCREEN()
            self.sendLine("Username :")
            self.state = "LOGINCHECK"

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
                defence = defence + self.defence
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
        self.sendLine("Class :  %s" % (self.classname))
        self.sendLine("Exp :    %-5s" % (self.exp))
        self.sendLine("ExpTNL : %-5s" % (self.exptnl))
        self.sendLine("================================")
        self.sendLine("HP : %3s / %3s" % (self.health, self.maxhealth))
        self.sendLine("Health Regen : %2s" % (self.healthregen))
        self.sendLine("MP : %3s / %3s" % (self.mana, self.maxmana))
        self.sendLine("Mana Regen   : %2s" % (self.manaregen))
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
            self.room = 1
            self.state = "Room"
            self.handle_CLEARSCREEN()
            self.sendLine("Welcome %s to the world of Arr'Fia" % (self.name))
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

    def handle_ROOM(self):
        global c

#    def RoomCreate(self, room):

    def handle_CHARACTERLOOKUP(self, name):
        diction = self.users
        person = str(name)
        char = diction.get(person)
        if char != None:
            self.sendLine("================================")
            self.sendLine("Name  : %s" % (char.name))
            self.sendLine("Class : %s" % (char.classname))
            self.sendLine("Level : %s" % (char.level))
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
        for name, protocol in self.users.iteritems():
            if protocol != self:
                message = "%s has joined" % (self.name,)
                protocol.sendLine(message)
        self.state = "CHAT"

    def handle_DEATH(self, atk):
        atk.health = atk.maxhealth
        self.pk += 1
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

    def handle_GETNAME(self, name):
        if self.users.has_key(name):  # lint:ok
            self.sendLine("User is already logged in...")
            return
        else:
            self.name = name
            self.handle_WELCOME(name)

    def handle_CHAT(self, message):
        if(message == '/help'):
            self.sendLine("The commands available to you are...")
            self.sendLine("/a <user>         *Attack another user")
            self.sendLine("/c                *Return back to command mode")
            self.sendLine("/clear            *clears the screen of text")
            self.sendLine("/equip            *Looks up personal gear equipped")
            self.sendLine("/lookup <user>    *Looks up a users stats")
            self.sendLine("/s                *Locks say chat mode. (use /c to return)")
            self.sendLine("/say <message>    *Talks to other users")
            self.sendLine("/stats            *Looks up your own stats")
            self.sendLine("/suicide          *Commits suicide")
            self.sendLine("/w <user>         *Enter private chat mode")
            return
        if(message == '/stats'):
            try:
                self.STATS()
                return
            except:
                self.sendLine("Something didn't work... Please report it'")
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
        if(message == '/equip'):
#            try:
            self.handle_EQUIP()
#            except:
#                print "Equip not working"
            return
        if(message == '/clear'):
            try:
                self.handle_CLEARSCREEN()
            except:
                print "Clear not working"
            return
        if(message[0:7] == '/attack'):
            attack = message[8:]
            if attack in(None, ''):
                self.handle_ATTACKINIT()
            else:
                self.handle_ATTACK(attack)
            return
        if(message == '/suicide'):
            try:
                self.handle_SUICIDE()
            except:
                print "Suicide Failed"
            return
        if(message[0:2] == '/a'):
            attack = message[3:]
            if attack in(None, ''):
                self.handle_ATTACKINIT()
            else:
                self.handle_ATTACK(attack)
            return
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
        if(message[0:2] == '/w'):
            check = message[3:]
            if check in(None, ''):
                self.state = "WHISP"
                self.sendLine("Who would you like to private chat with?")
            else:
                self.handle_WHISP_ini(check)
            return

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

    def handle_ATTACK(self, target):
        diction = self.users
        if target == self.name:
            self.sendLine("You cannot attack yourself... Do you want /suicide?")
            return
        target = str(target)
        atk = diction.get(target)
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

    def handle_SAY(self, message):
        if(message == '/c'):
            self.state = "CHAT"
            self.sendLine("You have left chat mode : SAY")
        else:
            message = "<%s> %s" % (self.name, message)
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

class ChatFactory(Factory):

    def __init__(self):
        self.users = {}  # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)

reactor.listenTCP(8123, ChatFactory())
reactor.run()
c.close()