from django.shortcuts import render


def home(request):
    return render(request, 'project_home.html')
