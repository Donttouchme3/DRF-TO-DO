from rest_framework import serializers
from .models import Tasks


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ('id', 'title', 'start_time', 'end_time', 'status')


class TaskCreateOrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'


# class TaskUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tasks
#         fields = '__all__'



