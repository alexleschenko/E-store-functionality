from django.test import TestCase
from models import *
from django.contrib.auth.models import User
# Create your tests here.
class ProjectTest(TestCase):

    def test_ok_add_order(self):
        data = {'order':'data', 'person':'person', 'email':'mail@mail.com', 'payment_value':1000, 'payment_method':'byn', 'comment':'blablabla'}
        User.objects.create_user('admin', 'lennon@the.com', 'testpassword')
        self.client.post('', data)
        q_data = UserDB.objects.filter()
        self.assertEquals(q_data.count(), 1)
