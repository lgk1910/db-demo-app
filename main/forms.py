from collections import defaultdict
from django import forms
from datetime import date
from django import forms
from django.forms.widgets import NumberInput

class InserCardInfo(forms.Form):
    card_code = forms.IntegerField()
    owner_name = forms.CharField(max_length=255)
    expired_date = forms.DateField(label="Date", required=True, widget=NumberInput(attrs={'type':'date'}))
    branch_name = forms.CharField(max_length=255) 
    bank = forms.CharField(max_length=255)
    cvv = forms.IntegerField(label='CVV')

class Quantity(forms.Form):
    quantity = forms.IntegerField()

class DateForm(forms.Form):
    date = forms.DateField(label="Date", required=True, widget=NumberInput(attrs={'type':'date'}))