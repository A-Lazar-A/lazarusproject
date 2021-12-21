from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Table, Meetings

User = get_user_model()


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/login.html')

    def test_sign_up_view(self):
        response = self.client.get(reverse('sign-up'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/sign-up.html')

    def test_login_redirect(self):
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 302)

    def test_inventory_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/index.html')

    def test_meetings_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('meetings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/meetings.html')


    def test_statistic_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('statistic'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/statistic.html')


class TestUser(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = {
            'username': 'test',
            'password': '12345'
        }

    def test_registration_login(self):
        response = self.client.post(reverse('sign-up'), self.user)
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('login'), self.user)
        self.assertEqual(response.status_code, 302)


class TestCreateViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='testuser')
        self.user.set_password('12345')
        self.user.save()
        self.client.login(username='testuser', password='12345')
        self.item1 = {
            'title': 'test',
            'size': 'NO SIZE',
            'currencyprice': 1200,
            'currencybuy': '₽',
            'currencysell': '₽',
            'currencysellprice': 0,
            'anyprice': 0,
            'datebuy': '2021-11-17',
            'notes': '',
            'extra': '1',
            'datesell': ''
        }
        self.item2 = {
            'title': 'test',
            'size': 'NO SIZE',
            'currencyprice': 1200,
            'currencybuy': 'BUSD',
            'currencysell': 'BUSD',
            'currencysellprice': 1400,
            'anyprice': 0,
            'datebuy': '2021-11-17',
            'notes': '',
            'extra': '1',
            'datesell': '2021-11-17'
        }
        self.item3 = {
            'title': 'test',
            'size': 'NO SIZE',
            'currencyprice': 2,
            'currencybuy': 'SOL',
            'currencysell': 'SOL',
            'currencysellprice': 5,
            'anyprice': 0,
            'datebuy': '2021-11-17',
            'notes': '',
            'extra': '1',
            'datesell': '2021-11-17'
        }
        self.item4 = {
            'title': 'test',
            'size': 'NO SIZE',
            'currencyprice': 0.2,
            'currencybuy': 'ETH',
            'currencysell': 'SOL',
            'currencysellprice': 1,
            'anyprice': 0,
            'datebuy': '2021-11-17',
            'notes': '',
            'extra': '1',
            'datesell': '2021-11-17'
        }
        self.item5 = {
            'title': 'test',
            'size': 'NO SIZE',
            'currencyprice': 0.2,
            'currencybuy': 'SOL',
            'currencysell': 'ETH',
            'currencysellprice': 1,
            'anyprice': 0,
            'datebuy': '2021-11-17',
            'notes': '',
            'extra': '1',
            'datesell': '2021-12-20'
        }
        self.meeting = {
            'title': 'test',
            'price': 4000,
            'currency': '₽',
            'datemeeting': '2021-11-18T03:15',
            'notes': ''
        }
        self.meeting2 = {
            'title': 'test',
            'price': 4000,
            'currency': 'SOL',
            'datemeeting': '2021-11-18T03:15',
            'notes': ''
        }
        self.meeting3 = {
            'title': 'test',
            'price': 4000,
            'currency': 'ETH',
            'datemeeting': '2021-11-18T03:15',
            'notes': ''
        }
        self.meeting4 = {
            'title': 'test',
            'price': 4000,
            'currency': 'BUSD',
            'datemeeting': '2021-11-18T03:15',
            'notes': ''
        }
        self.meeting_add1 = {

            'price': 4000,
            'currency': 'BUSD',
            'meet': 1
        }
        self.meeting_add2 = {

            'price': 4000,
            'currency': 'SOL',
            'meet': 1
        }
        self.meeting_add3 = {

            'price': 4000,
            'currency': 'ETH',
            'meet': 1
        }

        self.sold = {
            'currencysellprice': 1,
            'datesell': '2021-12-21',
            'currencysell': 'ETH',
            'notes': ''
        }

    def test_create_edit_delete_item(self):
        response = self.client.post(reverse('item-create'), self.item1)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item2)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item3)
        self.assertEqual(response.status_code, 302)
        print(Table.objects.all()[0].id)
        response = self.client.post('/edit/9', self.item2)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Table.objects.get(id=9).currencyprice, 1200)
        response = self.client.post('/edit/10', self.item4)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/edit/11', self.item5)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item4)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Table.objects.filter(userID=self.user).all().count(), 4)
        response = self.client.post('/delete/12')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/sold/11', self.sold)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Table.objects.filter(userID=self.user).all().count(), 3)

    def test_create_add_delete_meeting(self):
        response = self.client.post(reverse('item-create'), self.item1)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item2)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item3)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item4)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item5)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item5)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item5)
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('item-create'), self.item5)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/meeting-create/5', self.meeting)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/meeting-create/6', self.meeting2)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/meeting-create/7', self.meeting3)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/meeting-create/8', self.meeting4)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/meeting-add/5', self.meeting_add1)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/meeting-add/6', self.meeting_add2)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/meeting-add/7', self.meeting_add3)
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/meeting-delete/1')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/meeting-done/4')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Meetings.objects.filter(userID=self.user).all().count(), 2)

