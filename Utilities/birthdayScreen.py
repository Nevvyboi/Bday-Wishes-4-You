#CustomTkinter is a python UI-library based on Tkinter, which provides new, modern and fully customizable widgets.
import customtkinter
#Importing the the different utilities
from Utilities.sqlQueries import sqlQuery
from Utilities.imageLoader import imageLoadingAndCreator
from Utilities.colorPalette4Labels import colour4Widgets
#Importing filedialog to create a window to access file explorer for image access
from tkinter import filedialog
#Importing PIL to utilize Image package to open Image in its form
from PIL import Image
#Importing datetime from python
from datetime import datetime
#Importing re for pattern searching
import re
#Importing input/output package to convert image to bytes object
import io

class addBirthdayFrame():
    def __init__(self, master, table, cursor):
        self.master = master
        self.table = table
        self.cursor = cursor
        #Variable to check if add birthday frame exists or not
        self.createBirthdayFrame = None
        #Users avatar otherwise use emptyPfp
        self.pfpLabelBdayCard = None
        #To help prevent multiple frames openin gon top of each other
        if hasattr(self.master, 'createBirthdayFrame') and self.createBirthdayFrame is not None:
            return
        else:
            self.createBirthdayFrame = customtkinter.CTkFrame(master = self.master, width = 533, height = 450, border_color = "#313E41", border_width = 3)
            self.createBirthdayFrame.place(x = 207, y = 78)
            #Making the frame the only widget interactable
            self.createBirthdayFrame.grab_set()
            addBdayFrameTitle = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "Add Birthday", width = 144, height = 31, anchor =  "w",  font = ("Inter", 20, "bold"))
            addBdayFrameTitle.place(x = 21, y = 19)
            nameStarImportant = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "*", width = 14, height = 26, text_color = "#F03131", fg_color = "transparent")
            nameStarImportant.place(x = 10, y = 61)
            nameLabel = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "Name:", width = 70, height = 26, anchor =  "w",  font = ("Inter", 13, "bold"))
            nameLabel.place(x = 24, y = 61)
            self.nameEntry = customtkinter.CTkEntry(master = self.createBirthdayFrame, placeholder_text = "Name", width = 178, height = 26)
            self.nameEntry.place(x = 189, y = 61)
            #Adding a bind key function to run once a key is done pressing
            self.nameEntry.bind("<KeyRelease>", self.updateTextFieldNameBdayCard)
            bdayStarImportant = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "*", width = 14, height = 26, text_color = "#F03131", fg_color = "transparent")
            bdayStarImportant.place(x = 10, y = 98)
            bdayLabel = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "Birthday:", width = 70, height = 26, anchor =  "w",  font = ("Inter", 13, "bold"))
            bdayLabel.place(x = 24, y = 98)
            self.bdayEntry = customtkinter.CTkEntry(master = self.createBirthdayFrame, placeholder_text = "DD-MM-YYYY", width = 178, height = 26)
            self.bdayEntry.place(x = 189, y = 98)
            #Adding a bind key function to run once a key is done pressing
            self.bdayEntry.bind("<KeyRelease>", self.updateTextFieldBirthdayBdayCard)
            notesLabel = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "Notes:", width = 70, height = 26, anchor =  "w",  font = ("Inter", 13, "bold"))
            notesLabel.place(x = 24, y = 135)
            self.notesEntry = customtkinter.CTkEntry(master = self.createBirthdayFrame, placeholder_text = "Notes", width = 178, height = 26)
            self.notesEntry.place(x = 189, y = 135)
            #Adding a bind key function to run once a key is done pressing
            self.notesEntry.bind("<KeyRelease>", self.updateTextFieldNotesBdayCard)
            pfpLabel = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "Upload Profile Picture:", width = 165, height = 26, anchor =  "w",  font = ("Inter", 13, "bold"))
            pfpLabel.place(x = 24, y = 172)
            pfpButton = customtkinter.CTkButton(master = self.createBirthdayFrame, text = "Upload", width = 130, height = 26, command = self.emptyAvatarPressedBdayCard, font = ("Inter", 13, "bold"))
            pfpButton.place(x = 189, y = 172)
            self.pfpDestroyLabel = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "", width = 26, height = 26, image = imageLoadingAndCreator().resetPfpBdayCard, fg_color = colour4Widgets().findColour(self.master.theme), corner_radius = 5)
            self.pfpDestroyLabel.place(x = 330, y = 172)
            #Adding a bind key function to run once the button/label is pressed
            self.pfpDestroyLabel.bind("<Button-1>", self.deletePfpBdayCard)
            self.pfpDestroyLabel.bind("<Enter>", self.resetPfpStartHover)
            self.pfpDestroyLabel.bind("<Leave>", self.resetPfpStopHover)
            displaybdayCardTitle = customtkinter.CTkLabel(master = self.createBirthdayFrame, width = 371, height = 27, text = "Birthday Card Display", font = ("Inter", 20, "bold"), anchor = "w")
            displaybdayCardTitle.place(x = 21, y = 231)
            #Display Birthday Card
            addBirthdayCardFrame = customtkinter.CTkFrame(master = self.createBirthdayFrame, width = 491, height = 91, fg_color = colour4Widgets().findColour(self.master.theme))
            addBirthdayCardFrame.place(x = 21, y = 270)
            self.imageLabelBdayCard = customtkinter.CTkLabel(master = addBirthdayCardFrame, width = 75, height = 75, image = customtkinter.CTkImage(imageLoadingAndCreator().emptyPfpBdayCard, size = (75, 75)), text = "")
            self.imageLabelBdayCard.place(x = 15, y = 8)
            self.nameBdayCardLabel = customtkinter.CTkLabel(master = addBirthdayCardFrame, width = 262, height = 19, anchor = "w", text = "Name", font = ("Inter", 15, "bold"))
            self.nameBdayCardLabel.place(x = 101, y = 8)
            self.bdayBdayCardLabel = customtkinter.CTkLabel(master = addBirthdayCardFrame, width = 100, height = 16, anchor = "w", text = "Birthday Date", font = ("Inter", 13, "bold"))
            self.bdayBdayCardLabel.place(x = 101, y = 36)
            self.notesBdayCardLabel = customtkinter.CTkLabel(master = addBirthdayCardFrame, width = 312, height = 20, anchor = "w", text = "Notes", font = ("Inter", 13, "bold"))
            self.notesBdayCardLabel.place(x = 101, y = 63)
            dataInfoIcon = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "", image = imageLoadingAndCreator().dataInfo, width = 30, height = 30)
            dataInfoIcon.place(x = 17, y = 383)
            dataInfoIcon.bind("<Enter>", self.dataInfoStartHover)
            dataInfoIcon.bind("<Leave>", self.dataInfoStopHover)
            self.dataInfoLabel = customtkinter.CTkLabel(master = self.createBirthdayFrame, text = "", width = 231, height = 35)
            self.dataInfoLabel.place(x = 63, y = 380)
            #Creating the close/save buttons and placing on the frame
            closeProfile = customtkinter.CTkButton(master = self.createBirthdayFrame, command = self.closeAddBirthdayFrame, width = 91, height = 35, text = "Close", font = ("Open Sans", 13, "bold"), fg_color = "#F03131")
            closeProfile.place(x = 310, y = 380)
            saveProfile = customtkinter.CTkButton(master = self.createBirthdayFrame, command = self.saveAddBirthdayFrame, width  = 91, height = 35, text = "Save", font = ("Open Sans", 13, "bold"), fg_color = "#2FD82F")
            saveProfile.place(x = 421, y = 380)

    def saveAddBirthdayFrame(self) -> None:
        valueName = self.nameEntry.get()
        valueBday = self.bdayEntry.get()
        valueNotes = self.notesEntry.get()
        valuePfp = self.pfpLabelBdayCard or imageLoadingAndCreator().emptyPfpBdayCard
        if valueName == "" or valueBday == "":
            return self.master.dialogMessage("Oops! It looks like you missed a required field. Please provide the necessary information.", 12)
        if valueName.isnumeric():
            return self.master.dialogMessage("Oops! Names can’t include numbers. Please use letters only.", 13)
        if self.validationBirthday(valueBday) is False:
            return
        if self.checkIfNameExists(valueName) is False:
            return self.master.dialogMessage(f"Oops! It looks like a birthday for {valueName} exists already!", 13)
        sqlQuery(self.table, self.cursor).setSaveBdayCard(valueName, valueBday, self.imageToBytes(valuePfp), valueNotes)
        self.master.birthdayList = sqlQuery(self.table, self.cursor).getBirthdays()
        self.master.populateMiddleFrameWithBirthdays()
        self.createBirthdayFrame.destroy()
        self.createBirthdayFrame = None

    def checkIfNameExists(self, name: str) -> bool:
        birthdayList = sqlQuery(self.table, self.cursor).getBirthdays()
        birthdayListNamesOnly = list(map(lambda bday: bday[1], birthdayList))
        if name in birthdayListNamesOnly: return False
        return True

    def closeAddBirthdayFrame(self) -> None:
        self.createBirthdayFrame.destroy()
        self.pfpLabelBdayCard = None
        self.createBirthdayFrame = None

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

    def dataInfoStartHover(self, event) -> None:
        self.dataInfoLabel.configure(text = "All data is stored on your computer\nand can only be accessed by you ♡")

    def dataInfoStopHover(self, event) -> None:
        self.dataInfoLabel.configure(text = "")

    def resetPfpStartHover(self, event) -> None:
        self.pfpDestroyLabel.configure(image = imageLoadingAndCreator().resetPfpRedBdayCard)

    def resetPfpStopHover(self, event) -> None:
        self.pfpDestroyLabel.configure(image = imageLoadingAndCreator().resetPfpBdayCard)

    def deletePfpBdayCard(self, event) -> None:
        self.imageLabelBdayCard.configure(image = imageLoadingAndCreator().emptyPfpBdayCard)
        self.pfpLabelBdayCard = None

    def updateTextFieldNotesBdayCard(self, event) -> None:
        valueNotes = self.notesEntry.get()
        if valueNotes == "":
            self.notesBdayCardLabel.configure(text = "Notes")
        else:
            self.notesBdayCardLabel.configure(text = valueNotes)

    def updateTextFieldBirthdayBdayCard(self, event) -> None:
        valueBday = self.bdayEntry.get()
        if valueBday == "":
            self.bdayBdayCardLabel.configure(text = "Birthday Date")
        else:
            self.bdayBdayCardLabel.configure(text = valueBday)

    def updateTextFieldNameBdayCard(self, event) -> None:
        valueName = self.nameEntry.get()
        if valueName == "":
            self.nameBdayCardLabel.configure(text = "Name")
        else:
            self.nameBdayCardLabel.configure(text = valueName)

    def emptyAvatarPressedBdayCard(self) -> None:
        selectedImagePath = filedialog.askopenfilename(title = "Choose a image for your birthday card", filetypes = [("Image Files", "*.png;*.jpg;*.jpeg;")])
        if selectedImagePath:
            currentPfp = Image.open(selectedImagePath).convert("RGBA")
            currentPfp = imageLoadingAndCreator().createRoundedRectangularImage(currentPfp.resize((75, 75)))
            self.pfpLabelBdayCard = currentPfp
            self.imageLabelBdayCard.configure(image = customtkinter.CTkImage(currentPfp, size = (75, 75)))
            self.currentPfpBdayCard = customtkinter.CTkImage(currentPfp, size = (75, 75))

    def imageToBytes(self, image) -> bytes:
        if image is None:
            return None
        else:
            imageByteArray = io.BytesIO()
            image.save(imageByteArray, "PNG")
            return imageByteArray.getvalue()