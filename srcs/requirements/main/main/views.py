from django.utils.translation import activate
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from account.models import User
from .forms import PasswordResetForm
from django.conf import settings
import base64


def set_language(request):
    language = request.POST.get('language')
    if language is not None:
        activate(language)
        request.language = language
        request.session['django_language'] = language
    if request.META.get('HTTP_REFERER') is not None:
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('/')


def handler404(request, *args, **argv):
    return render(request, '404.html', status=404)


def base64_encode(value: str) -> str:
    encoded = base64.urlsafe_b64encode(str.encode(value))
    result = encoded.rstrip(b"=")
    return result.decode()


class PasswordResetMyView(FormView):
    template_name = "password/reset_form.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("password_reset_done")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = base64_encode(str(user.id))
        current_site = get_current_site(self.request)
        subject = "NO REPLY"
        message = render_to_string("password/reset_email.html", {
            "user": user,
            "protocol": self.request.scheme,
            "domain": current_site.domain,
            "uid": uid,
            "token": token,
        })
        print(f"uid {uid} token {token}")
        send_mail(subject, message, f"ft_transcendence {settings.EMAIL_HOST_USER}", [email])
        return super().form_valid(form)


def changelog(request):
    return render(request, 'changelog.html')
