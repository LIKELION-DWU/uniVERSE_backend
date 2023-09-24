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
        fields = ['booth_id', 'name', 'image', 'introduce']

class BoothSearchSerializer(serializers.ModelSerializer):
    # image 필드를 직렬화할 때 이미지 경로를 반환하도록 설정
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.Booth
        fields = ['booth_id', 'name', 'image', 'introduce']

    def get_image(self, obj):
        return obj.image.url
    
class BoothDetailSerailizer(serializers.ModelSerializer) :
    class Meta : 
        model = models.Booth
        fields = ['booth_id', 'image', 'name', 'introduce', 'place', 'date']