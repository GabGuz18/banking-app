from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger


def send_otp(email, otp):
    subject = _("Your OTP code for Login")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        "otp": otp,
        "expiry_time": settings.OTP_EXPIRATION,
        "site_name": settings.SITE_NAME,
    }
    html_message = render_to_string("emails/otp_email.html", context)
    plain_email = strip_tags(html_message)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")
    try:
        email.send()
        logger.info(f"OTP email sent successfully to {email}")
    except Exception as e:
        logger.error(f"Error to send OTP code to {email}. Error: {str(e)}")


def send_account_blocked(self):
    subject = _("Your account has been blocked")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [self.email]
    context = {
        "user": self,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds() // 60),
        "site_name": settings.SITE_NAME,
    }
    html_message = render_to_string("emails/account_blocked.html", context)
    plain_email = strip_tags(html_message)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")
    try:
        email.send()
        logger.info(f"Account blocked email sent to {self.email}")
    except Exception as e:
        logger.error(
            f"Failed to send the account blocked email to {email}. Error: {str(e)}"
        )
