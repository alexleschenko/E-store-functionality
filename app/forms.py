#coding=utf-8
from django import forms

class UserForm(forms.Form):
    choices = ('byn', 'BYN'), ('byr', 'BYR')

    order = forms.CharField(label='Что купить', max_length=100)
    person = forms.CharField(label="Кому", max_length=100)
    email = forms.EmailField(label='Email')
    payment_value = forms.FloatField(label='Сумма')
    payment_method= forms.ChoiceField(label='Валюта', choices=choices)
    comment = forms.CharField(label="Комментарии", widget=forms.Textarea, required=False)

class Login(forms.Form):
    user = forms.CharField(label='user', max_length=100)
    password = forms.CharField(label='password', max_length=100, widget=forms.PasswordInput)

class Update(forms.Form):
    choices = ('byn', 'BYN'), ('byr', 'BYR')
    order = forms.CharField(label='Что купить', max_length=100)
    person = forms.CharField(label="Кому", max_length=100)
    email = forms.EmailField(label='Email')
    payment_value = forms.FloatField(label='Сумма')
    payment_method = forms.ChoiceField(label='Валюта', choices=choices)
    comment = forms.CharField(label="Комментарии", widget=forms.Textarea, required=False)