from forms import *
from models import *
from django.http import HttpResponse
from django.shortcuts import render

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
            context = {'my_form':form}
            return render(request, 'user_form.html', context)
    else:
        context = {'my_form':UserForm()}
        return render(request, 'user_form.html', context)

