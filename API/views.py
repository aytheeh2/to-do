from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .serializer import TaskSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated


class todo(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)
        


    # def perform_create(self, serializer):
    #     username = self.request.data.get('username')  # Assuming 'username' is passed in the request data
    #     user = self.get_user_(username)
    #     if user is not None:
    #         task=Task.objects.create(user=user)
    #         task.save()
    #     else:
    #         # Handle the case where the user does not exist
    #         # For example, you could raise an exception or return an error response
    #         raise Http404
            




class user(viewsets.ModelViewSet):
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
