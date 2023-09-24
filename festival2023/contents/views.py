from django.contrib import admin
from .models import College, Student, Booth, Book
from .serializers import StudentSerializer, CollegeSerializer, BookSerializer, BoothSearchSerializer, BoothSerializer, BoothDetailSerailizer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, filters, status
from rest_framework.pagination import PageNumberPagination
from datetime import datetime
from django.db.models import Q 

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
                participation_rate = round(self.calculate_participation_rate(college), 2)
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

        # 참여율이 0%인 대학만 가져오기
        zeroColleges = colleges.filter(total=0)

        # 모든 대학의 참여율이 0%일때 -> 초기상태
        if zeroColleges.exists():
            zeroColleges = zeroColleges.order_by('college')
        else:
            colleges = colleges.order_by('college')

        for college in zeroColleges:
            participation_rate = round(self.calculate_participation_rate(college), 2)
            college_data.append({
                'college': college.college,
                'participation_rate': participation_rate,
            })

        # 나머지 대학들의 참여율을 기준으로 내림차순으로 정렬
        participation_colleges = colleges.exclude(total=0)
        participation_data = []
        for college in participation_colleges:
            participation_rate = round(self.calculate_participation_rate(college), 2)
            participation_data.append({
                'college': college.college,
                'participation_rate': participation_rate,
            })

        # 참여율로 내림차순정렬
        participation_data.sort(key=lambda x: x['participation_rate'], reverse=True)

        # 데이터를(zero, 아닌거)모든 데이터 합치기
        college_data.extend(participation_data)


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

# 검색
class BoothSearchView(generics.ListAPIView):
    serializer_class = BoothSearchSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category']

    pagination_class = PageNumberPagination

    def get_queryset(self):
        search_term = self.request.query_params.get('name')
        category_term = self.request.query_params.get('category')

        queryset = Booth.objects.all()

        if search_term:
            if not category_term:
                category_term = 'day1'
            queryset = queryset.filter(Q(name__icontains=search_term) & Q(category=category_term))

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        results_count = queryset.count()  # 검색 결과 수 계산

        if results_count == 0:
            return Response({'message': '검색 결과가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serialized_data = []  # 검색결과 직렬화
        for booth in queryset:
            serialized_data.append({
                'booth_id': booth.booth_id,
                'name': booth.name,
                'category': booth.category,
                'date': booth.date,
                'place': booth.place,
                'introduce': booth.introduce,
                'image': booth.image.url #postMan에서만 주석처리
            })

        data = {
            'results': serialized_data,
            'results_count': results_count
        }
        return Response(data)
    
#방명록 생성
class GuestBookView(APIView):
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        #micro 초 단위
        now = datetime.now().replace(microsecond=0)
        request.data['time'] = now.strftime('%Y-%m-%d %H:%M:%S.%f')

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)       
        
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 부스배치도 목록 
# day01
class BoothDay1ListView(APIView) :
    def get(self, request) : 
        booth1 = Booth.objects.filter(category='day1')
        serializer = BoothDetailSerailizer(booth1, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# day02
class BoothDay2ListView(APIView) :
    def get(self, request) : 
        booth2 = Booth.objects.filter(category='day2')
        serializer = BoothDetailSerailizer(booth2, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# day03
class BoothDay3ListView(APIView) :
    def get(self, request) : 
        booth3 = Booth.objects.filter(category='day3')
        serializer = BoothDetailSerailizer(booth3, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 부스배치도 상세페이지 - 성주 
class BoothDetailView(APIView) :
    def get(self, request, booth_id) :
        booth = Booth.objects.get(pk=booth_id)
        serailizer = BoothDetailSerailizer(booth)
        return Response(serailizer.data, status=status.HTTP_200_OK)

