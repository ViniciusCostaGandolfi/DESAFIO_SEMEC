from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from src.users.forms.login_form import LoginForm
from src.users.forms.register_form import RegistrationForm


class AuthViewsTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.email = "tester@example.com"
        self.full_name = "Tester Silva"
        self.password = "secret123"
        self.username = "tester@example.com"

        self.user = User(
            email=self.email,
            full_name=self.full_name,
        )
        self.user.set_password(self.password)
        self.user.save()

        self.client = Client()
        self.client.force_login(self.user)

    def test_login_redirects_if_already_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse("users:login"))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            (resp.headers.get("Location") or resp["Location"]).endswith(reverse("sales:sales_list"))
        )

    def test_login_get_shows_form(self):
        resp = self.client.get(reverse("users:login"))
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.context["form"], LoginForm)

    @patch("users.views.UserService.authenticate_user")
    @patch("users.views.UserService.login_user")
    def test_login_post_success(self, mock_login_user, mock_auth):
        mock_auth.return_value = self.user

        resp = self.client.post(
            reverse("users:login"),
            {"email": "t@t.com", "password": self.password},
            follow=True
        )

        mock_auth.assert_called_once()
        mock_login_user.assert_called_once()

        self.assertRedirects(resp, reverse("sales:sales_list"))

        messages = [m.message for m in get_messages(resp.wsgi_request)]
        self.assertTrue(any("Bem-vindo" in msg for msg in messages))

    @patch("users.views.UserService.authenticate_user")
    def test_login_post_invalid_credentials(self, mock_auth):
        mock_auth.return_value = None

        resp = self.client.post(
            reverse("users:login"),
            {"email": "wrong@t.com", "password": "badpass"},
            follow=True
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.context["form"], LoginForm)
        messages = [m.message for m in get_messages(resp.wsgi_request)]
        self.assertTrue(any("Credenciais inválidas" in msg for msg in messages))

    def test_register_redirects_if_already_authenticated(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse("users:register"))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            (resp.headers.get("Location") or resp["Location"]).endswith(reverse("sales:sales_list"))
        )

    def test_register_get_shows_form(self):
        resp = self.client.get(reverse("users:register"))
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.context["form"], RegistrationForm)

    @patch("users.views.UserService.register_user")
    @patch("users.views.UserService.login_user")
    def test_register_post_success(self, mock_login_user, mock_register):
        mock_register.return_value = self.user

        resp = self.client.post(
            reverse("users:register"),
            {
                "username": "newuser",
                "email": "new@t.com",
                "password1": "abc123xyz",
                "password2": "abc123xyz",
            },
            follow=True
        )

        mock_register.assert_called_once()
        mock_login_user.assert_called_once()

        self.assertRedirects(resp, reverse("sales:sales_list"))
        messages = [m.message for m in get_messages(resp.wsgi_request)]
        self.assertTrue(any("Conta criada com sucesso" in msg for msg in messages))

    @patch("users.views.UserService.register_user", side_effect=ValueError("erro de registro"))
    def test_register_post_service_error(self, mock_register):
        resp = self.client.post(
            reverse("users:register"),
            {
                "username": "bad",
                "email": "bad@t.com",
                "password1": "123",
                "password2": "456",
            },
            follow=True
        )

        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.context["form"], RegistrationForm)
        messages = [m.message for m in get_messages(resp.wsgi_request)]
        self.assertTrue(any("erro de registro" in msg for msg in messages))

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get(reverse("users:logout"), follow=True)

        self.assertRedirects(resp, reverse("users:login"))

        user = resp.wsgi_request.user
        self.assertFalse(user.is_authenticated)

        messages = [m.message for m in get_messages(resp.wsgi_request)]
        self.assertTrue(any("desconectado" in msg for msg in messages))

