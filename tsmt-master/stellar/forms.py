from django import forms
from django.forms import ModelForm
from .models import Contact, Accounts, Feedbacks
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        #exclude = ['user_name']
        fields = ('contact', 'address', 'memo',)
class AccountForm(ModelForm):
    class Meta:
        model = Accounts
        fields = ('user_name', 'name', 'address', 'seed',)
class FeedbacksForm(forms.ModelForm):
    class Meta:
        model = Feedbacks
        fields = ( 'Name', 'Email','Subject','Message')