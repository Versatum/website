
from models import Project

from django.shortcuts import render

def home(request):
    projects = Project.objects.all()
    data = dict(
        projects=projects,
    )
    return render(request, 'project_home.html', data)
