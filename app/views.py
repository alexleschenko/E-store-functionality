import arrow
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
