from django.urls import path
from .views import ContactView, ContactSuccessView

app_name = 'forms'

urlpatterns = [
    path('forms/', ContactView.as_view(), name="forms"),
    path('success/', ContactSuccessView.as_view(), name="success"),
]
