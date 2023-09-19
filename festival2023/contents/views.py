from django.contrib import admin
from .models import College, Student, Booth, Book
from .serializers import BoothSearchSerializer

from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

#이미 등록했으므로 주석 처리했어요
# class College_list(admin.ModelAdmin):
#     list_display = '__all__'
# admin.site.register(College, College_list)

# class Student_list(admin.ModelAdmin):
#     list_display = ('id', 'name', 'customer', 'product')
# admin.site.register(Student, Student_list)

# class Booth_list(admin.ModelAdmin):
#     list_display = ('id', 'num', 'customer')
# admin.site.register(Booth, Booth_list)

# class Book_list(admin.ModelAdmin):
#     list_display = ('id', 'num', 'customer')
# admin.site.register(Book, Book_list) #Card_list->Book_list로 바꿨어요..(?)

class BoothSearchView(generics.ListAPIView):
    serializer_class = BoothSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    pagination_class = PageNumberPagination

    def get_queryset(self):
        search_term = self.request.query_params.get('name')
        if search_term:
            queryset = Booth.objects.filter(name__icontains=search_term)
        else:
            queryset = Booth.objects.all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        search_term = self.request.query_params.get('name')
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        results_count = queryset.count()  # 검색 결과 수 계산

        if results_count == 0:
            return Response({'message': '검색 결과가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_data = []  # 검색결과 직렬화
        for booth in queryset:
            serialized_data.append({
                'name': booth.name,
                'introduce': booth.introduce
            })

        data = {
            'results': serialized_data,
            'results_count': results_count
        }
        return Response(data)