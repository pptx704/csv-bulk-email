import os
import smtplib

from csv import DictReader

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .extras import now, replace_var

# start new session
def startsession(credentials):
    # loading credentials
    SMTP_HOST = credentials.get("SMTP_HOST")
    SMTP_PORT = credentials.get("SMTP_PORT")
    SENDER_EMAIL = credentials.get("SENDER_EMAIL")
    SENDER_PASSWORD = credentials.get("SENDER_PASSWORD")

    # creating smtp session
    session = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    session.ehlo_or_helo_if_needed()
    session.starttls()
    session.login(SENDER_EMAIL, SENDER_PASSWORD)

    return session


# for sending bulk email where everybody will get same email
def sendnovar(
    database: str,
    body: str,
    subject: str,
    email_field: str,
    credentials: dict,
    type: str,
):
    # loading database
    database = open(database, "r", encoding="utf-8")
    reader = DictReader(database)

    # start
    session = startsession(credentials)
    SENDER_EMAIL = credentials.get("SENDER_EMAIL")

    # making logfiles
    successlog = open("success.log", "a", encoding="utf-8")
    failurelog = open("failure.log", "a", encoding="utf-8")
    successlog.write(f"\nSession starts at {now()}\n")
    failurelog.write(f"\nSession starts at {now()}\n")

    # email processing
    for row in reader:
        RECEIVER_EMAIL = row[email_field]
        try:
            email = MIMEMultipart()
            email["From"] = SENDER_EMAIL
            email["To"] = RECEIVER_EMAIL
            email["Subject"] = subject
            email.attach(MIMEText(body, type))
            session.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email.as_string())
            successlog.write(f"Email sent to {RECEIVER_EMAIL} at {now()}\n")
        except:
            failurelog.write(
                f"Failed to send email to {RECEIVER_EMAIL}. Time: {now()}\n"
            )

    # ending session and closing logs
    successlog.write(f"\nSession ends at {now()}\n-----------------------\n")
    failurelog.write(f"\nSession ends at {now()}\n-----------------------\n")

    successlog.close()
    failurelog.close()
    database.close()

    session.quit()


def sendvar(
    database: str,
    template: str,
    subject: str,
    email_field: str,
    variables: dict,
    credentials: dict,
    type: str,
):
    # loading database
    database = open(database, "r", encoding="utf-8")
    reader = DictReader(database)

    # start session
    session = startsession(credentials)
    SENDER_EMAIL = credentials.get("SENDER_EMAIL")

    # making logfiles
    successlog = open("success.log", "a", encoding="utf-8")
    failurelog = open("failure.log", "a", encoding="utf-8")
    successlog.write(f"\nSession starts at {now()}\n")
    failurelog.write(f"\nSession starts at {now()}\n")

    # email processing
    for row in reader:
        RECEIVER_EMAIL = row[email_field]
        try:
            email = MIMEMultipart()
            email["From"] = SENDER_EMAIL
            email["To"] = RECEIVER_EMAIL
            # subject = replace_var(subject, variables, row)
            email["Subject"] = subject
            body = replace_var(template, variables, row)
            email.attach(MIMEText(body, type))
            session.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email.as_string())
            successlog.write(f"Email sent to {RECEIVER_EMAIL} at {now()}\n")
        except:
            failurelog.write(
                f"Failed to send email to {RECEIVER_EMAIL}. Time: {now()}\n"
            )

    # ending session and closing logs
    successlog.write(f"\nSession ends at {now()}\n-----------------------\n")
    failurelog.write(f"\nSession ends at {now()}\n-----------------------\n")

    successlog.close()
    failurelog.close()
    database.close()

    session.quit()
