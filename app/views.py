#coding=utf-8
import arrow
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

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
            context = {'my_data': data}
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

        context = {'my_form':form}
        return render(request, 'login.html', context)
    else:
        data=''
        if request.session.has_key('login'):
            data = request.session.get('login')
            del request.session['login']
        context = {'my_form':Login(), 'login_data':data}
        return render(request, 'login.html', context)

def logout_site(request):
    logout(request)
    return redirect('login')



