from celery import shared_task
from accounts.models import CustomUser
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_verification_mail_async(user_id, token):
    user= CustomUser.objects.get(id=user_id)
    subject=' Verify your email'
    verification_url = f"http://localhost:8000/api/verify-email/?token={token}"
    message= f"Hi {user.email},\n\nPlease click the link below to verify your email address:\n{verification_url}\n\nThank you!"
    from_email= settings.DEFAULT_FROM_EMAIL
    reciepient_list= [user.email]

    send_mail(subject, message, from_email, reciepient_list)