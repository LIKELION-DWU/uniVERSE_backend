from django.contrib import admin
from .models import College, Student, Booth, Book
from .serializers import StudentSerializer, CollegeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# 단과대항전 학생 정보 입력하는 view
class StudentInfoView(APIView):
    serializer_class = StudentSerializer

    def get(self, request):
        # 모든 학생 정보를 조회
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 학생 정보 입력
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # 학생 정보가 추가된 후에 참여율 순위를 업데이트
            colleges = College.objects.all()
            college_data = []
            for college in colleges:
                participation_rate = self.calculate_participation_rate(college) * 100
                college_data.append({
                    'college': college.college,
                    'participation_rate': participation_rate,
                })

            # 참여율을 기준으로 내림차순으로 정렬
            college_data.sort(key=lambda x: x['participation_rate'], reverse=True)
            
            # 순위를 계산하고 추가
            rank = 1
            prev_rate = None
            for entry in college_data:
                if prev_rate is None or entry['participation_rate'] < prev_rate:
                    entry['rank'] = rank
                    rank += 1
                else:
                    entry['rank'] = rank - 1
                prev_rate = entry['participation_rate']

            return Response({'college_rank': college_data}, status=201)
        return Response(serializer.errors, status=400)

    def calculate_participation_rate(self, college):
        # 단과대학별 참여율을 계산하는 부분
        total_college_students = college.total

        if total_college_students > 0:
            participate_students = Student.objects.filter(college=college).count()
            participation_rate = (participate_students / total_college_students) * 100
        else:
            participation_rate = 0

        return participation_rate

# 단과대항전 순위를 보여주는 view
class CollegeRankListView(APIView):

    def get(self, request):
        # 단과대학별 참여율을 계산하여 반환
        colleges = College.objects.all()
        college_data = []
        for college in colleges:
            participation_rate = self.calculate_participation_rate(college)
            college_data.append({
                'college': college.college,
                'participation_rate': participation_rate,
            })

        # 참여율을 기준으로 내림차순으로 정렬
        college_data.sort(key=lambda x: x['participation_rate'], reverse=True)
        
        # 순위를 계산하고 추가
        rank = 1
        prev_rate = None
        for entry in college_data:
            if prev_rate is None or entry['participation_rate'] < prev_rate:
                entry['rank'] = rank
                rank += 1
            else:
                entry['rank'] = rank - 1
            prev_rate = entry['participation_rate']

        return Response({'college_rank': college_data})

    def calculate_participation_rate(self, college):
        # 단과대학별 참여율을 계산하는 메서드
        total_college_students = college.total

        if total_college_students > 0:
            participate_students = Student.objects.filter(college=college).count()
            participation_rate = (participate_students / total_college_students) * 100
        else:
            participation_rate = 0

        return participation_rate

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
# admin.site.register(Book, Card_list)