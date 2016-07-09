#coding=utf-8
from django import forms

class UserForm(forms.Form):
    # order = models.CharField(max_length=100)
    # person = models.CharField(max_length=100)
    # email = models.EmailField()
    # pay_BYR = models.IntegerField(null=True)
    # pay_BNR = models.FloatField(null=True)
    # comment = models.CharField(null=True, max_length=300)
    choices = 'BYR', 'BNR'

    order = forms.CharField(label='Что купить', max_length=100)
    person = forms.CharField(label="Кому", max_length=100)
    email = forms.EmailField(label='Email')
    payment_method = forms.ChoiceField(label='Валюта', choices=choices)
    payment_value = forms.FloatField(label='Сумма')
    comment = forms.CharField(label="Комментарии", widget=forms.Textarea)