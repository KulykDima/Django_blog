from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import widgets

from .models import Feedback, Message


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='email')
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html
    )
    password2 = forms.CharField(
        label='confirm password',
        widget=forms.PasswordInput,
        help_text='please repeat your password'
    )

    def clean_password1(self):
        pwd = self.cleaned_data['password1']
        if pwd:
            password_validation.validate_password(pwd)
        return pwd

    def clean(self):
        super().clean()
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError(
                {
                    'password2': ValidationError('Password not equals', code='password_mismatch')
                }
            )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_activated = False
        user.is_active = False

        if commit:
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


class ActivationLetterAgain(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)
        exclude = (
            'username',
            'password1',
            'password2',
        )


class UserUpdateForm(UserChangeForm):
    avatar = forms.ImageField(required=False, widget=widgets.FileInput())
    birthday = forms.DateField(required=False, widget=widgets.DateInput(attrs={'type': 'date'}))
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birthday',
            'city',
            'avatar'
        )

        # widgets = {'birthday': forms.DateInput(attrs={'type': 'date'})}


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'recipient',
            'subject',
            'body',
        ]

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SendMessageFromProfile(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient',
                  'subject',
                  'body'
                  ]

    def __init__(self, *args, **kwargs):
        super(SendMessageFromProfile, self).__init__(*args, **kwargs)
        self.fields['recipient'].initial = 'recipient'

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class FeedbackCreateForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'subject',
            'email',
            'content'
        ]

    def __init__(self, *args, **kwargs):
        "Обновление стилей формы"
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
