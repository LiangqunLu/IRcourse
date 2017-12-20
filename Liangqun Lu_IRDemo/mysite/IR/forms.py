
from django import forms

class NameForm(forms.Form):
    IRsearch = forms.CharField(max_length=100)
