import threading
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.template import TemplateDoesNotExist

def send_email_thread(full_name, email, phone, subject, message):
    try:
        html_message = render_to_string('emails/contact_email.html', {
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'message': message,
        })

        email_subject = f"New Contact Form Submission - {subject.title()}"
        to_email = settings.DEFAULT_CONTACT_EMAIL

        email_message = EmailMessage(
            subject=email_subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email],
        )
        email_message.content_subtype = 'html'
        email_message.send(fail_silently=False)
        print("Email sent successfully!")

    except TemplateDoesNotExist as e:
        print("TEMPLATE NOT FOUND:", e)

    except Exception as e:
        print("Email send error:", e)


def send_contact_email_form(full_name, email, phone, subject, message):
    email_thread = threading.Thread(
        target=send_email_thread,
        args=(full_name, email, phone, subject, message)
    )
    email_thread.start()
    return True
