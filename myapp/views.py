# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q
from .models import Project, Task
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

    # projects = Project.objects.all()

    # project_data = []

    # for project in projects: 
    #     tasks = project.tasks
    #     total_tasks = tasks.count()
    #     completed_tasks = tasks.filter(completed=True).count()
    #     pending_tasks = total_tasks - completed_tasks

    #     project_data.append({
    #         'project': project,
    #         'total_tasks': total_tasks,
    #         'completed_tasks': completed_tasks,
    #         'pending_tasks': pending_tasks,
    #     })        

    # return JsonResponse(projects, safe=False)

    projects = Project.objects.annotate(
        total_tasks=Count('tasks'),
        completed_tasks=Count('tasks', filter=Q(tasks__completed=True)),
        pending_tasks=Count('tasks', filter=Q(tasks__completed=False)),
    )

    return render(request, 'projects/projects.html', {
        'projects': projects,
    })

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    filter_option = request.GET.get('filter', 'all')
    
    # Chekea si el proyecto contiene tareas
    has_tasks = project.tasks.exists()

    if filter_option == 'completed':
        tasks = project.tasks.filter(completed=True)
    elif filter_option == 'pending':
        tasks = project.tasks.filter(completed=False)
    else: 
        tasks = project.tasks.all()


    if request.method == 'POST':
        form = CreateNewTask(request.POST)
        if form.is_valid():
            title = request.POST['title']
            description = request.POST['description']
            Task.objects.create(title=title, description=description, project_id=pk)
            return redirect('project_detail', pk)
        else: 
            form = CreateNewTask()

    return render(request, 'projects/project_detail.html', { 
        'project': project, 
        'tasks': tasks,
        'form': CreateNewTask(),
        'filter': filter_option,
        'has_tasks': has_tasks
    })


def create_task(request, pk):

    project = get_object_or_404(Project, pk=pk)

    if request.method == 'GET':
        # Show interface
        return render(request, 'tasks/create_task.html', {
            'form': CreateNewTask(),
            'project': project
        })
    else: 
        # title = request.GET.get('title', False)
        # description = request.GET.get('description', False)
        
        title = request.POST['title']
        description = request.POST['description']

        Task.objects.create(title=title, description=description, project_id=pk)
        return redirect('projects')

def tasks(request):
    # taks = Taks.objects.get(id=id)
    # taks = get_object_or_404(Taks, id=id)
    tasks = Task.objects.all()
    # return HttpResponse('task: %s'  % taks.title)

    if (request.method =='POST'):
        print(request.POST)
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        print(task.done)
        task.done = not task.done
        task.save()
        return redirect('tasks')

    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })


    

def create_project(request):

    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject()
        })
    else: 
        Project.objects.create(name=request.POST['name'], description=request.POST['description'])
        return redirect('projects') # Se coloca 'url/' si no se maneja un nombre de url