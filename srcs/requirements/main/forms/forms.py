from django.core.mail import send_mail
from django import forms
from django.conf import settings


class ContactForm(forms.Form):

    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    inquiry = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email').strip()
        subject = cl_data.get('inquiry')

        msg = f'{name} with email {from_email} said:\n\n{cl_data.get("message")}'

        return subject, msg, from_email

    def send(self):

        subject, msg, email = self.get_info()
        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email]
        )
