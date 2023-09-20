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

class BookSerializer(ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'

class BoothSerializer(ModelSerializer):
    class Meta:
        model = models.Booth
        fields = ['image', 'name', 'introduce']

class BoothSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booth
        fields = ['name', 'image', 'introduce']

class BoothDetialSerailizer(serializers.ModelSerializer) :
    class Meta : 
        model = models.Booth
        fields = ['image', 'name', 'introduce', 'place', 'date']