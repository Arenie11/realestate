from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status

def SendMail(email):
    subject = "Welcome to Real Estate website"
    message = f'''
                This is we saying a big welcome to you. 
                Thanks for registering
                '''
    
    send_mail(
    subject,
    message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently= False,
)
    
    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)