from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'password',]

    def create(self, validated_data):
        user =User.objects.create_user(username=validated_data['username'],password=validated_data['password'])
        user.save()
        return user
