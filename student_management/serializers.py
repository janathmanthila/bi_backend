from rest_framework import serializers

from .models import *


class StudentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'phone', 'email', 'city']


class StudentViewSerializer(StudentBaseSerializer):
    pass


class StudentListSerializer(StudentBaseSerializer):
    pass


class MarkBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ['id', 'student', 'subject', 'mark', 'semester', 'grade', 'year']


class MarkViewSerializer(MarkBaseSerializer):
    pass


class MarkListSerializer(MarkBaseSerializer):
    pass
