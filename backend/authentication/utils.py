import random

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import OneTimePassword


def generate_otp():
    return "".join(([str(random.randint(0, 9)) for _ in range(6)]))


def send_code_to_user(email, resending=False):
    from .models import CustomUser

    user = CustomUser.objects.get(email=email)

    SUBJECT = "One time passcode for email verification"
    if resending:
        BODY = f"""
        Thank you {user.first_name.capitalize()} for registering to
        the book management application!
        """
    else:
        BODY = """
        We resend you this email to enable you to register
        to the book management application!
        """

    OTP_CODE = generate_otp()
    PASSCODE_PART = f"Please verify your email with your one time passcode: {OTP_CODE}"

    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=OTP_CODE)

    send_email = EmailMessage(
        subject=SUBJECT,
        body="\n".join([BODY, PASSCODE_PART]),
        from_email=from_email,
        to=[email],
    )

    send_email.send(fail_silently=False)


def generate_password_reset_tokens(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)

    return uid, token


def send_password_reset_email(user, uid, token, request):
    site_domain = settings.DOMAIN_NAME
    relative_link = reverse(
        "password-reset-confirm", kwargs={"uid": uid, "token": token}
    )
    abs_link = f"http://{site_domain}{relative_link}"

    subject = "Password Reset Request"
    message = f"""
        Hello {user.first_name.capitalize()}!
        Use this link to reset your password:\n{abs_link}
    """
    from_email = settings.DEFAULT_FROM_EMAIL

    send_email = EmailMessage(
        subject=subject, body=message, from_email=from_email, to=[user.email]
    )

    send_email.send(fail_silently=False)
