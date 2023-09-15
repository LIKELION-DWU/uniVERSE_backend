from django.contrib import admin
from .models import College, Student, Booth, Book


class College_list(admin.ModelAdmin):
    list_display = '__all__'
admin.site.register(College, College_list)

class Student_list(admin.ModelAdmin):
    list_display = ('id', 'name', 'customer', 'product')
admin.site.register(Student, Student_list)

class Booth_list(admin.ModelAdmin):
    list_display = ('id', 'num', 'customer')
admin.site.register(Booth, Booth_list)

class Book_list(admin.ModelAdmin):
    list_display = ('id', 'num', 'customer')
admin.site.register(Book, Card_list)