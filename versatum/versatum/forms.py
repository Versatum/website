# coding: UTF-8

from django import forms
from utils import BaseBootstrapForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserForm(forms.ModelForm, BaseBootstrapForm):

    password2 = forms.CharField(
        label=_("Confirm password"),
        help_text=_("This field should be the same as the first"),
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):

        super(UserForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.required = True
            if isinstance(field.widget, (forms.TextInput, forms.Textarea)):
                if field.required:
                    field.widget.attrs.setdefault(
                        'placeholder',  _(u'Required field'))

    def clean(self):
        clean = super(UserForm, self).clean()
        if clean.get('password') != clean.get('password2'):
            raise forms.ValidationError(
                _("The \"confirm password\" field should be the same as the first field"))
        return clean

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        model = User
        widgets = {
            'password': forms.PasswordInput,
        }


class LoginForm(forms.Form, BaseBootstrapForm):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user or (user and not user.is_active):
                raise forms.ValidationError(_(u"User or password is invalid"))

        return self.cleaned_data

    def authenticate(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            login(request, user)

        return user
