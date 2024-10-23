import threading
import time
from datetime import datetime
import datetime

from Utilities.birthdayReminderSystem import sendBirthdayReminders
from Utilities.sqlQueries import sqlQuery


#Class to check for birthdays in 3 days and 24 hours
class checking4Birthdays():
    def __init__(self, table, cursor):
        self.table = table
        self.cursor = cursor
        self.checkInterval = 1800

    def start(self) -> None:
        #Starting the background thread
        thread = threading.Thread(target = self.checkBirthdays)
        thread.daemon = True  #Daemon thread will automatically close when the main program exits
        thread.start()

    def checkBirthdays(self) -> None:
        while True:
            self.sendBdayReminders()
            #Waiting for the next check (check every hour)
            time.sleep(self.checkInterval)

    def sendBdayReminders(self) -> None:
        try:
            #Query to get reminder settings (email, windows notification, etc.)
            self.cursor.execute('SELECT emailReminder, windowsNoti, hours24 FROM reminderSettings WHERE id = 1')
            data = self.cursor.fetchall()
            if len(data) == 0:
                return
            else:
                emailReminder, windowsNoti, hours24 = data[0]
                userEmail = sqlQuery(self.table, self.cursor).getEmailProfile()
                userName = sqlQuery(self.table, self.cursor).getNameSurnameProfile()
                self.cursor.execute('SELECT name, birthday, notes FROM bdays')
                birthdays = self.cursor.fetchall()
                if not emailReminder and not windowsNoti:
                    return
                else:
                    today = datetime.datetime.now()
                    for name, birthday, notes in birthdays:
                        day, month, year = birthday.split('-')
                        bdayDate = datetime.datetime.strptime(birthday, "%d-%m-%Y").replace(year = datetime.datetime.now().year)
                        if bdayDate is None:
                            continue
                        else:
                            daysLeft = (bdayDate.day - today.day)
                            if daysLeft == 3:
                                if emailReminder and userEmail:
                                    #Send an email reminder 3 days before the birthday
                                    sendBirthdayReminders().sendEmailNotification(userEmail, name, bdayDate, '3days', notes or "")
                                if windowsNoti:
                                    #If emailReminder is off, but Windows notifications are on, send Windows notification
                                    sendBirthdayReminders().sendWindowsNotificationReminder(name, 3)
                            elif daysLeft == 1:
                                if hours24:
                                    if emailReminder:
                                        #Send a reminder 24 hours before the birthday
                                        sendBirthdayReminders().sendEmailNotification(userEmail, name, bdayDate, '24hours', notes or "")
                                    if windowsNoti:
                                        #Send Windows notification instead of email if email reminders are off
                                        sendBirthdayReminders().sendWindowsNotificationReminder(name, 1)
                            elif daysLeft == 0:
                                if emailReminder:
                                    sendBirthdayReminders().sendEmailNotification(userEmail, name, bdayDate, '24hours', notes or "")
                                if windowsNoti:
                                    sendBirthdayReminders().sendWindowsNotificationReminder(name, 0)
        except Exception as e:
            print(e)