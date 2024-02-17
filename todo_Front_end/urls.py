from django.urls import path
from .import views
from django.contrib.auth.views import LoginView as loginview
from django.contrib.auth.views import LogoutView as logoutview
from .forms import loginform
app_name="todo"
urlpatterns=[
    path('',views.TaskList.as_view(),name='home'),
    path('task/<int:pk>/',views.TaskDetail.as_view(),name='taskdetail'),
    path('completed/<int:pk>/',views.completed,name='completed'),
    path('delete/<int:pk>/',views.taskDelete.as_view(),name='taskDelete'),
    path('add/',views.addTask,name='addtask'),
    path('login/',views.login_user,name='login'),
    path('logout/',logoutview.as_view(),name='logout'),
    path('search/',views.search,name='search'),
    path('register/',views.register,name='register'),
    

]