import os
from dotenv import load_dotenv
from csv import DictReader
from datetime import datetime

from .csvreader import cache

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def now():
    return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


def sender(cachedb:str):
    database = open(cachedb, 'r', encoding='utf-8')
    reader = DictReader(database)

    #loading env
    load_dotenv()
    SMTP_HOST = os.environ.get("SMTP_HOST")
    SMTP_PORT = os.environ.get("SMTP_PORT")
    SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
    SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
    
    #create session
    session = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    session.starttls()
    session.login(SENDER_EMAIL, SENDER_PASSWORD)

    successlog = open('successlog.txt', 'a', encoding='utf-8')
    failurelog = open('failurelog.txt', 'a', encoding='utf-8')
    successlog.write(f"\nSession starts at {now()}\n")
    failurelog.write(f"\nSession starts at {now()}\n")
    for row in reader:
        RECEIVER_EMAIL = row['email']
        try:
            email = MIMEMultipart()
            email['From'] = SENDER_EMAIL
            email['To'] = RECEIVER_EMAIL
            email['Subject'] = row['subject']
            email.attach(MIMEText(row['body'], 'plain'))
            session.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email.as_string())
            successlog.write(f"Email sent to {RECEIVER_EMAIL} at {now()}\n")
        except:
            failurelog.write(f"Failed to send email to {RECEIVER_EMAIL}. Time: {now()}\n")
    
    successlog.write(f"\nSession ends at {now()}\n")
    failurelog.write(f"\nSession ends at {now()}\n")

    successlog.close()
    failurelog.close()
    database.close()
    os.remove(cachedb)

    session.quit()



class MailCSV():
    def __init__(self, filename:str):
        self.file = filename
        self.variables = dict()
        self.constants = dict()
        self.template = 'template.txt'
        self.email_field = 'email'
        self.subject = 'Blank Subject'

    def add_variables(self, variables:dict):
        self.variables.update(variables)
    
    def add_constants(self, constants:dict):
        self.constants.update(constants)
    
    def set_template(self, filename:str):
        self.template = filename
    
    def set_email_field(self, fieldname:str):
        self.email_field = fieldname

    def set_subject_file(self, filename:str):
        f = open(filename, 'r', encoding='utf-8')
        self.subject = f.readline()
    
    def set_subject(self, text:str):
        self.subject = text
    
    def send(self):
        cachedb = cache(self.file, self.template, self.variables, self.constants, self.subject, self.email_field)
        sender(cachedb)
