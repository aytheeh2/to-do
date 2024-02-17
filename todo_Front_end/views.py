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
    return redirect('todo:home')


class taskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('todo:home')


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
            return redirect('todo:home')
        else:
            return HttpResponse(request, 'form invalid')

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

            # Log in the user after registration
            user = authenticate(username=username, password=password1)
            if user:
                login(request, user)
                return redirect('todo:home')
            else:
                return HttpResponse('Failed to authenticate user after registration')
        else:
            return HttpResponse('Passwords do not match')

    return render(request, 'register.html')
