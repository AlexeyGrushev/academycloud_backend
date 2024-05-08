import random


def generate_password(lenght: int) -> str:
    chars = "abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    password = ""
    for i in range(lenght):
        password += random.choice(chars)
    return password
