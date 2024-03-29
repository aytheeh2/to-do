from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView
from API.models import Task
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


class TaskList(LoginRequiredMixin, ListView):
    # queryset=Task.objects.all()
    model = Task
    template_name = 'index.html'
    context_object_name = 'tasklist'

    def get_queryset(self):
        u = self.request.user
        return Task.objects.filter(user=u)

# @login_required
# def TaskList(request):
#     taskList=Task.objects.filter(user=request.user)
#     return render(request,'index.html',{'taskList':taskList})


class TaskDetail(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'taskdetail'
    fields = ('name', 'description', 'completed')
    # imp should add a message here showing success
    success_url = reverse_lazy('todo:home')

# def TaskDetail(request, username):
#     try:
#         user = User.objects.get(username=username)
#     except User.DoesNotExist:
#         raise Http404
#     else:
#         details = Task.objects.filter(user=user)
#         return render(request, 'detail.html', {
#             'details': details,
#         })


@login_required
def completed(request, pk):
    task = Task.objects.get(pk=pk)
    task.completed = True
    task.save()
    messages.success(request, f'Task {task.name} marked as completed! ')
    return redirect('todo:home')


@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(completed=True,user=request.user).order_by('-date_modified')
    return render(request, 'completed.html', {'tasks': tasks})


@login_required
def incompleted_tasks(request):
    tasks = Task.objects.filter(completed=False,user=request.user).order_by('-date_modified')
    return render(request, 'incomplete.html', {'tasks': tasks})


class taskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'delete.html'
    context_object_name = 'task'
    # imp should add a message here showing success
    success_url = reverse_lazy('todo:home')


@login_required
def clearAllTasks(request):
    tasks = Task.objects.filter(user=request.user)
    if tasks:
        if request.method == "POST":
            tasks = Task.objects.filter(user=request.user)
            tasks.delete()
            messages.success(request, f'All of your tasks are deleted! ')
            return redirect('todo:home')
        return render(request, 'clearalltasks.html')
    else:
        messages.success(request, 'You have no tasks to delete! ')
        return redirect("todo:home")


@login_required
def addTask(request):
    if request.method == "POST":
        username = request.user
        name = request.POST['name']
        description = request.POST['description']
        task = Task.objects.create(
            user=username, name=name, description=description)
        if task:
            task.save()
            messages.success(request, f'Task {name} added!')
            return redirect('todo:home')
        else:
            messages.success(request, f'Failed to add task!')
            return redirect('todo:home')
            # return HttpResponse(request, 'form invalid')

    return render(request, 'addtask.html')


@login_required
def search(request):
    query = ""
    search_results = None
    if request.method == "POST":
        query = request.POST.get('q', '')
        if query:
            search_results = Task.objects.filter(Q(name__icontains=query) | Q(
                description__icontains=query), user=request.user)
    return render(request, "search.html", {'query': query, 'search_results': search_results})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('todo:home')
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            user = User.objects.create_user(
                username=username, password=password1, email=email)
            user.save()
            messages.success(request, 'User Registered Successfully')

            # Log in the user after registration
            user = authenticate(username=username, password=password1)
            if user:
                login(request, user)
                messages.success(request, 'Login Successful')
                return redirect('todo:home')
            else:
                return HttpResponse('Failed to authenticate user after registration')
        else:
            return HttpResponse('Passwords do not match')

    return render(request, 'register.html')
