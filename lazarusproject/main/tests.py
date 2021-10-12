from django.test import TestCase, RequestFactory
# from models import Table, Meetings
from django.contrib.auth.models import User
from .views import UserLoginView
from django.utils import timezone


class MainTestCases(TestCase):

    # def setUp(self) -> None:
        # self.user = User.objects.create_user(username='testuser', password='test')
        # self.table = Table.objects.create(userID=self.user, title='test_sneaker', datebuy=timezone.now().date(), )

    def test_login(self):
        factory = RequestFactory()
        request = factory.get('')
        response = UserLoginView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/inventory/')

# Create your tests here.
