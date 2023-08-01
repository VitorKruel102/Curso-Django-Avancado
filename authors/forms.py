from django import forms
from django.contrib.auth.models import User


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


class RegisterForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['username'], 'Your username')
        add_placeholder(self.fields['email'], 'Your e-mail')
        add_placeholder(self.fields['first_name'], 'Your firts name')
        add_placeholder(self.fields['last_name'], 'Your last name')


    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Your password',
            }
        ),
        error_messages={
            'required': 'Password must not be empty'
        },
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be' 
            'at least 8 characters.'
        )
    )
    password2 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repeat your password',
            }
        ),
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
            'password': 'Password',
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
