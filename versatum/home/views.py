# coding: UTF-8

from django.shortcuts import render


def homepage(request):
    return render(request, "home_homepage.html")


def about(request):
    return render(request, "home_about.html")


def community(request):
    return render(request, "home_community.html")


def help(request):
    return render(request, "home_help.html")
