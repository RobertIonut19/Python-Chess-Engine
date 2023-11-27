import string
import random

def generate_password(length=8, include_special = True, include_numbers = True, include_uppercase = True):
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    numbers = string.digits
    special = string.punctuation


    all_chars = lowercase + uppercase + numbers + special

    password = ''

    len = length
    for i in range(len):
        if length != 0:
            password += random.choice(lowercase)
            length -= 1
        if length != 0 and include_uppercase == 'y':
            password += random.choice(uppercase)
            length -= 1
        if length != 0 and include_numbers == 'y':
            password += random.choice(numbers)
            length -= 1
        if length != 0 and include_special == 'y':
            password += random.choice(special)
            length -= 1
        if length == 0:
            break
    return password