from django.core.mail import send_mail
from django.conf import settings
from backends_engine.abstract_classes import EmailSender


class SMTPEmailSender(EmailSender):
    def send_email(self, subject, message, recipient_list, from_email=None):
        if from_email is None:
            from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, recipient_list)
