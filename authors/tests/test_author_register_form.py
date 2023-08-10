# from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

from unittest import TestCase
from django.test import TestCase as DjangoTestCase

from django.urls import resolve, reverse

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
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
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


class AuthorRegisterFormIntegrationTest(DjangoTestCase):


    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please, repeat you password'),
        ('email', 'Email is requerid'),
    ])
    def test_fields_cannot_be_empty(self, field, mensagem):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)    

        # self.assertIn(mensagem, response.content.decode('utf-8'))
        self.assertIn(mensagem, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)    

        mensagem = 'Username must have at least 4 characters'
        self.assertIn(mensagem, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)    

        mensagem = 'Username must have less than 150 characters'
        self.assertIn(mensagem, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'


        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)    

        mensagem = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be' 
            'at least 8 characters.'
        )
            
        self.assertIn(mensagem, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@Abc2abc123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)    

        self.assertNotIn(mensagem, response.context['form'].errors.get('password'))

    def test_password_field_and_passwor_confirmation_are_equal(self):
        self.form_data['password'] = '@ABEDabc123'
        self.form_data['password2'] = '@ABEDabc1235'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)    

        mensagem = 'Senha são diferentes'
          
        self.assertIn(mensagem, response.context['form'].errors.get('password'))

        self.form_data['password'] = '@ABEDabc123'
        self.form_data['password2'] = '@ABEDabc123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)    

        self.assertNotIn(mensagem, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_views_returns_404(self):
        url = reverse('authors:create')
        response = self.client.get(url)    

        self.assertEqual(response.status_code, 404)

    def test_email_field_must_unique(self):
        url = reverse('authors:create')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)    
        msg = 'User e-mail is already in use'

        self.assertIn(msg, response.context['form'].errors.get('email'))

    def test_author_created_can_login(self):
        url = reverse('authors:create')

        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password2': '@Bc123456',
            }
        )
        
        self.client.post(url, data=self.form_data, follow=True)    

        is_authenticated = self.client.login(username='testuser', password='@Bc123456')

        self.assertTrue(is_authenticated)