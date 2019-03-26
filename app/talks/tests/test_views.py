from django import test
from django.urls import reverse

from auth_custom.models import User
from talks.models import PrivateMessage, PublicMessage


class TalksViewTest(test.TransactionTestCase):
    fixtures = [
        'users.json', 'messages.json', 'friendship_requests.json',
        'friends.json'
    ]

    def setUp(self):
        self.client = test.Client()
        self.client.login(username='user', password='pass')

    def test_not_logged_user(self):
        not_logged_client = test.Client()
        kwargs = {'receiver_name': 'global', 'page_num': 1}
        talks_url = reverse('talks:talk', kwargs=kwargs)
        response = not_logged_client.get(talks_url, folow=True)
        query_params = f'?next={talks_url}'
        redirect_url = f'{reverse("auth_custom:login")}{query_params}'
        self.assertRedirects(response, redirect_url)

    def test_logged_user(self):
        kwargs = {'receiver_name': 'global', 'page_num': 1}
        url = reverse('talks:talk', kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'talks/base.html')

    def test_contacts_list(self):
        kwargs = {'receiver_name': 'global', 'page_num': 1}
        url = reverse('talks:talk', kwargs=kwargs)
        response = self.client.get(url)
        contacts = [
            User.objects.get(username='alex'),
            User.objects.get(username='bob'),
            User.objects.get(username='john')
        ]
        self.assertEqual(response.context['contacts'], contacts)

    def test_messages(self):
        kwargs = {'receiver_name': 'john', 'page_num': 1}
        url = reverse('talks:talk', kwargs=kwargs)
        response = self.client.get(url)
        messages = [
            PrivateMessage.objects.get(text__contains='Hello, john!'),
            PrivateMessage.objects.get(text__contains='Hi, user!')
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['dialog_messages'], messages)

    def test_friends(self):
        kwargs = {'receiver_name': 'john', 'page_num': 1}
        url = reverse('talks:talk', kwargs=kwargs)
        response = self.client.get(url)
        friends = [
            User.objects.get(username='alex')
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['friends'], friends)

    def test_global_messages(self):
        kwargs = {'receiver_name': 'global', 'page_num': 1}
        url = reverse('talks:talk', kwargs=kwargs)
        response = self.client.get(url)
        messages = [
            PublicMessage.objects.get(text__contains="It's user"),
            PublicMessage.objects.get(text__contains="It's alex")
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['dialog_messages'], messages)
