from csv import DictReader, DictWriter
import re

def const_replacer(text:str, constants:dict):
    text = text
    for i in constants.keys():
        text = re.sub(f'<{i}>', constants[i], text)

    return text

def var_replacer(text:str, variables:dict, row:dict):
    text = text
    for i in variables.keys():
        text = re.sub(f'<{i}>', row[variables[i]], text)

    return text

def cache(original:str, template:str, variables:dict, constants:dict, subject:str, email_field:str):
    # user input texts
    original = open(original, 'r', encoding='utf-8')
    template = open(template, 'r', encoding='utf-8')
    _body = template.read()
    
    subject = const_replacer(subject, constants)
    body = const_replacer(_body, constants)

    database = DictReader(original)

    # cache info
    cachedb = open('cache(do not delete).csv', 'w', encoding='utf-8')
    cacheheaders = ['email', 'subject', 'body']
    cachedatabase = DictWriter(cachedb, fieldnames=cacheheaders)
    cachedatabase.writeheader()

    # making cache
    for row in database:
        cachedatabase.writerow({
            'email':row[email_field],
            'subject':var_replacer(subject, variables, row),
            'body':var_replacer(body, variables, row)
        })
    
    original.close()
    template.close()
    cachedb.close()

    return 'cache(do not delete).csv'