from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

class Util:
  

    @staticmethod
    def send_forgot_passord_email(data):
        """ Sends the new password to the user who forgot password """

        user = data['user']
        password = data['password']
        email = data['email']

        domain = 'localhost:3000'
        if 'localhost' not in str(data['site']):
            domain = 'rapihire.com'


        html_message = render_to_string('accounts/forgot_password.html', {
                'user': user,
                'password':password,
                'domain':domain,
            })

        email_subject='Reset your password'

        message = EmailMessage(
            email_subject,
            html_message,
            None,
            [email],
        )
        message.content_subtype = 'html'
        message.send()



    