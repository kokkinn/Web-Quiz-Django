from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError


class AccountRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html
    )
    password2 = forms.CharField(
        label='Confirm password:',
        widget=forms.PasswordInput,
        help_text='Please repeat password'
    )

    def clean_password1(self):
        pwd = self.cleaned_data['password1']
        password_validation.validate_password(pwd)
        return self.cleaned_data['password1']

    def clean(self):
        super().clean()
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')
        print(pwd1, pwd2)
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError(
                {
                    'password2': ValidationError('Password not equals', code='password_mismatch')
                }
            )
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save()
        user.set_password(self.cleaned_data['password1'])
        user.is_active = True
        user.is_activated = True
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class AccountUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'birthday',
            'city',
            'avatar',
        ]
