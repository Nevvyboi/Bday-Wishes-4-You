
#Creating a class with all the sql queries needed
class sqlQuery():
    def __init__(self, table, cursor) -> None:
        self.table = table
        self.cursor = cursor
    ####################Table####################
    def createTable(self) -> None:
        self.cursor.execute("CREATE TABLE IF NOT EXISTS bdays (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, birthday TEXT, pfp BLOB, notes TEXT);")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS profile (nameSurname TEXT, bday TEXT, pfp BLOB, email TEXT, theme TEXT, mode TEXT, id INTEGER PRIMARY KEY CHECK (id = 1))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS reminderSettings (emailReminder NUMERIC, windowsNoti NUMERIC, hours24 NUMERIC, id INTEGER PRIMARY KEY CHECK (id = 1))")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sentNotifications (name TEXT, reminderType TEXT, sentDate DATE)")
        self.table.commit()
    ####################BirthdayChecks####################
    def hasNotificationBeenSent(self, name : str, reminderType : str, sentDate : str) -> bool:
        self.cursor.execute("SELECT 1 FROM sentNotifications WHERE name = ? AND reminderType = ? AND sentDate = ?", (name, reminderType, sentDate))
        return self.cursor.fetchone() is not None

    def recordNotification(self, name : str, reminderType : str, sentDate : str) -> None:
        self.cursor.execute("INSERT INTO sentNotifications (name, reminderType, sentDate) VALUES (?, ?, ?)", (name, reminderType, sentDate))
        self.table.commit()
    ####################Profile####################
    def getAvatarProfile(self) -> bytes:
        self.cursor.execute('SELECT pfp FROM profile WHERE id = 1')
        avatarBytes = self.cursor.fetchone()
        if avatarBytes:
            return avatarBytes[0]
        else:
            return None

    def getNameSurnameProfile(self) -> None | str:
        #Fetching the name stored in the database (profile)
        self.cursor.execute('SELECT nameSurname FROM profile WHERE id = 1')
        nameSurname = self.cursor.fetchone()
        if nameSurname is None:
            return None
        else:
            return nameSurname[0]

    def getBdayProfile(self) -> None | str:
        #Fetching birthday (profile)
        self.cursor.execute('SELECT bday FROM profile WHERE id = 1')
        bday = self.cursor.fetchone()
        if bday is None:
            return None
        else:
            return bday[0]

    def getEmailProfile(self) -> None | str:
        #Fetching email (profile)
        self.cursor.execute('SELECT email FROM profile WHERE id = 1')
        email = self.cursor.fetchone()
        if email is None:
            return None
        else:
            return email[0]

    def getThemeProfile(self) -> None | str:
        #Fetching email (profile)
        self.cursor.execute('SELECT theme FROM profile WHERE id = 1')
        theme = self.cursor.fetchone()
        if theme is None:
            return None
        else:
            return theme[0]

    def setThemeProfile(self, theme : str) -> None | str:
        #Storing the current theme into the database
        self.cursor.execute("""
            INSERT INTO profile (id, theme) VALUES (1, ?)
            ON CONFLICT(id) DO UPDATE SET theme = excluded.theme
        """, (theme,))
        self.table.commit()

    def getModeProfile(self) -> None | str:
        #Fetching email (profile)
        self.cursor.execute('SELECT mode FROM profile WHERE id = 1')
        mode = self.cursor.fetchone()
        if mode is None:
            return None
        else:
            return mode[0]

    def setSaveProfile(self, nameSurname : str, bdayDate : str, image : bytes, email : str) -> None | str:
        query = """
        INSERT INTO profile (nameSurname, bday, pfp, email, id)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            pfp = excluded.pfp,
            nameSurname = excluded.nameSurname,
            bday = excluded.bday,
            email = excluded.email;
        """
        self.cursor.execute(query, (nameSurname, bdayDate, image, email, 1))
        self.table.commit()

    def setSaveBdayCard(self, nameBday : str, birthdayBday : str, imageBday : bytes, notesBday : str) -> None:
        query = """
        INSERT INTO bdays (name, birthday, pfp, notes)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            birthday = CASE 
                WHEN excluded.birthday IS NOT NULL AND excluded.birthday != '' 
                THEN excluded.birthday 
                ELSE bdays.birthday 
            END,
            pfp = CASE 
                WHEN excluded.pfp IS NOT NULL AND excluded.pfp != '' 
                THEN excluded.pfp 
                ELSE bdays.pfp 
            END,
            notes = CASE 
                WHEN excluded.notes IS NOT NULL AND excluded.notes != '' 
                THEN excluded.notes 
                ELSE bdays.notes 
            END;
        """
        self.cursor.execute(query, (nameBday, birthdayBday, imageBday, notesBday))
        self.table.commit()

    def setModeProfile(self, modeLightOrDark : str) -> None:
        #Storing the current mode into the database
        self.cursor.execute("""
            INSERT INTO profile (id, mode) VALUES (1, ?)
            ON CONFLICT(id) DO UPDATE SET mode = excluded.mode
        """, (modeLightOrDark,))
        self.table.commit()
    ####################Birthdays####################
    def getBirthdays(self) -> None | list:
        #Fetching birthdays
        self.cursor.execute("SELECT * FROM bdays")
        birthdays = self.cursor.fetchall()
        if birthdays is None:
            return None
        else:
            return [bdays for bdays in birthdays]

    def deleteBirthday(self, name) -> None:
        self.cursor.execute("DELETE FROM bdays WHERE name = ?", (name,))
        self.table.commit()
    ####################Reminders####################
    def getEmailNoti(self) -> None | int:
        #Fetching email notification setting
        self.cursor.execute("SELECT emailReminder FROM reminderSettings WHERE id = 1")
        emailReminder = self.cursor.fetchone()
        if emailReminder is None:
            return None
        else:
            return emailReminder[0]

    def getWindowsNoti(self) -> None | int:
        #Fetching windows notification setting
        self.cursor.execute('SELECT windowsNoti FROM reminderSettings WHERE id = 1')
        windowsNoti = self.cursor.fetchone()
        if windowsNoti is None:
            return None
        else:
            return windowsNoti[0]

    def getDays3(self) -> None | int:
        #Fetching 3 days notification setting
        self.cursor.execute('SELECT days3 FROM reminderSettings WHERE id = 1')
        days3 = self.cursor.fetchone()
        if days3 is None:
            return None
        else:
            return days3[0]

    def getHours24(self) -> None | int:
        #Fetching 24 hours notification setting
        self.cursor.execute('SELECT hours24 FROM reminderSettings WHERE id = 1')
        hours24 = self.cursor.fetchone()
        if hours24 is None:
            return None
        else:
            return hours24[0]