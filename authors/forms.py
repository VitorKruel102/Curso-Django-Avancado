from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re

def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val

def strong_password(password):
    regex = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$')
    
    if not regex.match(password):
        raise ValidationError((
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be' 
            'at least 8 characters.'
        ),
        code='invalid'
    )


class RegisterForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Your firts name')
        add_placeholder(self.fields['last_name'], 'Your last name')
        add_placeholder(self.fields['password'], 'Your password')
        add_placeholder(self.fields['password2'], 'Confirm the password')


    password = forms.CharField(
        label='Password',
        required=True, 
        widget=forms.PasswordInput(
        ),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be' 
            'at least 8 characters.'
        ),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        label='Password2',
        required=True, 
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Password must not be empty'
        }
    )

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name']
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
        }
        help_texts = {
            'email': 'The e-mail must be valid.',
        }

        error_messages = {
            'username': {
                'required': 'This field must not be empty',
                'max_length': 'This field must have less than 3 character',
                'invalid': 'This fieldis invalid',
            }
        }

    def clean_username(self): 
        # Utilizado para validar o campo,
        # clean_ + nome-do-campo
        username = self.cleaned_data.get('username')

        if '$' in username:
            raise ValidationError(
                'UserName inválido',
                code='invalid'

            )
        return username

    def clean(self):
        cleaned_data = super().clean()

        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': ValidationError(
                    'Senha são diferentes',
                    code='invalid'
                ),
                'password2': 'Senha são diferentes',
            }
            )
