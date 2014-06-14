from django import forms

from captcha.fields import ReCaptchaField


class ContactForm(forms.Form):
    email = forms.EmailField()
    message = ReCaptchaField()
