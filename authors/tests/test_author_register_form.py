# from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from unittest import TestCase

class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('first_name', 'Your firts name'),
        ('last_name', 'Your last name'),
        ('password', 'Your password'),
        ('password2', 'Confirm the password'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', (
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.'
        )),
        ('email', 'The e-mail must be valid.'),
        ('password', (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be' 
            'at least 8 characters.'
        )),
    ])
    def test_fields_help_text(self, campo, help_text):
        form = RegisterForm()
        help_text_atual = form[campo].field.help_text

        self.assertEqual(help_text, help_text_atual)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, campo, label):
        form = RegisterForm()
        label_atual = form[campo].field.label

        self.assertEqual(label, label_atual)