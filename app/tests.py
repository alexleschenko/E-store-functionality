#coding=utf-8
import json

from django.core import serializers
from django.http.response import HttpResponse
from django.test import TestCase
from mock import patch

from views import *


def new_render(a, b, c):
    c['my_data'] = serializers.serialize('json', c['my_data'])
    result = json.dumps(c)
    return HttpResponse(result)


# Create your tests here.
class ProjectTest(TestCase):
    def test_ok_add_order(self): #тест добавление
        data = {'order': 'data', 'person': 'person', 'email': 'mail@mail.com', 'payment_value': 1000,
                'payment_method': 'byn', 'comment': 'blablabla'}
        User.objects.create_user('admin', 'lennon@the.com', 'testpassword')
        self.client.post('', data)
        q_data = UserDB.objects.filter()
        self.assertEquals(q_data.count(), 1)
        order = q_data.get()
        self.assertEquals(order.order, data['order'])
        self.assertEquals(order.person, data['person'])
        self.assertEquals(order.email, data['email'])
        self.assertEquals(order.pay_method, data['payment_method'])
        self.assertEquals(order.pay_value, data['payment_value'])
        self.assertEquals(order.comment, data['comment'])

    def test_ok_update(self): #тест обновление
        User.objects.create_user('admin', 'lennon@the.com', 'testpassword', is_active=True)
        self.client.login(username='admin', password='testpassword')
        UserDB.objects.create(order='order', person='person', email='email@email.com', pay_value=100, pay_method='byn',
                              comment='blablabla')
        order = UserDB.objects.filter().last()
        self.client.get('/admin_page/update/', {'id': order.id})
        data = {'order': 'data', 'person': 'person', 'email': 'mail@mail.com', 'payment_value': 1000,
                'payment_method': 'byn', 'comment': 'bla'}
        self.client.post('/admin_page/update/', data)
        order = UserDB.objects.filter().get()
        self.assertEquals(order.order, data['order'])
        self.assertEquals(order.comment, data['comment'])

    def test_ok_delete(self): # тест удаление
        User.objects.create_user('admin', 'lennon@the.com', 'testpassword', is_active=True)
        self.client.login(username='admin', password='testpassword')
        UserDB.objects.create(order='order', person='person', email='email@email.com', pay_value=100, pay_method='byn',
                              comment='blablabla')
        order = UserDB.objects.filter().last()
        self.client.get('/admin_page/', {'id': order.id, 'action': 'del'})
        q_order = UserDB.objects.filter()
        self.assertEquals(q_order.count(), 0)

    def test_ok_sum_payment(self): #тест подсчета суммы
        with patch('app.views.render', new=new_render):
            User.objects.create_user('admin', 'lennon@the.com', 'testpassword', is_active=True)
            self.client.login(username='admin', password='testpassword')
            UserDB.objects.create(order='order', person='person', email='email@email.com', pay_value=100,
                                  pay_method='byn',
                                  comment='blablabla')
            UserDB.objects.create(order='order', person='person', email='email@email.com', pay_value=10000,
                                  pay_method='byr',
                                  comment='blablabla')
            result = self.client.get('/admin_page/')
            data = json.loads(result.content)
        self.assertEquals(data['sum'], 101)
