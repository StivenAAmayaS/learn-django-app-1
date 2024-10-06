# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Project, Taks
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CreateNewTask, CreateNewProject

def index(request):
    title = "Django course!!"
    return render(request, 'index.html', {
        'title': title
    })

def hello(request, username):
    print(type(username))
    return HttpResponse("<h2>Hello %s</h2>" % username)

def projects(request):
    # projects = list(Project.objects.values())
    projects = Project.objects.all()
    # return JsonResponse(projects, safe=False)
    return render(request, 'projects/projects.html', {
        'projects': projects
    })

def tasks(request):
    # taks = Taks.objects.get(id=id)
    # taks = get_object_or_404(Taks, id=id)
    tasks = Taks.objects.all()
    # return HttpResponse('task: %s'  % taks.title)

    if (request.method =='POST'):
        print(request.POST)
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Taks, id=task_id)
        print(task.done)
        task.done = not task.done
        task.save()
        return redirect('tasks')

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })

def create_task(request):

    if request.method == 'GET':
        # Show interface
        return render(request, 'tasks/create_task.html', {
            'form': CreateNewTask()
        })
    else: 
        # title = request.GET.get('title', False)
        # description = request.GET.get('description', False)
        
        title = request.POST['title']
        description = request.POST['description']

        Taks.objects.create(title=title, description=description, project_id=2)
        return redirect('tasks')
    

def create_project(request):

    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()
        })
    else: 
        Project.objects.create(name=request.POST['name'])
        return redirect('projects') # Se coloca 'url/' si no se maneja un nombre de url