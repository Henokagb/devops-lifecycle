import re


def validMail(mail):
    if re.match('^(?!.*[-_.]{2})[\w\-_.&]*[\@][\w\-]*[\w+\.]*[\.][a-zA-Z]+', mail):
        return True
    return False


def validUsername(username):
    if re.match('^[A-Za-z]+$', username):
        return True
    return False

def validProfession(profession):
    if re.match('^[A-Za-z ]+$', profession):
        return True
    return False

def validAge(age):
    return age < 16 < 55