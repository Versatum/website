# coding: UTF-8

from models import Article

from django.shortcuts import render
from django.shortcuts import get_object_or_404

def articles(request):
    articles = Article.objects.all()
    data = dict(
        articles=articles,
    )
    return render(request, 'blog_home.html', data)


def article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    data = dict(
        article=article,
    )
    return render(request, 'blog_article.html', data)
