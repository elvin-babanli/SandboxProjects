1) PS C:\Users\Alvin\Desktop\CRUD-roadmap> mkdir core
2) PS C:\Users\Alvin\Desktop\CRUD-roadmap> cd .\core\
3) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> python -m venv .venv
4) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> .venv\Scripts\activate
5) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> pip install Django
6) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> django-admin startproject core .
7) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> python manage.py startapp home
8) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> python manage.py runserver

Structure is ready

Step-1:
core/core/settings.py

add-INSTALLED_APPS: 
'home',

Step-2:
1) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> python manage.py migrate

core/home/models.py

add:
class Person(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"Name: {self.name}"

2) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> python manage.py makemigrations
3) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> python manage.py migrate

Step-3:
core/home/admin.py

1) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> python manage.py createsuperuser

Username (leave blank to use 'alvin'): alvin
Email address: elvinbabanli0@gmail.com
Password: 12345678 (Password going to be invisible)
Password (again): 12345678 (Password going to be invisible)
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.

Step-4:
add core/core/urls.py:

1) from home.views import *

2) path('admin/', admin.site.urls),
3) path('', include('home.urls'))

add core/home/urls.py:

1) path('', index, name='main'),
2) path('data/', get_data, name='get_data'),
3) path('delete/<int:person_id>/', delete_data, name='delete_data'),
4) path('update/<int:person_id>', update_data, name='update'),

Step-5:

Cteate:
1) core/home/templates/base.html
2) core/home/templates/index.html
3) core/home/templates/data.html
4) core/home/templates/update.html

Create:
1) core/home/static/
2) styless.css

step-6:

add core/home/views.py:

from django.shortcuts import render, redirect, get_object_or_404
from .models import Person

def index(request):
    edit_id = request.GET.get('edit')
    if request.method == 'GET' and edit_id:
        obj = get_object_or_404(Person, id=edit_id)
        return render(request, 'index.html', {'person': obj, 'is_edit': True})
    
    if request.method == 'POST':
        person_id = request.POST.get('person_id')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')

        if person_id:
            obj = get_object_or_404(Person, id=person_id)
            obj.name = name
            obj.surname = surname
            obj.email = email
            obj.save()
            return redirect('/data/')
        else:
            Person.objects.create(name=name, surname=surname, email=email)
            return redirect('/')

    return render(request, 'index.html')

def get_data(request):
    people = Person.objects.all()
    return render(request, 'data.html', {'data': people})


def update_data(request, person_id):
    obj = get_object_or_404(Person, id=person_id)
    if request.method == 'POST':
        obj.name = request.POST.get('name')
        obj.surname = request.POST.get('surname')
        obj.email = request.POST.get('email')
        obj.save()
        return redirect('/data/')
    return render(request, 'update.html', {'data': obj})


def delete_data(request, person_id):
    obj = get_object_or_404(Person, id=person_id)
    obj.delete()
    return redirect('/data/')


Step-7:
Html examples: https://getbootstrap.com/
core/home/templates/base.html:

<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <title>{% block title %}{% endblock %}</title>
</head>
<body class="p-3">
    <nav class="mb-3 d-flex gap-2">
        <a class="btn btn-primary" href="/">Home</a>
        <a class="btn btn-secondary" href="/data/">Data</a>
    </nav>
    {% block content %}{% endblock %}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>

core/home/templates/index.html:

{% extends 'base.html' %}
{% block title %}Home{% endblock %}
{% block content %}
<form method="post" class="card p-3 shadow-sm">
    {% csrf_token %}
    {% if is_edit %}
        <input type="hidden" name="person_id" value="{{ person.id }}">
    {% endif %}
    <div class="mb-3">
        <input class="form-control" name="name" placeholder="Name"
               value="{{ person.name|default:'' }}" required>
    </div>
    <div class="mb-3">
        <input class="form-control" name="surname" placeholder="Surname"
               value="{{ person.surname|default:'' }}" required>
    </div>
    <div class="mb-3">
        <input class="form-control" name="email" type="email" placeholder="Email"
               value="{{ person.email|default:'' }}" required>
    </div>

    <div class="d-flex gap-2 mt-2">
        <button class="btn btn-primary" type="submit">
            {% if is_edit %}Save Changes{% else %}Add User{% endif %}
        </button>

        {% if is_edit %}
            <a class="btn btn-secondary" href="/">Cancel</a>
        {% endif %}
    </div>
</form>
{% endblock %}


core/home/templates/data.html:

{% extends 'base.html' %}
{% block title %}Data{% endblock %}
{% block content %}
<table class="table table-striped align-middle">
    <thead>
        <tr>
            <th>#</th>
            <th>Name</th>
            <th>Surname</th>
            <th>Email</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for p in data %}
        <tr>
            <th scope="row">{{ forloop.counter }}</th>
            <td>{{ p.name }}</td>
            <td>{{ p.surname }}</td>
            <td>{{ p.email }}</td>
            <td class="d-flex gap-2">
                <!-- Edit artıq index-ə yönləndirir və formu doldurulmuş göstərir -->
                <a href="/?edit={{ p.id }}" class="btn btn-sm btn-warning">Edit</a>
                <a href="/delete/{{ p.id }}/" class="btn btn-sm btn-danger">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}


core/home/templates/update.html:

{% extends 'base.html' %}
{% block title %}Update{% endblock %}
{% block content %}
<form method="post" class="card p-3 shadow-sm">
    {% csrf_token %}
    <div class="mb-3">
        <input class="form-control" name="name" value="{{ data.name }}" required>
    </div>
    <div class="mb-3">
        <input class="form-control" name="surname" value="{{ data.surname }}" required>
    </div>
    <div class="mb-3">
        <input class="form-control" type="email" name="email" value="{{ data.email }}" required>
    </div>
    <button class="btn btn-primary" type="submit">Save</button>
</form>
{% endblock %}



Step-8:

Test server:
1) PS C:\Users\Alvin\Desktop\CRUD-roadmap\core> python manage.py runserver
Open: https://sqliteviewer.app/




