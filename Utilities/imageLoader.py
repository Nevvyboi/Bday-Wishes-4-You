import customtkinter
from PIL import Image, ImageDraw

class imageLoadingAndCreator():
    def __init__(self):
        #Loading the images/icons etc
        self.birthdayWishesIcon = "Images//birthdayDayWishesIcon.ico"
        self.birthdayWishesLogoTrayIcon = Image.open("Images//birthdayWishesLogo.png").resize((64, 64), resample = Image.Resampling.LANCZOS)
        self.birthdayWishesLogo = customtkinter.CTkImage(Image.open("Images//birthdayWishesLogo.png"), size = (100, 100))
        self.emptyPfp = customtkinter.CTkImage(Image.open("Images//emptyPfp.png"), size = (100, 100))
        self.emptyPfpBdayCard = Image.open("Images//emptyPfpBdayCard.png").resize((75, 75), Image.Resampling.LANCZOS)
        self.resetPfpBdayCard = customtkinter.CTkImage(Image.open("Images//deleteIcon.png"), size = (26, 26))
        self.resetPfpRedBdayCard = customtkinter.CTkImage(Image.open("Images//deleteIconRed.png"), size = (26, 26))
        self.dataInfo = customtkinter.CTkImage(Image.open("Images//layersDataInformation.png"), size = (30, 30))
        self.supportCentre = customtkinter.CTkImage(Image.open("Images//helpCentreCircle.png"), size = (44, 44))
        self.closeWindowBlackImage = customtkinter.CTkImage(Image.open("Images//closeWindowIconBlack.png"), size = (41, 41))
        self.closeWindowRedImage = customtkinter.CTkImage(Image.open("Images//closeWindowIconRed.png"), size = (41, 41))
        self.lightModeIcon = customtkinter.CTkImage(Image.open("Images//lightModeIcon.png"), size = (36, 36))
        self.darkModeIcon = customtkinter.CTkImage(Image.open("Images//darkModeIcon.png"), size = (36, 36))
        self.lightModeIconHover = customtkinter.CTkImage(Image.open("Images//lightModeIconHover.png"), size = (36, 36))
        self.darkModeIconHover = customtkinter.CTkImage(Image.open("Images//darkModeIconHover.png"), size = (36, 36))

    def createCircularImage(self, image) -> None:
        # Ensure the image is square by taking the smallest dimension
        sizeOfCircleMask = min(image.size)
        # Creating the transparent circular mask
        mask = Image.new('L', (sizeOfCircleMask, sizeOfCircleMask), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, sizeOfCircleMask, sizeOfCircleMask), fill=255)
        # Resize the mask with anti-aliasing for smooth edges
        mask = mask.resize((sizeOfCircleMask, sizeOfCircleMask), Image.LANCZOS)
        # Create an empty image with a transparent background for the circular image
        result = Image.new('RGBA', (sizeOfCircleMask, sizeOfCircleMask), (0, 0, 0, 0))
        # Resize and paste the original image using the circular mask
        image = image.resize((sizeOfCircleMask, sizeOfCircleMask), Image.LANCZOS)
        result.paste(image, (0, 0), mask)
        return result

    def createRoundedRectangularImage(self, image) -> None:
        # Ensure the image is square by taking the smallest dimension
        sizeOfRectMask = min(image.size)
        # Creating the transparent rectangular mask with rounded corners
        mask = Image.new(mode = 'L', size = (sizeOfRectMask, sizeOfRectMask), color = 0)
        draw = ImageDraw.Draw(mask)
        # Draw the rounded rectangle with corner radius of 5
        draw.rounded_rectangle((0, 0, sizeOfRectMask, sizeOfRectMask), radius = 15, fill = 255)
        # Resize the mask with anti-aliasing for smooth edges
        mask = mask.resize((sizeOfRectMask, sizeOfRectMask), Image.LANCZOS)
        # Create an empty image with a transparent background for the rectangular image
        result = Image.new(mode = 'RGBA', size = (sizeOfRectMask, sizeOfRectMask), color = (0, 0, 0, 0))
        # Resize and paste the original image using the rectangular mask
        image = image.resize((sizeOfRectMask, sizeOfRectMask), Image.LANCZOS)
        result.paste(image, (0, 0), mask)
        self.pfpLabelBdayCard = result
        return result