# coding: UTF-8

from utils import enviar_email_html
from .forms import LoginForm, UserForm
from django.core.urlresolvers import reverse
from .secrets import SECRET_SALT_KEY as salt
from django.contrib.auth import get_user_model
from django.core.signing import TimestampSigner
from .secrets import SECRET_EMAIL_KEY as secret
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import logout as make_logout
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404



def files(request, filename):
    return render(request, filename)


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate(request)
            if user:
                redirect = request.GET.get('next', reverse("home:homepage"))
                return HttpResponseRedirect(redirect)

    return render(request, 'login.html', {'form': form})


def logout(request):
    make_logout(request)
    return HttpResponseRedirect(
        request.GET.get("next", reverse("home:homepage")))


def confirm(self, string):
    User = get_user_model()
    signer = TimestampSigner(secret, sep="##", salt=salt)
    string = signer.unsign(string)
    user = get_object_or_404(User, username=string)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse("home:homepage"))


ASSUNTO = _(u'Versatum - Confirm your email')


def register(request):
    user = None
    form = UserForm()
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            signer = TimestampSigner(secret, sep="##", salt=salt)
            string = signer.sign(user.username)
            enviar_email_html(
                'eduardomartins1993@gmail.com',
                ASSUNTO,
                u'email/email_register.html',
                {
                    'subject': ASSUNTO,
                    'name': user.first_name,
                    'link': request.build_absolute_uri(
                        reverse('confirm', kwargs={'string': string})
                    )
                },
                request,
            )
            user.save()
    return render(request, 'register.html', {'form': form, 'user': user})
