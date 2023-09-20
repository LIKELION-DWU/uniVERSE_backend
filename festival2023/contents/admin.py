from django.contrib import admin
from . import models



class College_list(admin.ModelAdmin):
    list_display = ('college_id', 'college', 'total')
admin.site.register(models.College, College_list)

class Booth_list(admin.ModelAdmin) :
    list_display = ('booth_id', 'name', 'category', 'date', 'place', 'introduce')
admin.site.register(models.Booth, Booth_list)

admin.site.register(models.Student)
admin.site.register(models.Book)
