#CustomTkinter is a python UI-library based on Tkinter, which provides new, modern and fully customizable widgets.
import customtkinter
#Importing the sqlQuery class for database queries
from Utilities.sqlQueries import sqlQuery

class reminderFrame():
    def __init__(self, master, table, cursor):
        self.master = master
        self.table = table
        self.cursor = cursor
        #Setting the reminder frame and loading it up when called
        self.reminderBackgroundFrame = customtkinter.CTkFrame(master = self.master, width = 197, height = 450, border_color = "#313E41", border_width = 3)
        self.reminderBackgroundFrame.place(x = 761, y = 78)
        #Making the frame the only widget interactable
        self.reminderBackgroundFrame.grab_set()
        #Setting up the labels ontop the frame
        self.reminderFrameTitle = customtkinter.CTkLabel(master = self.reminderBackgroundFrame, text = "Reminder Settings", width = 177, height = 33, font = ("Inter", 20, "bold"))
        self.reminderFrameTitle.place(x = 10, y = 16)
        self.emailSwitch = customtkinter.CTkSwitch(master = self.reminderBackgroundFrame, width = 79, height = 35, text = "Email Reminders", font = ("Inter", 13, "bold"), onvalue = True, offvalue = False)
        self.emailSwitch.place(x = 15, y = 60)
        self.notificationSwitch = customtkinter.CTkSwitch(master = self.reminderBackgroundFrame, width = 79, height = 35, text = "Windows Notifications", font = ("Inter", 13, "bold"), onvalue = True, offvalue = False)
        self.notificationSwitch.place(x = 15, y = 112)
        self.remindMe24HoursBefore = customtkinter.CTkSwitch(master = self.reminderBackgroundFrame, width = 79, height = 35, text = "Remind me 24 hours \nbefore birthday", font = ("Inter", 13, "bold"), onvalue = True, offvalue = False)
        self.remindMe24HoursBefore.place(x = 15, y = 164)
        #Depending on the data stored in the database (enabling or disabling the switch according to the users settings)
        emailValue = sqlQuery(self.table, self.cursor).getEmailNoti()
        notificationValue = sqlQuery(self.table, self.cursor).getWindowsNoti()
        reminder24HoursValue = sqlQuery(self.table, self.cursor).getHours24()
        if emailValue == 1: self.emailSwitch.select()
        if notificationValue == 1: self.notificationSwitch.select()
        if reminder24HoursValue == 1: self.remindMe24HoursBefore.select()
        #Creating the close/save buttons and placing on the frame
        closeProfile = customtkinter.CTkButton(master = self.reminderBackgroundFrame, width = 76, height = 35, text = "Close", font = ("Open Sans", 13, "bold"), fg_color = "#F03131", command = self.closeReminderSettingsFrame)
        closeProfile.place(x = 15, y = 396)
        saveProfile = customtkinter.CTkButton(master = self.reminderBackgroundFrame, width  = 76, height = 35, text = "Save", font = ("Open Sans", 13, "bold"), fg_color = "#2FD82F", command = self.saveReminderSettingsFrame)
        saveProfile.place(x = 106, y = 396)

    def saveReminderSettingsFrame(self) -> None:
        emailValue = self.emailSwitch.get()
        notificationValue = self.notificationSwitch.get()
        reminder24HoursValue = self.remindMe24HoursBefore.get()
        query = """
        INSERT INTO reminderSettings (id, emailReminder, windowsNoti, hours24)
        VALUES (1, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            emailReminder = COALESCE(excluded.emailReminder, reminderSettings.emailReminder),
            windowsNoti = COALESCE(excluded.windowsNoti, reminderSettings.windowsNoti),
            hours24 = COALESCE(excluded.hours24, reminderSettings.hours24);
        """
        self.cursor.execute(query, (emailValue, notificationValue, reminder24HoursValue))
        self.table.commit()
        self.reminderBackgroundFrame.destroy()

    def closeReminderSettingsFrame(self) -> None:
        self.reminderBackgroundFrame.destroy()