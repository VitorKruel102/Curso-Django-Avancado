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

    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letters, numbers or one of those @.+-_. '
            'The length should be between 4 and 150 characters.'
        ),
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        min_length=4, max_length=150,
    )

    first_name = forms.CharField(
        error_messages={
            'required': 'Write your first name'
        },
        label='First name'
    )

    last_name = forms.CharField(
        error_messages={
            'required': 'Write your last name'
        },
        label='Last name'
    )

    email = forms.EmailField(
        error_messages={
            'required': 'Email is requerid'
        },
        help_text='The e-mail must be valid.',
        label='E-mail'
    )

    password = forms.CharField(
        label='Password', 
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
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Please, repeat you password'
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
