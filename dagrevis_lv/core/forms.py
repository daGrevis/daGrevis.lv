from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField()
    message = forms.CharField()
