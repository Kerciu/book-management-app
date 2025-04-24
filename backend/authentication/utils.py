from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import smart_bytes
import random
from django.core.mail import EmailMessage
from django.conf import settings
from .models import CustomUser, OneTimePassword

def generate_otp():
    return "".join(([str(random.randint(0, 9)) for i in range(6)]))

def send_code_to_user(email, resending = False):
    user = CustomUser.objects.get(email=email)

    SUBJECT = "One time passcode for email verification"
    if resending:
        BODY = f"Thank you {user.first_name.capitalize()} for registering to the book management application!"
    else:
        BODY = f"We resend you this email to enable you to register to the book management application!"
        
    OTP_CODE = generate_otp()
    PASSCODE_PART = f"Please verify your email with your one time passcode: {OTP_CODE}"

    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(
        user=user,
        code=OTP_CODE
    )

    send_email = EmailMessage(
        subject=SUBJECT,
        body='\n'.join([BODY, PASSCODE_PART]),
        from_email=from_email,
        to=[email]
    )

    send_email.send(fail_silently=False)

def generate_password_reset_tokens(user):
    uid = urlsafe_base64_encode(smart_bytes(user))
    token = PasswordResetTokenGenerator().make_token(uid)

    return uid, token
