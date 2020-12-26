import re
from datetime import datetime

# function for parsing templates
def replace_var(text: str, variables: dict, row: dict):
    text = text
    for i in variables.keys():
        text = re.sub(f"<{i}>", row[variables[i]], text)

    return text


# string format of current time
def now():
    return datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


# default variables for gmail env
gmailvars = """\nSMTP_HOST='smtp.gmail.com'
SMTP_PORT='587'
SENDER_EMAIL='youremail@gmail.com'
SENDER_PASSWORD='yourpassword'
"""
# template message
template_message = """Dear <var1>,

This is a test message. Please change this template according to your will before sending your <var2> mails.

Thank you

Regards,
<var3>
"""
