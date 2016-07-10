# coding=utf-8
import arrow
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from forms import *
from models import *


# Create your views here.
def order(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            UserDB.objects.create(order=data['order'], person=data['person'], email=data['email'],
                                  comment=data['comment'],
                                  pay_value=data['payment_value'], pay_method=data['payment_method'])

            return HttpResponse('done')
        else:
            context = {'my_form': form}
            return render(request, 'user_form.html', context)
    else:
        time = arrow.now()
        time = time.format('HH')
        if time == '13' or time == '14':
            access = True
        else:
            access = False
        context = {'my_form': UserForm(), 'access': access}
        return render(request, 'user_form.html', context)


def admin(request):
    if request.user.is_authenticated():
        if request.GET.items():
            action = request.GET.get('action')
            id = request.GET.get('id')
            if action == 'del':
                UserDB.objects.filter(id=id).delete()
                return redirect('admin')

        else:
            data = UserDB.objects.filter()
            data_byn = UserDB.objects.filter(pay_method='byn')
            value_byn = 0
            for i in data_byn:
                value_byn = value_byn + i.pay_value
            data_byr = UserDB.objects.filter(pay_method='byr')
            value_byr = 0
            for i in data_byr:
                value_byr = value_byr + i.pay_value
            summ = value_byn + value_byr/10000
            context = {'my_data': data, 'byn':value_byn, 'byr': value_byr, 'sum':summ}
            return render(request, 'admin_list.html', context)
    else:
        return redirect('login')


def login_site(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['user']
            password = data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin')
            else:
                request.session['login'] = 'Неверный логин/пароль'
                return redirect('login')
        else:
            request.session['login'] = 'Неверный логин/пароль'
            return redirect('login')

        context = {'my_form': form}
        return render(request, 'login.html', context)
    else:
        data = ''
        if request.session.has_key('login'):
            data = request.session.get('login')
            del request.session['login']
        context = {'my_form': Login(), 'login_data': data}
        return render(request, 'login.html', context)


def logout_site(request):
    logout(request)
    return redirect('login')


def update(request):
    if request.method == 'POST':
        form = Update(request.POST)

        if request.session.has_key('data'):
            id = request.session.get('data')
        del request.session['data']
        if form.is_valid():
            data = form.cleaned_data
            UserDB.objects.filter(id=id).update(order=data['order'], comment=data['comment'])
            return redirect('admin')
        context = {'my_form': form}
        return render(request, 'update.html', context)
    else:
        id = request.GET.get('id')
        predata = UserDB.objects.filter(id=id).get()
        request.session['data'] = id
        context = {'my_form': Update(initial={'order': predata.order, 'comment': predata.comment})}
        return render(request, 'update.html', context)
