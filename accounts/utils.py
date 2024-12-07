from functools import wraps

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def anonymous_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(
                "accounts:dashboard"
            )  # Replace 'home' with your desired redirect URL name
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def send_activation_email(request, user, email_template, mail_subject):
    # Set the sender email address
    from_email = settings.DEFAULT_FROM_EMAIL

    # Get the current site (domain)
    current_site = get_current_site(request)

    # Render the email template with the context
    message = render_to_string(
        email_template,
        {
            "user": user,
            "domain": current_site,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": default_token_generator.make_token(user),
        },
    )
    # Set the recipient's email address
    to_email = user.email
    # Create the email message
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    # Set the content type to HTML
    mail.content_subtype = "html"
    # Send the email
    mail.send()
