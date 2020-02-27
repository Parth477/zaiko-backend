from celery.task import task
from django.core.mail import EmailMultiAlternatives


from django.template.loader import render_to_string


@task(name='zaiko.send_verification_email')
def send_email_task(client_email,key):
    text = "Click this link to verify your email..."
    html_content = render_to_string('verified_email.html', {'key': "http://localhost:8000/api/v1/customer/verify-email/"+ key})
    msg = EmailMultiAlternatives('Invitation Link from Parth',text,'harrydeaol@gmail.com',[client_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return None
