import random
from django.core.email import EmailMessage

def generate_otp():
    return "".join(([str(random.randint(0, 9)) for i in range(6)]))
