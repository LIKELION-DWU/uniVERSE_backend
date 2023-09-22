from django.urls import path, include
from . import views
from .views import StudentInfoView, CollegeRankListView

urlpatterns =[
    path('student-info/', StudentInfoView.as_view(), name="studentinfo"), # 단과대항전 정보 입력
    path('competition/', CollegeRankListView.as_view(), name="competition"), # 단과대항전 순위 출력
    path('booth-search/', views.BoothSearchView.as_view(), name="boothSearch"), # 소은 - 검색 기능
    path('guestbook/', views.GuestBookView.as_view(), name='bookCreate'), #채연 -방명록생성
    path('guestbook/', views.GuestBookView.as_view(), name='bookList'), #채연 -방명록목록
    path('day1-booth/', views.BoothDay1ListView.as_view(), name="day1-booth"), # 성주 - 부스 목록
    path('day2-booth/', views.BoothDay2ListView.as_view(), name="day2-booth"), 
    path('day3-booth/', views.BoothDay3ListView.as_view(), name="day3-booth"), 
    path('booth-detail/<int:booth_id>/', views.BoothDetailView.as_view(), name="booth-detail"), # 성주 - 부스 상세
]
