from django.utils import unittest
from django.core.urlresolvers import reverse
from django.test.client import Client
from ..models import RegistrationLink
from ..views import check_registration_link


class TestUrlAccess(unittest.TestCase):
    urls = 'urls'
    code = "foo"

    def setUp(self):
        # Create a valid registration link
        reg = RegistrationLink.objects.create(code=self.code, use_threshold=2)
        self.reg = reg
        self.client = Client()
        # Reverse the correct URL using registration code
        self.correct_link = reverse(check_registration_link, args=[self.code, ])

    def tearDown(self):
        # Remove registration link from DB
        RegistrationLink.objects.filter(code=self.code).delete()

    def test_not_authorized(self):
        """Access a registration page without using the registration link"""
        url = reverse('registration_register')
        response = self.client.get(url, follow=True)
        self.assertTrue('accounts/register/closed' in response.redirect_chain[0][0])

    def test_wrong_link(self):
        """Access a wrong registration link"""
        url = reverse(check_registration_link, args=['bar', ])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_correct_link(self):
        """Access correct registration link"""
        response = self.client.get(self.correct_link, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], 'http://testserver/accounts/register/')
        # django 1.4 self.assertRedirects(response, 'accounts/register/')

    def register_user(self, username):
        """Register a new user account in the system"""
        # Use registration link
        response = self.client.get(self.correct_link, follow=True)
        self.assertEqual(response.status_code, 200)
        # Submit registration form
        response = self.client.post(reverse('registration_register'), {'email': '%s@bar.com' % username,
            'password1': 'test', 'password2': 'test', 'username': username}, follow=False)

    def logout_user(self):
        """Request the logout url to logout the user"""
        # Logout
        self.client.get(reverse('auth_logout'), follow=True)

    def test_usage_and_threshold(self):
        """After exceeding threshold no more registrations should be allowed"""
        # 1st time
        self.register_user("foo")
        # used_times increment
        self.reg = RegistrationLink.objects.get(id=self.reg.id)
        self.assertEqual(self.reg.used_times, 1)
        self.logout_user()

        # 2nd use
        self.register_user("foo1")
        self.reg = RegistrationLink.objects.get(id=self.reg.id)
        self.assertEqual(self.reg.used_times, 2)
        self.logout_user()

        # 3rd use (not allowed)
        response = self.client.get(self.correct_link, follow=True)
        self.assertEqual(response.status_code, 403)
        self.reg = RegistrationLink.objects.get(id=self.reg.id)
        self.assertEqual(self.reg.used_times, 2)
        self.logout_user()

    def test_active_inactive(self):
        """Disable and enable registration link"""
        self.reg.active = False
        self.reg.save()
        response = self.client.get(self.correct_link, follow=True)
        self.assertEqual(response.status_code, 403)

        self.reg.active = True
        self.reg.save()
        response = self.client.get(self.correct_link, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_logged_in_register(self):
        """User should not be able to access registration page when he is logged in"""
        self.register_user("foo3")
        response = self.client.post(reverse('registration_register'), {'email': 'foo2@bar.com',
            'password1': 'test', 'password2': 'test', 'username': 'foo2'})
        self.assertTrue('accounts/register/closed' in response["Location"])
