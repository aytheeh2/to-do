
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as Rview
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('API.urls')),
    # path('login/',Rview.obtain_auth_token),
    path('api/login/', Rview.obtain_auth_token),
    path('', include('todo_Front_end.urls')),

]
