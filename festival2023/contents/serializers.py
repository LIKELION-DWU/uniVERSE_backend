from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from . import models

class CollegeSerializer(ModelSerializer):
    class Meta:
        model = models.College
        fields = '__all__'

class StudentSerializer(ModelSerializer):
    class Meta:
        model = models.Student
        fields = '__all__'
    
class BoothSerializer(ModelSerializer):
    class Meta:
        model = models.Booth
        fields = '__all__'

class BookSerializer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'

class BoothSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booth
        fields = ['name']
