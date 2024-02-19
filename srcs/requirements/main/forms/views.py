from django.views.generic import FormView, TemplateView
from forms.forms import ContactForm
from django.urls import reverse_lazy


# Create your views here.
class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('forms:success')

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    template_name = 'success.html'
