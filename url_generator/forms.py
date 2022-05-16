from django import forms


class user_form(forms.Form):
    domain = forms.CharField()