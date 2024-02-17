from django.urls import path,include
from .import views
from rest_framework.routers import SimpleRouter

router=SimpleRouter()
router.register('task',views.todo)
router.register('user',views.user)
urlpatterns=[
    path('',include(router.urls)),
]