from django import test
from django.urls import reverse
from django.utils import html

from auth_custom.models import User


class RegisterViewTest(test.TestCase):
    def setUp(self):
        super().setUp()
        self.client = test.Client()

    def test_get_register_page(self):
        response = self.client.get(
            reverse('auth_custom:register')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_custom/register.html')

    def test_register_success_redirect(self):
        response = self.client.post(
            reverse('auth_custom:register'),
            {
                'username': 'u',
                'password1': 'p',
                'password2': 'p',
            },
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('auth_custom:login'),
            status_code=302,
            target_status_code=200
        )

    def test_register_success_message(self):
        response = self.client.post(
            reverse('auth_custom:register'),
            {
                'username': 'u',
                'password1': 'p',
                'password2': 'p'
            },
            follow=True
        )
        self.assertContains(response, 'User u was successfully created!')

    def test_register_user_already_exists(self):
        User.objects.create_user(
            username='u',
            password='p'
        )
        response = self.client.post(
            reverse('auth_custom:register'),
            {
                'username': 'u',
                'password1': 'pp',
                'password2': 'pp'
            }
        )
        self.assertContains(
            response,
            'A user with that username already exists.'
        )

    def test_register_passwords_did_not_match(self):
        response = self.client.post(
            reverse('auth_custom:register'),
            {
                'username': 'u',
                'password1': 'p',
                'password2': 'pp'
            }
        )
        self.assertContains(
            response,
            html.escape("The two password fields didn't match.")
        )

    def test_register_invalid_username(self):
        for char in '~`#$;%^&?*()={}[]:\'\",<>\|':
            response = self.client.post(
                reverse('auth_custom:register'),
                {
                    'username': f'u{char}',
                    'password1': 'p',
                    'password2': 'p'
                }
            )
            self.assertContains(
                response,
                html.escape(
                    'Enter a valid username. This value may contain '
                    'only letters, numbers, and @/./+/-/_ characters.'
                )
            )


class LoginViewTest(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_get_login_page(self):
        response = self.client.get(
            reverse('auth_custom:login')
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('auth_custom/login.html')

    def test_login_success_redirect(self):
        User.objects.create_user(
            username='u',
            password='p'
        )
        response = self.client.post(
            reverse('auth_custom:login'),
            {
                'username': 'u',
                'password': 'p'
            },
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('pages:page', kwargs={'username': 'u'}),
            status_code=302,
            target_status_code=200
        )

    def test_login_error_message(self):
        response = self.client.post(
            reverse('auth_custom:login'),
            {
                'username': 'u',
                'password': 'p'
            }
        )
        self.assertContains(
            response,
            html.escape(
                'Please enter a correct username and password. '
                'Note that both fields may be case-sensitive.'
            )
        )

    def test_login_user_in_session(self):
        user = User.objects.create_user(
            username='u',
            password='p'
        )
        response = self.client.post(
            reverse('auth_custom:login'),
            {
                'username': 'u',
                'password': 'p'
            }
        )
        session_user_id = int(self.client.session['_auth_user_id'])
        self.assertEqual(session_user_id, user.pk)
