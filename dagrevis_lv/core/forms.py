from django import forms


class FreelanceForm(forms.Form):
    client_email = forms.EmailField()
    message = forms.CharField()
