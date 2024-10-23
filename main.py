#CustomTkinter is a python UI-library based on Tkinter, which provides new, modern and fully customizable widgets.
import customtkinter
#Using pystray in order ot create a system tray icon
import pystray
from pystray import Icon as icon, Menu as menu, MenuItem as item
#Importing threading to use for the icon tray and backround tasks
import threading
#Importing webserver package to direct user to the website using their defualt web browswer
import webbrowser

def setupTrayIcon() -> None:
    #Icon tray image
    iconBirthdayWishes = imageLoadingAndCreator().birthdayWishesLogoTrayIcon
    # Create a Pystray icon with a menu
    def iconTrayClickOpen(icon, item) -> None:
        app.popUpWindowIconTray()

    def show_notification(icon, item):
        icon.notify("Birthday Reminder", "It's time to send birthday wishes!")

    # Function to remove the notification
    def remove_notification(icon, item):
        icon.remove_notification()

    menu = pystray.Menu(
        item("Open", iconTrayClickOpen)
    )

    icon = pystray.Icon("Birthday Wishes", iconBirthdayWishes, menu = menu)
    icon.title = "Birthday Wishes"
    # Run the icon (this will run in a separate thread)
    icon.run()

import os, sys
import io
import time
from datetime import datetime, timedelta
import sqlite3
from PIL import Image, ImageDraw

from Utilities.sqlQueries import sqlQuery
from Utilities.birthdayReminderSystem import sendBirthdayReminders
from Utilities.check4Birthdays import checking4Birthdays
from Utilities.colorPalette4Labels import colour4Widgets
from Utilities.imageLoader import imageLoadingAndCreator
from Utilities.reminderScreen import reminderFrame
from Utilities.profileScreen import profileFrame
from Utilities.birthdayScreen import addBirthdayFrame

class mainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Setting the icon of when defualt window is utilized
        self.iconbitmap(imageLoadingAndCreator().birthdayWishesIcon)
        #Disabling the default window; to enable app customization
        self.overrideredirect(True)
        self.openWindowCentreOfScreen(974, 543)
        self.xOffSet = None
        self.yOffSet = None
        #Creating database and intiating cursor
        self.table = sqlite3.connect("Database//bdays.db", check_same_thread = False)
        self.cursor = self.table.cursor()
        #Creating tables in the database
        sqlQuery(self.table, self.cursor).createTable()
        self.currentMode = sqlQuery(self.table, self.cursor).getModeProfile() or "dark"

        self.birthdayList = sqlQuery(self.table, self.cursor).getBirthdays()
        self.birthdayList = sorted(self.birthdayList , key = lambda bday : bday[1].lower())
        self.birthdayListFiltered = self.birthdayList.copy()
        #Setting the mode image in startup (light mode or dark mode)
        self.currentModeImage = None
        if self.currentMode == "dark":
            self.currentModeImage = imageLoadingAndCreator().darkModeIcon
            customtkinter.set_appearance_mode("dark")
        elif self.currentMode == "light":
            self.currentModeImage = imageLoadingAndCreator().lightModeIcon
            customtkinter.set_appearance_mode("light")
        #Getting the theme set to load during startup (default breeze)
        self.theme = sqlQuery(self.table, self.cursor).getThemeProfile() or "breeze"
        if self.theme == "breeze":
            customtkinter.set_default_color_theme("Themes//breeze.json")
        elif self.theme == "autumn":
            customtkinter.set_default_color_theme("Themes//autumn.json")
        elif self.theme == "cherry":
            customtkinter.set_default_color_theme("Themes//cherry.json")
        elif self.theme == "coffee":
            customtkinter.set_default_color_theme("Themes//coffee.json")
        elif self.theme == "lavender":
            customtkinter.set_default_color_theme("Themes//lavender.json")
        elif self.theme == "marsh":
            customtkinter.set_default_color_theme("Themes//marsh.json")
        self.awaitingThemeSelection = None
        #Getting the users avatar from the database if not None
        self.userAvatar = self.bytesToImage(sqlQuery(self.table, self.cursor).getAvatarProfile(), (100, 100))
        #Loading up the widgets for the main window
        self.setupMainWindow()

    def setupMainWindow(self) -> None:
        #Setting the label which will act as the background image
        backgroundImageLabel = customtkinter.CTkLabel(self, text = "", fg_color = "transparent")
        backgroundImageLabel.pack(fill = "both", expand = True)
        backgroundImageLabel.bind("<Button-1>", self.startMovingWindow)
        backgroundImageLabel.bind("<B1-Motion>", self.dragWindow)

        topLeftBarFrame = customtkinter.CTkFrame(backgroundImageLabel, width = 177, height = 321)
        topLeftBarFrame.place(x = 15, y = 15)
        bottomLeftBarFrame = customtkinter.CTkFrame(backgroundImageLabel, width = 177, height = 177)
        bottomLeftBarFrame.place(x = 15, y = 351)
        middleTopLeftBarFrame = customtkinter.CTkFrame(backgroundImageLabel, width = 322, height = 47)
        middleTopLeftBarFrame.place(x = 207, y = 15)
        middleTopRightBarFrame = customtkinter.CTkFrame(backgroundImageLabel, width = 46, height = 47)
        middleTopRightBarFrame.place(x = 695, y = 15)
        self.middleBottomBarFrameScrollable = customtkinter.CTkScrollableFrame(backgroundImageLabel, width = 510, height = 437)
        self.middleBottomBarFrameScrollable.place(x = 207, y = 78)
        topRightLeftBarFrame = customtkinter.CTkFrame(backgroundImageLabel, width = 140, height = 47)
        topRightLeftBarFrame.place(x = 542, y = 15)
        topRightRightBarFrame = customtkinter.CTkFrame(backgroundImageLabel, width = 46, height = 47)
        topRightRightBarFrame.place(x = 912, y = 15)
        topRightBarFrame = customtkinter.CTkFrame(backgroundImageLabel, width = 197, height = 300)
        topRightBarFrame.place(x = 761, y = 78)
        bottomRightBarFrame = customtkinter.CTkFrame(backgroundImageLabel, width = 197, height = 136)
        bottomRightBarFrame.place(x = 761, y = 392)
        themeFrameTopRight = customtkinter.CTkFrame(backgroundImageLabel, width = 140, height = 47)
        themeFrameTopRight.place(x = 761, y = 15)

        #Adding the title of the application and logo
        topLeftFrameTitle = customtkinter.CTkLabel(master = topLeftBarFrame, text = "Birthday Wishes", width = 148, height = 38, justify = "center", font = ( "Inter", 20, "bold"))
        topLeftFrameTitle.place(x = 12, y = 16)
        topLeftFrameImage = customtkinter.CTkLabel(master = topLeftBarFrame, text = "", image = imageLoadingAndCreator().birthdayWishesLogo)
        topLeftFrameImage.place(x = 38, y = 57)

        #Adding label to close the window
        self.closeWindowImageLabel = customtkinter.CTkLabel(topRightRightBarFrame, image = imageLoadingAndCreator().closeWindowBlackImage, text = "")
        self.closeWindowImageLabel.place(x = 2, y = 2)
        self.closeWindowImageLabel.bind("<Enter>", self.closeButtonStartHover)
        self.closeWindowImageLabel.bind("<Leave>", self.closeButtonStopHover)
        self.closeWindowImageLabel.bind("<Button-1>", self.minimizeWindowWhenCloseIconPressed)

        #Adding a search bar
        self.middleTopLeftSearchBar = customtkinter.CTkEntry(master = middleTopLeftBarFrame, placeholder_text = "Search Birthday", width = 313, height = 37)
        self.middleTopLeftSearchBar.place(x = 5, y = 5)
        self.middleTopLeftSearchBar.bind("<KeyRelease>", self.textBoxSearchOperations)

        #Dark/Light mode label and functionality
        self.middleTopRightDarkLightMode = customtkinter.CTkLabel(master = middleTopRightBarFrame, image = self.currentModeImage, text = "")
        self.middleTopRightDarkLightMode.place(x = 5, y = 5.5)
        self.middleTopRightDarkLightMode.bind("<Enter>", self.darkLightButtonStartHover)
        self.middleTopRightDarkLightMode.bind("<Leave>", self.darkLightButtonStopHover)
        self.middleTopRightDarkLightMode.bind("<Button-1>", self.darkLightButtonPressed)

        #Adding Buttons to the Top Left Bar
        topLeftBarAddBirthdayButton = customtkinter.CTkButton(master = topLeftBarFrame, text = "Add Birthday", width = 154, height = 35, font = ("Open Sans", 13, "bold"), command = self.createBirthday)
        topLeftBarAddBirthdayButton.place(x = 11, y = 174)
        topLeftBarViewAllBirthdaysButton = customtkinter.CTkButton(master = topLeftBarFrame, text = "View All Birthdays", width = 154, height = 35, font = ("Open Sans", 13, "bold"), command = self.viewBirthdays)
        topLeftBarViewAllBirthdaysButton.place(x = 11, y = 221)
        UpcomingBirthdaysOptionMenuPlacementText = customtkinter.StringVar(value = "Upcoming Bdays")
        topLeftBarUpcomingBirthdaysOptionMenu = customtkinter.CTkOptionMenu(master = topLeftBarFrame, values = ["In One Day", "In Three Days", "In Seven Days"], width = 154, height = 35, font = ("Open Sans", 13, "bold"), variable = UpcomingBirthdaysOptionMenuPlacementText, dropdown_font = ("Open Sans", 13, "bold"), command = self.optionMenuOptionSelected, dropdown_fg_color = colour4Widgets().findColour(self.theme))
        topLeftBarUpcomingBirthdaysOptionMenu.place(x = 11, y = 268)

        #Profile picture customization
        self.topProfilePictureMainWindow = customtkinter.CTkLabel(master = topRightBarFrame, width = 100, height = 100, text = "", image = self.userAvatar or imageLoadingAndCreator().emptyPfp)
        self.topProfilePictureMainWindow.place(x = 49, y = 21)

        #Top Right Button (Profile Customization)
        self.customizeName = customtkinter.CTkLabel(master = topRightBarFrame, text = sqlQuery(self.table, self.cursor).getNameSurnameProfile() or "", width = 167, height = 35, fg_color = colour4Widgets().findColour(self.theme), font = ('Inter', 16, "bold"), corner_radius = 5)
        self.customizeName.place(x = 12, y = 134)
        self.customizeBirthdayDay = customtkinter.CTkLabel(master = topRightBarFrame, text = sqlQuery(self.table, self.cursor).getBdayProfile() or "", width = 167, height = 35, fg_color = colour4Widgets().findColour(self.theme), font = ('Inter', 18, "bold"), corner_radius = 5)
        self.customizeBirthdayDay.place(x = 12, y= 183)
        self.timeTillUserBday = customtkinter.StringVar(value = "🎉")
        timeTillBdayProfile = customtkinter.CTkLabel(master = topRightBarFrame, textvariable = self.timeTillUserBday, width = 167, height = 50, fg_color = colour4Widgets().findColour(self.theme), font = ('Inter', 13, "bold"), corner_radius = 5, anchor = "center", wraplength = 165)
        timeTillBdayProfile.place(x = 12, y = 232)
        self.liveBdayTillBday()

        #Bottom Right Buttons (Additional Features)
        editProfileButton = customtkinter.CTkButton(master = bottomRightBarFrame, width = 167, height = 35, text = "Edit Profile", font = ("Open Sans", 16, "bold"), command  = self.editProfileButton)
        editProfileButton.place(x = 15, y = 25)
        reminderSettings = customtkinter.CTkButton(master = bottomRightBarFrame, width = 167, height = 35, text = "Reminder Settings", font = ("Open Sans", 16, "bold"), command = self.reminderSettingsButton)
        reminderSettings.place(x = 15, y = 78)

        #Top right Theme Button Choice
        chooseThemesOptionMenuPlacementText = customtkinter.StringVar(value = "Choose\nTheme")
        chooseThemesOptionMenu = customtkinter.CTkOptionMenu(master = themeFrameTopRight, command = self.selectingTheme, width = 125, height = 35, anchor = "center", font = ("Inter", 13, "bold"), variable = chooseThemesOptionMenuPlacementText, values = ["Autumn", "Breeze", "Cherry", "Coffee", "Lavender", "Marsh"], dropdown_font = ("Inter", 18, "bold"), dynamic_resizing = False, dropdown_fg_color = colour4Widgets().findColour(self.theme))
        chooseThemesOptionMenu.place(x = 7, y = 6)

        #Adding a live digital clock
        self.liveClock = customtkinter.StringVar(value = "")
        topRightLeftDigitalClock = customtkinter.CTkLabel(master = topRightLeftBarFrame, textvariable = self.liveClock, width = 117, height = 31, font = ("Open Sans", 30, "bold"))
        topRightLeftDigitalClock.place(x = 8, y = 3)
        self.liveDigitalClock()

        #Adding a support/report/suggestion feature
        self.supportCentreLabel = customtkinter.CTkLabel(master = bottomLeftBarFrame, text = "", image = imageLoadingAndCreator().supportCentre)
        self.supportCentreLabel.place(x = 66, y = 6)
        supportCentreTitle = customtkinter.CTkLabel(master = bottomLeftBarFrame, text = "Need Help?", font = ( "Inter", 16, "bold"), width = 116, height = 26)
        supportCentreTitle.place(x = 30, y = 50)
        supportCentreDescription = customtkinter.CTkLabel(master = bottomLeftBarFrame, text = "Reports Bugs?\nProvide Suggestions?\nContact Support?", width = 138, height = 38)
        supportCentreDescription.place(x = 19, y = 76)
        supportCentreButton = customtkinter.CTkButton(master = bottomLeftBarFrame, text = "Go To Help Centre", width = 154, height = 35, font = ("Open Sans", 13, "bold"), command = self.supportCentreButtonPressed)
        supportCentreButton.place(x = 11, y = 129)

        #Populating the frame with birthdays
        self.populateMiddleFrameWithBirthdays()

    def liveBdayTillBday(self) -> None:
        bday = sqlQuery(self.table, self.cursor).getBdayProfile()
        if bday is None or bday == "":
            self.timeTillUserBday.set("🎉")
        else:
            now = datetime.now()
            #Attempting to parse birthday, handle errors
            birthday = datetime.strptime(bday, "%d-%m-%Y").replace(year=now.year)
            if birthday < now:
                birthday = birthday.replace(year=now.year + 1)
            timeLeft = birthday - now
            # If it's the user's birthday today
            if birthday.day == now.day and birthday.month == now.month:
                self.timeTillUserBday.set("🎉 Happy Birthday! 🎉")
                seconds = self.secondsTillMidnight()
                self.after(int(seconds * 1000), self.liveBdayTillBday)
            else:
                # Calculate days, hours, minutes, and seconds remaining
                days, seconds = divmod(timeLeft.total_seconds(), 86400)
                hours, seconds = divmod(seconds, 3600)
                minutes, seconds = divmod(seconds, 60)
                # Update label based on time left
                if days > 0:
                    text = f"Bday in {int(days)} days, {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
                elif hours > 0:
                    text = f"Bday in {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"
                elif minutes > 0:
                    text = f"Bday in {int(minutes)} minutes, {int(seconds)} seconds"
                else:
                    text = f"Bday in {int(seconds)} seconds"
                self.timeTillUserBday.set(text)
                # Call after every second
                self.after(1000, self.liveBdayTillBday)

    def secondsTillMidnight(self) -> int:
        now = datetime.now()
        midnight = (now + timedelta(days = 1)).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        secondsleft2Midnight = (midnight - now).total_seconds()
        return secondsleft2Midnight

    def selectingTheme(self, choice) -> None:
        if self.theme == choice.lower():
            return self.dialogMessage("The selected theme is already active.", 14)
        elif choice.lower() == "autumn":
            self.awaitingThemeSelection = "autumn"
            return self.dialogMessageThemeSelection(f"Do you want to switch to the Autumn theme?", 14)
        elif choice.lower() == "cherry":
            self.awaitingThemeSelection = "cherry"
            return self.dialogMessageThemeSelection(f"Do you want to switch to the Cherry theme?", 14)
        elif choice.lower() == "coffee":
            self.awaitingThemeSelection = "coffee"
            return self.dialogMessageThemeSelection(f"Do you want to switch to the Coffee theme?", 14)
        elif choice.lower() == "lavender":
            self.awaitingThemeSelection = "lavender"
            return self.dialogMessageThemeSelection(f"Do you want to switch to the Lavender theme?", 14)
        elif choice.lower() == "marsh":
            self.awaitingThemeSelection = "marsh"
            return self.dialogMessageThemeSelection(f"Do you want to switch to the Marsh theme?", 14)
        elif choice.lower() == "breeze":
            self.awaitingThemeSelection = "breeze"
            return self.dialogMessageThemeSelection(f"Do you want to switch to the Breeze theme?", 14)

    def dialogMessageThemeSelection(self, message : str, size : int) -> None:
        self.dialogOutputThemeMessage = customtkinter.CTkFrame(master = self, width = 209, height = 120, fg_color = colour4Widgets().findColour(self.theme), bg_color = "transparent", border_color = "#313E41", corner_radius = 0, border_width = 3)
        self.dialogOutputThemeMessage.place(x = 380, y = 190)
        self.dialogOutputThemeMessage.grab_set()
        dialogOutputThemeMessageLabel = customtkinter.CTkLabel(master = self.dialogOutputThemeMessage, width = 171, height = 41, font = ("Inter", size, "bold"), justify = customtkinter.LEFT, text = message, wraplength = 180)
        dialogOutputThemeMessageLabel.place(x = 17, y = 19)
        closeDialogOutputThemeMessage = customtkinter.CTkButton(master = self.dialogOutputThemeMessage, width = 81, height = 35, fg_color = "#F03131", text = 'Close', command = self.closeThemeSelectionMenu, text_color = "#000000", font = ("Inter", 13, "bold"))
        closeDialogOutputThemeMessage.place(x = 15, y = 74)
        restartSaveDialogOutputMessage = customtkinter.CTkButton(master = self.dialogOutputThemeMessage, width = 81, height = 35, fg_color = "#0FF040", text = 'Restart', command = self.saveRestartTheme, text_color = "#000000", font = ("Inter", 13, "bold"))
        restartSaveDialogOutputMessage.place(x = 116, y = 74)

    def saveRestartTheme(self) -> None:
        sqlQuery(self.table, self.cursor).setThemeProfile(self.awaitingThemeSelection)
        self.awaitingThemeSelection = None
        self.dialogOutputThemeMessage.destroy()
        self.destroy()
        python = sys.executable
        os.execl(python, python, *sys.argv)
        checking4Birthdays(app.table, app.cursor).start()

    def closeThemeSelectionMenu(self) -> None:
        self.awaitingThemeSelection = None
        self.dialogOutputThemeMessage.destroy()

    def optionMenuOptionSelected(self, choice) -> None:
        if choice == "In One Day":
            self.getUpcomingBirthday(1)
        elif choice == "In Three Days":
            self.getUpcomingBirthday(3)
        elif choice == "In Seven Days":
            self.getUpcomingBirthday(7)

    def getUpcomingBirthday(self, daysAheadOfToday: int) -> list:
        #Getting the current date
        currentDateRN = datetime.now()
        #Calculating the target date range
        dateToTarget = currentDateRN + timedelta(days = daysAheadOfToday)
        #Extract the day and month from the target date
        dayTarget = dateToTarget.day
        monthTarget = dateToTarget.month
        # Query to find matching birthdays
        self.cursor.execute("""
        SELECT * FROM bdays
        WHERE substr(birthday, 1, 2) = ?
        AND substr(birthday, 4, 2) = ?
        """, (f'{dayTarget:02}', f'{monthTarget:02}'))
        upComingBdays = self.cursor.fetchall()
        if upComingBdays:
            self.birthdayListFiltered = upComingBdays
            for widget in self.middleBottomBarFrameScrollable.winfo_children():
                widget.destroy()
            self.displayBirthdaysFiltered()
        else:
            return self.dialogMessage("No birthdays found in the next {} days.".format(daysAheadOfToday), 13)

    #Opening the reminder frame and place it ontop the main window
    def reminderSettingsButton(self) -> None:
        reminderFrame(self, self.table, self.cursor)

    #Opening the profile frame and place it ontop the main window
    def editProfileButton(self) -> None:
        profileFrame(self, self.table, self.cursor)

    #Opening the create birthday frame and place it ontop the main window
    def createBirthday(self) -> None:
        addBirthdayFrame(self, self.table, self.cursor)

    #Opening the support centre frame and place it ontop the main window
    def supportCentreButtonPressed(self) -> None:
        email_address = "birthday4uwishes@gmail.com"
        subject = "Hello from the Birthday Wishes App"
        body = "I would like to contact you regarding the app."
        gmailLink = f"https://mail.google.com/mail/?view=cm&fs=1&to={email_address}&su={subject}&body={body}"
        webbrowser.open(gmailLink)

    def bytesToImage(self, bytesToConvert : bytes | None, sizeOfImage : tuple[int, int]) -> None:
        if bytesToConvert is None:
            return None
        else:
            image = io.BytesIO(bytesToConvert)
            image = customtkinter.CTkImage(Image.open(image), size = sizeOfImage)
            return image

    def imageToBytes(self, image) -> bytes:
        if image is None:
            return None
        else:
            imageByteArray = io.BytesIO()
            image.save(imageByteArray, "PNG")
            return imageByteArray.getvalue()

    def textBoxSearchOperations(self, event) -> None:
        searchedText = self.middleTopLeftSearchBar.get().lower()
        self.birthdayListFiltered = [birthday for birthday in self.birthdayList if searchedText in birthday[1].lower()]
        for widget in self.middleBottomBarFrameScrollable.winfo_children():
            widget.destroy()
        self.displayBirthdaysFiltered()

    def displayBirthdaysFiltered(self) -> None:
        currentLetter = ""
        for birthday in self.birthdayListFiltered:
            firstLetter = birthday[1][0].upper()
            if firstLetter != currentLetter:
                currentLetter = firstLetter
                self.addBirthdayFrameSeperator(currentLetter)
            self.createBirthdayListObject(birthday[1], birthday[2], birthday[3], birthday[4] or None)

    def viewBirthdays(self) -> None:
        if len(self.birthdayList) == 0:
            return self.dialogMessage("No birthdays to view! Why dont you add your friends birthday's?", 12)
        currentLetter = ""
        for widget in self.middleBottomBarFrameScrollable.winfo_children():
            widget.destroy()
        for birthday in self.birthdayList:
            firstLetter = birthday[1][0].upper()
            if firstLetter != currentLetter:
                currentLetter = firstLetter
                self.addBirthdayFrameSeperator(currentLetter)
            self.createBirthdayListObject(birthday[1], birthday[2], birthday[3], birthday[4])

    def populateMiddleFrameWithBirthdays(self) -> None:
        currentLetter = ""
        for widget in self.middleBottomBarFrameScrollable.winfo_children():
            widget.destroy()
        for birthday in self.birthdayList:
            firstLetter = birthday[1][0].upper()
            if firstLetter != currentLetter:
                currentLetter = firstLetter
                self.addBirthdayFrameSeperator(currentLetter)
            self.createBirthdayListObject(birthday[1], birthday[2], birthday[3], birthday[4])

    def addBirthdayFrameSeperator(self, letter) -> None:
        separator = customtkinter.CTkLabel(master = self.middleBottomBarFrameScrollable, text = letter, font = ("Inter", 12, "bold"), width = 37, height = 10, fg_color = colour4Widgets().findColour(self.theme), corner_radius = 5)
        separator.pack(pady = 5, anchor = "w", padx = 10)

    def createBirthdayListObject(self, name : str, birthday : str, pfp : int, notes : str | None) -> None:
        birthdayObject = customtkinter.CTkFrame(master = self.middleBottomBarFrameScrollable, width = 491, height = 91, fg_color = colour4Widgets().findColour(self.theme), corner_radius = 15)
        profilePictureLabel = customtkinter.CTkLabel(master = birthdayObject, image = self.bytesToImage(pfp, (75, 75)), text = "", corner_radius = 20)
        profilePictureLabel.place(x = 3, y = 8)
        nameOfBirthdayObject = customtkinter.CTkLabel(master = birthdayObject, text = name.title(), width = 262, height = 19, fg_color = colour4Widgets().findColour(self.theme), font = ("Inter", 20), anchor = "w")
        nameOfBirthdayObject.place(x = 101, y = 8)
        bdayOfBirthdayObject = customtkinter.CTkLabel(master = birthdayObject, text = birthday, width = 100, height = 16, anchor = "w", font = ("Inter", 13, "bold"))
        bdayOfBirthdayObject.place(x = 101, y = 36)
        notesOfBirthdayObject = customtkinter.CTkLabel(master = birthdayObject, text = notes, width = 300, height = 20, anchor = "w")
        notesOfBirthdayObject.place(x = 101, y = 63)
        self.deleteBirthdayObject = customtkinter.CTkLabel(master = birthdayObject, text = "", image = imageLoadingAndCreator().resetPfpBdayCard)
        self.deleteBirthdayObject.place(x = 458, y = 8)
        self.deleteBirthdayObject.bind("<Button>", lambda event, frame = birthdayObject: self.deleteBdayObjectPressed(event, frame, name))
        self.deleteBirthdayObject.bind("<Enter>", lambda event, label = self.deleteBirthdayObject : self.deleteBdayObjectStartHover(event, label))
        self.deleteBirthdayObject.bind("<Leave>", lambda event, label = self.deleteBirthdayObject : self.deleteBdayObjectStopHover(event, label))
        birthdayObject.pack(pady = 5)

    def deleteBdayObjectPressed(self, event, frame, nameOfFrame) -> None:
        self.dialogConfirmationMessage = customtkinter.CTkFrame(master = self, width = 209, height = 120, fg_color = colour4Widgets().findColour(self.theme), bg_color = "transparent", border_color = "#313E41", corner_radius = 0, border_width = 3)
        self.dialogConfirmationMessage.place(x = 380, y = 190)
        self.dialogConfirmationMessage.grab_set()
        dialogOutputMessageLabel = customtkinter.CTkLabel(master = self.dialogConfirmationMessage, width = 171, height = 41, font = ("Inter", 11, "bold"), justify = customtkinter.LEFT, text = f"You're about to delete the birthday for {nameOfFrame}. Once deleted, this can't be undone. Do you want to proceed?", wraplength = 180)
        dialogOutputMessageLabel.place(x = 17, y = 10)
        closeDialogOutputMessage = customtkinter.CTkButton(master = self.dialogConfirmationMessage, width = 91, height = 35, fg_color = "#F03131", text = 'Close', command = self.closeDialogConfirmation, text_color = "#000000", font = ("Inter", 13, "bold"))
        closeDialogOutputMessage.place(x = 13, y = 74)
        saveProfile = customtkinter.CTkButton(master = self.dialogConfirmationMessage, command = lambda : self.confirmDialogConfirmation(nameOfFrame), width = 91 , height = 35, text = "Confirm", font = ("Open Sans", 13, "bold"), fg_color = "#2FD82F")
        saveProfile.place(x = 110, y = 74)

    def deleteBdayObjectStartHover(self, event, label) -> None:
        label.configure(image = imageLoadingAndCreator().resetPfpRedBdayCard)

    def deleteBdayObjectStopHover(self, event, label) -> None:
        label.configure(image = imageLoadingAndCreator().resetPfpBdayCard)

    def confirmDialogConfirmation(self, name : str) -> None:
        sqlQuery(self.table, self.cursor).deleteBirthday(name)
        self.birthdayList = sqlQuery(self.table, self.cursor).getBirthdays()
        self.populateMiddleFrameWithBirthdays()
        self.dialogConfirmationMessage.destroy()

    def closeDialogConfirmation(self) -> None:
        self.dialogConfirmationMessage.destroy()

    def dialogMessage(self, message : str, size : int) -> None:
        self.dialogOutputMessage = customtkinter.CTkFrame(master = self, width = 209, height = 120, fg_color = colour4Widgets().findColour(self.theme), bg_color = "transparent", border_color = "#313E41", corner_radius = 0, border_width = 3)
        self.dialogOutputMessage.place(x = 380, y = 190)
        self.dialogOutputMessage.grab_set()
        dialogOutputMessageLabel = customtkinter.CTkLabel(master = self.dialogOutputMessage, width = 171, height = 41, font = ("Inter", size, "bold"), justify = customtkinter.LEFT, text = message, wraplength = 180)
        dialogOutputMessageLabel.place(x = 17, y = 19)
        closeDialogOutputMessage = customtkinter.CTkButton(master = self.dialogOutputMessage, width = 91, height = 35, fg_color = "#F03131", text = 'Close', command = self.closeDialogOutputMessage, text_color = "#000000", font = ("Inter", 13, "bold"))
        closeDialogOutputMessage.place(x = 13, y = 74)

    def closeDialogOutputMessage(self) -> None:
        self.dialogOutputMessage.destroy()

    def liveDigitalClock(self):
        digitalTime = time.strftime("%H:%M:%S")
        self.liveClock.set(digitalTime)
        self.after(1000, self.liveDigitalClock)

    def darkLightButtonPressed(self, event) -> None:
        if self.currentMode == "dark":
            self.middleTopRightDarkLightMode.configure(image = imageLoadingAndCreator().darkModeIcon)
            sqlQuery(self.table, self.cursor).setModeProfile("light")
            customtkinter.set_appearance_mode("light")
            self.currentMode = "light"
        elif self.currentMode == "light":
            self.middleTopRightDarkLightMode.configure(image = imageLoadingAndCreator().lightModeIcon)
            sqlQuery(self.table, self.cursor).setModeProfile("dark")
            customtkinter.set_appearance_mode("dark")
            self.currentMode = "dark"

    def darkLightButtonStartHover(self, event) -> None:
        if self.currentMode == "light":
            self.middleTopRightDarkLightMode.configure(image = imageLoadingAndCreator().darkModeIconHover)
        elif self.currentMode == "dark":
            self.middleTopRightDarkLightMode.configure(image = imageLoadingAndCreator().lightModeIconHover)

    def darkLightButtonStopHover(self, event) -> None:
        if self.currentMode == "light":
            self.middleTopRightDarkLightMode.configure(image = imageLoadingAndCreator().darkModeIcon)
        elif self.currentMode == "dark":
            self.middleTopRightDarkLightMode.configure(image = imageLoadingAndCreator().lightModeIcon)

    def closeButtonStartHover(self, event) -> None:
        self.closeWindowImageLabel.configure(image = imageLoadingAndCreator().closeWindowRedImage)

    def closeButtonStopHover(self, event) -> None:
        self.closeWindowImageLabel.configure(image = imageLoadingAndCreator().closeWindowBlackImage)

    def minimizeWindowWhenCloseIconPressed(self, event) -> None:
        self.destroy()

    def popUpWindowIconTray(self) -> None:
        #self.deiconify()  # Unhide the window if it's hidden
        self.lift()  # Bring the window to the front
        self.attributes("-topmost", True)  # Make sure it's on top
        self.attributes("-topmost", False)

    def startMovingWindow(self, event) -> None:
        self.xOffSet = event.x
        self.yOffSet = event.y

    def dragWindow(self, event) -> None:
        if self.xOffSet is not None and self.yOffSet is not None:
            self.geometry(f'+{event.x_root - self.xOffSet}+{event.y_root - self.yOffSet}')

    def openWindowCentreOfScreen(self, width : int, height : int) -> None:
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()
        x = (screenWidth - width) // 2
        y = (screenHeight - height) // 2
        self.geometry(f'{width}x{height}+{x}+{y}')

    def run(self) -> None:
        self.mainloop()
########################################################################################################################
if __name__ == "__main__":
    app = mainWindow()
    checking4Birthdays(app.table, app.cursor).start()
    #Starting the tray icon in a new thread
    trayThread = threading.Thread(target = setupTrayIcon)
    trayThread.daemon = True  # Daemon thread will exit when main program exits
    trayThread.start()
    #Starting up the GUI
    app.run()