import smtplib
import logindetails # Enter GMAIL login details at logindetails.py

def send_email(subject, message):
    try:
        mailserver = smtplib.SMTP('smtp.gmail.com:587')
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(logindetails.emailAddress, logindetails.password)
        message = 'Subject: {}\n\n{}'.format(subject, message)
        mailserver.sendmail(logindetails.emailAddress, logindetails.emailAddress, message)
        mailserver.quit()
        print("Task done. Success: Email sent!")
    
    except:
        print("Task done. Email failed to send.")