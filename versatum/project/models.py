# coding: UTF-8

from __future__ import unicode_literals

from utils import rename_image

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):
    name = models.CharField(
        unique=True,
        max_length=100,
        verbose_name=_("Name"),
    )
    logo = models.ImageField(
        upload_to=rename_image,
    )
    description = models.TextField(
        verbose_name=_("Descrption"),
        null=True, blank=True
    )
    information = models.TextField(
        verbose_name=_("Info"),
        null=True, blank=True
    )
    maintainers = models.ManyToManyField(
        User,
        verbose_name=_("Maintainers"),
    )
    url = models.SlugField(
        verbose_name='url',
        max_length=164
    )
    created = models.DateTimeField(
        verbose_name=_("Created"),
        auto_now_add=True,
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
