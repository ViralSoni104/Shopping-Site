from django.core.validators import RegexValidator
from django import forms
from .models import Contact


alphabet_validate=RegexValidator(r'[A-Za-z]+',"Name must be in aphabets only.")
class ContactForm(forms.ModelForm):
    contact_name=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'common-input mt-20'}),validators=[alphabet_validate])
    class Meta:
        model=Contact
        fields=['contact_name','contact_email','message']