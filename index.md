# python-bulkmail

#### version 1.0.2

This package is for sending bulk emails using a CSV database. Bulk emails can be sent using CLI or can be used inside other python applications.

Currently it can send only text and html based emails but will soon have attachments facilities.

## Dependencies

### Python Version

Python 3.7 +

### Required Packages

`python-dotenv==0.15.0`
`click==7.1.2`

## Installation

`pip install bulkmail`

Run `bulkmail --help` to check if the package was installed in command line properly.

# Usage

The following demo csv database will be used all over this documentation.

```
Full Name,Date of Birth,Citizenship,Contact No.,Email Address
Mr. A,18/10/1988,Yes,+8801911111111,a@gmail.com
Mr. B,18/11/1988,No,+8801911111112,b@gmail.com
Mr. C,18/12/1988,Yes,+8801911111113,c@gmail.com
```



## Command Line Tool

The `bulkmail` CLI has two types of features currently. You can send bulk emails using already formatted residual files. Or you might not want extra hassle of junks(!). For both cases, you will need a csv database mandatorily.

### Preformatted Files

Get into the folder where your csv file is located. Suppose the database name is `mydb.csv`. Create a `.env` file with the following variables into the same directory-

```python
SMTP_HOST='smtp.gmail.com' #Or your smtp server address
SMTP_PORT='587' #Or your smtp port number
SENDER_EMAIL='youremail@domain.com'
SENDER_PASSWORD='yourpassword'
```

Make sure to enable `less secure apps` for in your Gmail account settings. I will try to add secured API based login for Gmail.

Then create a `template.txt` file where you will save your mail template.

Your directory structure will look like below.

```
├───myfolder
├──────.env
├──────mydb.csv
├──────template.txt
```

Apparently you can skip all the hassles by running `bulkmail defaults` command in the folder your `.csv` file is located and the app will take care of creating those for you. 

After running the command, the directory structure will look like this.

```
├───myfolder
├──────.env
├──────mydb.csv
├──────template.txt
```

The `.env` and `template.txt` fill will consequently look like the below-

```
SMTP_HOST='smtp.gmail.com'
SMTP_PORT='587'
SENDER_EMAIL='youremail@gmail.com'
SENDER_PASSWORD='yourpassword'
```

```
Dear <var1>,

This is a test message. Please change this template according to your will before sending your <var2> mails.

Thank you

Regards,
<var3>
```

You can easily edit them and proceed. Check [writing templates](#templating) for details.



After creating the templates and environments, you can run the following command to start sending emails-

`bulkmail sendmail --database mydb.csv --type plain --template template.txt --subject "Your email subject" --email-field 'Email Address'`

or simply,

`bulkmail sendmail --db mydb.csv --type plain --t template.txt --s "your email subject" -e 'Email Address'`

or just,

`bulkmail sendmail --type plain`

You will be told to add the other options by the prompt. The process will look something like this-

```
>> bulkmail sendmail --type plain
Database: mydb.csv
Template: template.txt
Subject: Test email
Email field: email
Database: mydb.csv
Template: template.txt
Subject: Bulk Email
Email field: email
Do you want to use variables? [y/N]: n
Started sending emails. Please check success.log and failure.log for updates on individual emails

Sending complete.
>>
```

Check [Email Field](#email-field) and [Variables](#variables) for details about these.

A `success.log` and a `failure.log` file will be visible in the folder. They will look something like this from inside-

```
Session starts at 26/12/2020, 00:36:07
Email sent to a@gmail.com at 26/12/2020, 00:36:09
Email sent to b@gmail.com at 26/12/2020, 00:36:10
Email sent to c@gmail.com at 26/12/2020, 00:36:10
Session ends at 26/12/2020, 00:36:11
-----------------------
```

Overall directory will look like below after the process is over-

```
├───myfolder
├──────.env
├──────mydb.csv
├──────failure.log
├──────success.log
├──────template.txt
```

### Working with temporary files

It might happen that you need to write a short email or you don't want to save your `.env` or `template.txt` file. In that case go to the directory where your `mydb.csv` file is located and use the following command-

`bulkmail sendtemp --database mydb.csv --subject "Your subject" --email-field 'Email Address'`

or simply,

`bulkmail sendtemp --d mydb.csv --s "Your subject" -e 'Email Address'`

or just

`bulkmail sendtemp`

Your command prompt will more or less look like below-

```
>> bulkmail sendtemp
Database: db.csv
Subject: My email
Email field: Email Address
Email body type (plain or html): plain
Edit the template.txt and .env file and then continue.
Are you done editing the files? [y/N]:
```

And the directory will be something like this-

```
├───myfolder
├──────.env
├──────mydb.csv
├──────template.txt
```

Edit the `.env` and `template.txt` as per your need and then type `y` in the command prompt.

Then [set up variables](#variables) and continue. Your mails will start being sent. After the process is over, the folder directory will look like below with no template and environment file-

```
├───myfolder
├──────failure.log
├──────mydb.csv
├──────success.log
```



## Using in another Python Application

You can use this package in your python application if you need to.

Currently the package contains one class `TextMail` which is used to send text based bulk emails. `TexMail` class takes two mandatory arguments `filename` which is the database file name, in this case `mydb.csv` and `type` which tells if the email will be plaintext or html.

Methods-

*  `set_email_field`- Takes email field name as argument and sets up the [email field](#email-field) name. 
* `set_subject`- Takes the email's subject as argument and sets up the mails' subject. 
* `set_template`- Takes template file name e.g. `template.txt` as argument and reads the content.
* `add_variables`- Takes a dictionary of [variables](#variables) and sets them up for replacing in template.

Look at the following code snippets for details-

```python
from bulkmail import TextMail

subject = "An email"
variables = {
    'var1':'variable field 1',
    'var2':'variable field 2',
    'var3':'variable field 3'
}

mail = TextMail(filename='mydb.csv', type='plain')

mail.set_email_field('Email Address')
mail.set_subject(subject)
mail.set_template('template.txt')
mail.add_variables(variables)

mail.send()
```

Apparently you can ignore the `set_email_field`, `set_template` and `set_subject` method and set them up while initializing the class.

```python
from bulkmail import TextMail

subject = "An email"
variables = {
    'var1':'variable field 1',
    'var2':'variable field 2',
    'var3':'variable field 3'
}

mail = TextMail(
    filename='mydb.csv',
    type='plain',
    template='template.txt',
    email_field='Email Address',
    subject=subject
)

mail.add_variables(variables)

mail.send()
```

For all cases, make sure to have `.env` file with `SMTP_HOST`, `SMTP_PORT`, `SENDER_EMAIL` and `SENDER_PASSWORD` keys with their correct value present. Or initiate them using `bulkmail defaults` command.



## Miscellaneous

The following demo csv database will be used all over this documentation.

```
Full Name,Date of Birth,Citizenship,Contact No.,Email Address
Mr. A,18/10/1988,Yes,+8801911111111,a@gmail.com
Mr. B,18/11/1988,No,+8801911111112,b@gmail.com
Mr. C,18/12/1988,Yes,+8801911111113,c@gmail.com
```

### Templating

Templates will be parsed to `text`/`html` after replacing variables related per person and will be sent. Here goes a sample template related to the demo csv file-

```
Dear <name>,

This is to let you know that we are rechecking our database.
Your provided birthdate is <date> and contact is <contact>. Let us know if they are correct or not.

Thank you
```

The parts wrapped with angular braces (`<>`) will be replaced by the info provided in csv.

### Email Field

`Email Field` aka `email_field` refers to the fieldname in the csv file which contains the receivers' email addresses. For the given aforementioned csv it is `Email Address`.

### Variables

Variables are basically the changeable parts in the template. `name`, `date` and `contact` are variables wrapped inside `<>` in the aforementioned template. 

So the idea is- you will mention the variable name first and then the field that refers to this variable. Regarding the template and csv given, the variables and fieldnames are connected like below-

`name` - `Full Name`
`date` - `Date of Birth`
`contact` - `Contact No.`

#### Setting up variables

1. **For CLI**-
   Type `y` when prompted that if you want to use variables or not. Then input the number of variables you want to add. Then type variable name first and then field name when prompted. The whole thing will look like below for the given template and database-

   ```
   Do you want to use variables? [y/N]: y
   Number of variable fields: 3
   Variable no. 1
   Variable Name: name
   Fieldname: Full Name
   Variable no. 2
   Variable Name: contact
   Fieldname: Contact No.
   Variable no. 3
   Variable Name: date
   Fieldname: Date of Birth
   ```

   CLI prompts will be the same for both `sendmail` and `sendtemp` command.

2. **For Application**-
   In this case, you will have to create a dictionary and use the `add_variables` method for adding variables to your `TextMail` object.

   ```python
   from bulkmail import TextMail
   
   variables = {
       'name':'Full Name',
       'contact':'Contact No.',
       'date':'Date of Birth'
   }
   
   mail = TextMail(
       filename='mydb.csv',
       type='plain',
       template='template.txt',
       email_field='Email Address',
       subject=subject
   )
   
   mail.add_variables(variables)
   ```



**Note:  If your variables contains a field name that is not present in the csv file, it will raise an error.**





# For Contributors

The following part is for contributors who want to contribute to this package.

## To-do

1. Add function based variables
2. Add robust template system
3. Updates on CLI emails
4. Sending Attachments
5. Resume Capability
6. API Based Login for Gmail
7. Fix DRY violations

## Bugs

* Subjects can use variables but only for the first email. That remains constant for the rest of the database.
* Shows the `smtplib.SMTPServerDisconnected: please run connect() first`  error sometimes. Gets fixed after restarting Command Prompt or changing directory.
