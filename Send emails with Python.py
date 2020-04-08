import smtplib # SMTP (Simple Mail Transfer Protocol) Python library

smtpObj = smtplib.SMTP('smtp.office365.com', 587) # makes an Outlook/Hotmail smtp object
smtpObj.ehlo() # sends 'hello' message; must be done
smtpObj.starttls() # enables encryption method; puts connection in TLS mode

print('The server is set up, please put in your Outlook/Hotmail email:')
email = input()

print('Please put in your password:')
password = input()

smtpObj.login(email, password)

print("Put in the recipient's email:")
recipient = input()

print("You can change your message in your Python code.")

message = """\
Subject: Sending emails with Python, faster, again

This email was sent with some Python code"""

smtpObj.sendmail(email, recipient, message)

smtpObj.quit() # disconnects from the smtp server; must be done

print("Message has been sent")
