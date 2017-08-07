# coding: UTF-8

from __future__ import unicode_literals

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


CHARS_ALLOWED = r'1234567890ABCDEFGHIJKLMNOPQRSTUVXWYZabcdefghijklmnopqrstuvxwyz'


def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    return 'projects/logo/{0}.{1}'.format(
        get_random_string(length=16, allowed_chars=CHARS_ALLOWED),
        ext
    )


class Project(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nome"),
        null=True, blank=True,
    )
    logo = models.ImageField(
        upload_to=rename_image,
    )
    description = models.TextField(
        verbose_name=_("Descrição"),
        null=True, blank=True
    )
    information = models.TextField(
        verbose_name=_("Informação"),
        null=True, blank=True
    )
    url = models.SlugField(
        max_length=164
    )
    creation = models.DateTimeField(
        
    )
