from rest_framework_simplejwt.tokens import RefreshToken

def get_email_veriification_token(user):
    refresh= RefreshToken.for_user(user)
    return str(refresh.access_token)

from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user, token):
    subject=' Verify your email'
    verification_url = f"http://localhost:8000/api/verify-email/?token={token}"
    message= f"Hi {user.email},\n\nPlease click the link below to verify your email address:\n{verification_url}\n\nThank you!"
    from_email= settings.DEFAULT_FROM_EMAIL
    reciepient_list= [user.email]

    send_mail(subject, message, from_email, reciepient_list)