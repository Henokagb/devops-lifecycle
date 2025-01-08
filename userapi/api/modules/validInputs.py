import re

def validMail(mail):
    if re.match('^(?!.*[-_.]{2})[\w\-_.&]*[\@][\w\-]*[\w+\.]*[\.][a-zA-Z]+', mail):
        return True
    return False


def validname(name):
    if re.match('^[A-Za-z]+$', name):
        return True
    return False

def validProfession(profession):
    if re.match('^[A-Za-z ]+$', profession):
        return True
    return False

def validAge(age):
    return 16 < age <= 60