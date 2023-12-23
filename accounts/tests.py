from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm

class LoginFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {
            'username': 'Testuser1',
            'password': 'Testpassword1',
        }

    def setUp(self):
        # Create an initially empty login form
        self.empty_form = AuthenticationForm(data={
            'username': '',
            'password': '',
        })

    # Ensure users are redirected to the recipes list page after logging in
    def test_login_redirect(self):
        self.empty_form.data = self.form_data
        client = Client()
        response = client.post(reverse('accounts:login'), data=self.empty_form.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response, reverse('recipes:recipes_list_signed_users'))

    # Ensure users are not redirected to the recipes list page after failed log in
    def test_failed_login_redirect(self):
        self.empty_fields = self.empty_form.data
        client = Client()
        response = client.post(reverse('accounts:login'), data=self.empty_fields)
        self.assertTemplateUsed(response, 'accounts/login.html')

    # Ensure unsigned-users are redirected to the log in page after attempting to access recipes list protected page
    def test_unauthenticated_user_recipes_list_redirect(self):
        client = Client()
        response = client.get(reverse('recipes:recipes_list_signed_users'))
        expected_url = reverse('accounts:login') + '?next=' + reverse('recipes:recipes_list_signed_users')
        self.assertRedirects(response, expected_url)

    # Ensure unsigned-users are redirected to the log in page after attempting to access recipe detail protected page
    def test_unauthenticated_user_recipes_detail_redirect(self):
        client = Client()
        response = client.get(reverse('recipes:recipes_detail_signed_users', kwargs={'pk': 1}))
        expected_url = reverse('accounts:login') + '?next=' + reverse('recipes:recipes_detail_signed_users', kwargs={'pk': 1})
        self.assertRedirects(response, expected_url)

    # Ensure unsigned-users are redirected to the log in page after attempting to access profile protected page
    def test_unauthenticated_user_profile_redirect(self):
        client = Client()
        response = client.get(reverse('accounts:profile'))
        expected_url = reverse('accounts:login') + '?next=' + reverse('accounts:profile')
        self.assertRedirects(response, expected_url)

    # Ensure users are redirected to the logout page after clicking on the logout button
    def test_logout(self):
        client = Client()
        response = client.post(reverse('accounts:logout'))
        self.assertTemplateUsed(response, 'accounts/logout.html')

