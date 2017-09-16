from __future__ import unicode_literals

from utils import rename_image

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name=_("User"),
    )
    picture = models.ImageField(
        upload_to=rename_image,
    )
    about = models.TextField(
        verbose_name=_("About"),
    )

    def __unicode__(self):
        return self.user.get_full_name()


class Tag(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        null=True, blank=True
    )

    def __unicode__(self):
        return self.name


class Article(models.Model):
    author = models.ForeignKey(
        Author,
        verbose_name=_("Author"),
    )
    title = models.CharField(
        verbose_name=_("Title"),
        max_length=128,
    )
    cover = models.ImageField(
        upload_to=rename_image,
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    text = models.TextField(
        verbose_name=_("Text"),
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_("Tags"),
    )
    publication_date = models.DateTimeField(
        verbose_name=_("Publication date"),
    )
    created = models.DateTimeField(
        verbose_name=_("Created"),
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        verbose_name=_("Modified"),
        auto_now=True,
    )

    def __unicode__(self):
        return "Article: {0} - {1}".format(
            self.title,
            self.author,
        )


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article,
        verbose_name=_("Article"),
    )
    image = models.ImageField(
        upload_to=rename_image,
    )
    label = models.CharField(
        verbose_name=_("Label"),
        max_length=100,
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return "Article Image: {0} - {1}".format(
            self.article,
            self.lebel,
        )
