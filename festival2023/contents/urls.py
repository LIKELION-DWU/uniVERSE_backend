from django.urls import path, include
from . import views
from .views import StudentInfoView, CollegeRankListView

urlpatterns =[
    path('POST/student-info/', StudentInfoView.as_view(), name="studentinfo"), # 단과대항전 정보 입력
    path('GET/competition/', CollegeRankListView.as_view(), name="competition"), # 단과대항전 순위 출력
    path('GET/booth-search', views.BoothSearchView.as_view(), name="boothSearch"), # 소은 - 검색 기능
]
