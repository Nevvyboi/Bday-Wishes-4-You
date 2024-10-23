#Imports to send email and get environment variables
import windows_toasts
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
load_dotenv()
from windows_toasts import Toast, WindowsToaster, ToastDisplayImage, ToastScenario

#Creating the class to send birthday emails
class sendBirthdayReminders():
    def __init__(self):
        self.BirthdayWishesUser = os.getenv('BirthdayWishesUser')
        self.BirthdayWishesPassword = os.getenv('BirthdayWishesPassword')
        self.toaster = WindowsToaster("Birthday Wishes 🎂")

    def sendWindowsNotificationReminder(self, friendName : str, type : int) -> None:
        if type == 3:
            title = f"🎉 {friendName}'s Birthday is Coming Up!"
            msg = f"{friendName}'s birthday is in 3 days. Start preparing your wishes!"
        elif type == 1:
            title = f"🎂 Only 24 Hours Until {friendName}'s Birthday! ⏳"
            msg = f"Get ready! {friendName}'s birthday is tomorrow. Don't forget to send your best wishes!"
        elif type == 0:
            title = f"🎉 It's {friendName}'s Birthday TODAY! 🎈"
            msg = f"Today is {friendName}'s birthday! Make sure to celebrate and send your love!"
        else:
            # Default fallback message if none of the conditions match
            title = f"🎂 Birthday Reminder"
            msg = f"{friendName}'s birthday is coming soon. Be ready!"
        newToast = Toast()
        newToast.text_fields = [title, msg]
        newToast.scenario = ToastScenario.Reminder
        newToast.AddImage(ToastDisplayImage.fromPath(r"/Utilities/Images\birthdayWishesLogo.png"))
        self.toaster.show_toast(newToast)

    def sendEmailNotification(self, sendTo: str, bdayName: str, birthdayDate: str, type: str, notes : str) -> None:
        # Create a multipart email
        msg = MIMEMultipart()
        msg['From'] = "your_email@example.com"
        msg['To'] = sendTo
        msg['Subject'] = ""

        # Define the email body based on the type of reminder (3 days, 24 hours, or actual birthday)
        if type == "3days":
            msg['Subject'] = f"🎉 Get Ready! {bdayName}'s Birthday is in 3 Days! 🎂"
            body = f"""
            Hi there,

            Just a friendly reminder that {bdayName}'s birthday is coming up in 3 days on {birthdayDate}! 🎂
            Now’s the perfect time to plan how you’ll celebrate your awesome friend.

            Whether it’s a surprise message, gift, or a plan to hang out, make sure you make {bdayName}'s day as special as they are!

            Best wishes,
            The BirthdayWishes Team 🎉🎁
            """

        elif type == "24hours":
            msg['Subject'] = f"🎂 Only 24 Hours Until {bdayName}'s Birthday! ⏳🎉"
            body = f"""
            Hey there,

            This is just a quick reminder that {bdayName}'s birthday is only 24 hours away! 🎉
            Don't forget to reach out and make their day truly special on {birthdayDate}.

            Get your messages, surprises, or celebrations ready! 🎈🎁

            Warm regards,
            The BirthdayWishes Team 🎂🎉
            """

        elif type == "today":
            msg['Subject'] = f"🎉 It's {bdayName}'s Birthday TODAY! 🎂🎈"
            body = f"""
            Hi {sendTo},

            🎉 It's time to celebrate! 🎉
            Today is {bdayName}'s birthday ({birthdayDate}), and it's a perfect opportunity to show them how much they mean to you.

            Don't forget to wish them a fantastic day full of happiness and joy! 🎂🎁

            Best regards,
            The BirthdayWishes Team 🎂🎉
            """

        else:
            # Default message if the type is unknown
            msg['Subject'] = "🎉 Birthday Reminder 🎂"
            body = f"""
            Hello,

            Just a heads up that {bdayName}'s birthday is coming soon on {birthdayDate}.
            Don’t forget to send them some birthday love!

            Best,
            The BirthdayWishes Team
            """

        # Attach the body text
        msg.attach(MIMEText(body, 'plain'))

        # Sending the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login('your_email@example.com', 'your_password')
                smtp.sendmail(msg['From'], sendTo, msg.as_string())
            print(f"Email successfully sent to {sendTo}")
        except Exception as e:
            print(f"Failed to send email to {sendTo}: {e}")

#sendBirthdayReminders().sendWindowsNotificationReminder("Nevin Tom", 1)
#sendBirthdayReminders("heh", "jo").sendEmailNotification("nevintom2018@gmail.com", "Nevin Tom", "10-20-2204", "hi")