#CustomTkinter is a python UI-library based on Tkinter, which provides new, modern and fully customizable widgets.
import customtkinter
#Importing the sqlQuery class for database queries
from Utilities.sqlQueries import sqlQuery
from Utilities.imageLoader import imageLoadingAndCreator
from Utilities.colorPalette4Labels import colour4Widgets
#Importing datetime from python
from datetime import datetime
#Importing re for pattern searching
import re
#Importing filedialog to create a window to access file explorer for image access
from tkinter import filedialog
#Importing PIL to utilize Image package to open Image in its form
from PIL import Image
#Importing input/output package to convert image to bytes object
import io

class profileFrame():
    def __init__(self, master, table, cursor):
        self.master = master
        self.table = table
        self.cursor = cursor
        #Users avatar otherwise use emptyPfp
        self.currentProfilePicture = None
        #Setting the profile frame and loading it up when called
        self.profileBackgroundFrame = customtkinter.CTkFrame(master = self.master, width = 197, height = 513, border_color = "#313E41", border_width = 3)
        self.profileBackgroundFrame.place(x = 761, y = 15)
        #Making the frame the only widget interactable
        self.profileBackgroundFrame.grab_set()
        #Setting up the labels ontop the frame
        self.topProfilePicture = customtkinter.CTkLabel(master = self.profileBackgroundFrame, width = 100, height = 100,text = "", image = self.master.userAvatar or imageLoadingAndCreator().emptyPfp)
        self.topProfilePicture.place(x = 49, y = 21)
        self.topProfilePicture.bind("<Button-1>", self.emptyAvatarPressed)
        nameSurnameLabel = customtkinter.CTkLabel(master = self.profileBackgroundFrame, width = 167, height = 35, text = "Name Surname", font = ("Open Sans", 16, "bold"), corner_radius = 5, fg_color = colour4Widgets().findColour(self.master.theme))
        nameSurnameLabel.place(x = 12, y = 137)
        self.nameSurnameEntryPlacementData = customtkinter.StringVar(value = sqlQuery(self.table, self.cursor).getNameSurnameProfile() or "Name Surname")
        self.nameSurnameEntry = customtkinter.CTkEntry(master = self.profileBackgroundFrame, width = 167, height = 35, textvariable = self.nameSurnameEntryPlacementData)
        self.nameSurnameEntry.place(x = 12, y = 189)
        bdayLabel = customtkinter.CTkLabel(master = self.profileBackgroundFrame, width = 167, height = 35, text = "Birthday", font = ("Open Sans", 16, "bold"), corner_radius = 5, fg_color = colour4Widgets().findColour(self.master.theme))
        bdayLabel.place(x = 12, y = 241)
        self.bdayEntryPlacementData = customtkinter.StringVar(value = sqlQuery(self.table, self.cursor).getBdayProfile() or "DD-MM-YYYY")
        self.bdayEntry = customtkinter.CTkEntry(master = self.profileBackgroundFrame, width = 167, height = 35, textvariable = self.bdayEntryPlacementData)
        self.bdayEntry.place(x = 12, y = 293)
        emailLabel = customtkinter.CTkLabel(master = self.profileBackgroundFrame, width = 167, height = 35, text = "Email", font = ("Open Sans", 16, "bold"), corner_radius = 5, fg_color = colour4Widgets().findColour(self.master.theme))
        emailLabel.place(x = 12, y = 345)
        self.emailEntryPlacementData = customtkinter.StringVar(value = sqlQuery(self.table, self.cursor).getEmailProfile() or "Email Address")
        self.emailEntry = customtkinter.CTkEntry(master = self.profileBackgroundFrame, width = 167, height = 35, textvariable = self.emailEntryPlacementData)
        self.emailEntry.place(x = 12, y = 397)
        #Creating the close/save buttons and placing on the frame
        closeProfile = customtkinter.CTkButton(master = self.profileBackgroundFrame, width = 76, height = 35, text = "Close", font = ("Open Sans", 13, "bold"), command = self.closeProfileFrame, fg_color = "#F03131")
        closeProfile.place(x = 12, y = 448)
        saveProfile = customtkinter.CTkButton(master = self.profileBackgroundFrame, width  = 76, height = 35, text = "Save", font = ("Open Sans", 13, "bold"), fg_color = "#2FD82F", command = self.saveProfileFrame)
        saveProfile.place(x = 103, y = 448)

    def saveProfileFrame(self) -> None:
        if self.currentProfilePicture is None:
            pass
        elif self.currentProfilePicture is not None:
            avatarData = customtkinter.CTkImage(self.currentProfilePicture, size = (100, 100))
        nameSurnameEntryData = self.nameSurnameEntry.get()
        bdayEntryData = self.bdayEntry.get()
        emailEntryData = self.emailEntry.get()
        if nameSurnameEntryData == "Name Surname" or nameSurnameEntryData == "":
            nameSurnameEntryData = None
        elif nameSurnameEntryData != "":
            if nameSurnameEntryData.isnumeric(): return self.master.dialogMessage("Oops! Names can’t include numbers. Please use letters only.", 13)
        if bdayEntryData == "DD-MM-YYYY" or bdayEntryData == "":
            bdayEntryData = None
        elif bdayEntryData != "":
            if self.validationBirthday(bdayEntryData) is False: return
        if emailEntryData == "Email" or emailEntryData == "":
            emailEntryData = None
        elif emailEntryData != "":
            if self.checkIfValidEmail(emailEntryData) is False: return self.master.dialogMessage("Invalid email address. Please enter a valid email in the format: example@domain.com.", 12)
        sqlQuery(self.table, self.cursor).setSaveProfile(nameSurnameEntryData, bdayEntryData, self.imageToBytes(self.currentProfilePicture), emailEntryData)
        self.master.userAvatar = self.bytesToImage(sqlQuery(self.table, self.cursor).getAvatarProfile(), (100, 100))
        self.master.topProfilePictureMainWindow.configure(image = self.master.userAvatar)
        self.master.customizeName.configure(text = sqlQuery(self.table, self.cursor).getNameSurnameProfile() or "")
        self.master.customizeBirthdayDay.configure(text = sqlQuery(self.table, self.cursor).getBdayProfile() or "")
        self.profileBackgroundFrame.destroy()
        if sqlQuery(self.table, self.cursor).getBdayProfile() != None:
            self.master.liveBdayTillBday()

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

    def checkIfValidEmail(self, email : str) -> bool:
        #Regular expression for validating an email address
        emailPattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        #Checking if the email matches the regex pattern
        if re.match(emailPattern, email):
            return True
        else:
            return False

    def isLeapYear(self, year: int) -> bool:
        #Check to see if the year is a leap year
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def validationBirthday(self, date : str) -> bool:
        #Regular expression to match the format DD-MM-YYYY
        datePattern = r"^\d{2}-\d{2}-\d{4}$"
        #Getting the current year
        currentYear = datetime.now().year
        #Checking if the input matches the pattern
        if re.match(datePattern, date):
            #Splitting the input into day, month, and year
            day, month, year = map(int, date.split('-'))
            #Checking to see if the year is not greater than the current year
            if year > currentYear:
                self.master.dialogMessage(f"Invalid year. The year cannot be in the future. Please enter a valid year.", 13)
                return False
            #Checking to see if the month is valid
            if not 1 <= month <= 12:
                self.master.dialogMessage(f"Invalid month. Please enter a month between 1 (January) and 12 (December).", 13)
                return False
            #Checking the days in the month
            if month == 2:  # February
                if self.isLeapYear(year):
                    if day > 29:
                        self.master.dialogMessage("Invalid day. February in a leap year has a maximum of 29 days.", 13)
                        return False
                else:
                    if day > 28:
                        self.master.dialogMessage("Invalid day. February in a non-leap year has a maximum of 28 days.", 13)
                        return False
            elif month in [4, 6, 9, 11]:  #April, June, September, November
                if day > 30:
                    self.master.dialogMessage(f"Invalid day. The month {month} has a maximum of 30 days.", 13)
                    return False
            else:  #All other months have 31 days
                if day > 31:
                    self.master.dialogMessage(f"Invalid day. The month {month} has a maximum of 31 days.", 13)
                    return False
            #If all checks pass, return True
            return True
        else:
            self.master.dialogMessage("Invalid date format. Please use format: DD-MM-YYYY.", 13)
            return False

    def closeProfileFrame(self) -> None:
        self.profileBackgroundFrame.destroy()

    def emptyAvatarPressed(self, event) -> None:
        fileTypesAccepted = [("Image Files", "*.png;*.jpg;*.jpeg;")]
        selectedImagePath = filedialog.askopenfilename(title = "Choose a image for your avatar", filetypes = fileTypesAccepted)
        if selectedImagePath:
            currentPfp = Image.open(selectedImagePath).convert("RGBA")
            currentPfp = imageLoadingAndCreator().createCircularImage(currentPfp.resize((100, 100)))
            self.currentProfilePicture = currentPfp
            self.topProfilePicture.configure(image = customtkinter.CTkImage(currentPfp, size = (100, 100)))