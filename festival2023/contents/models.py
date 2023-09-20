from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError

DATES = (
    ('day1', "2023-10-04"),
    ('day2', "2023-10-05"),
    ('day3', "2023-10-06"),
)

class College(models.Model) : # 단과대학 
    college_id = models.CharField(verbose_name="대학 커스텀 ID", primary_key=True, max_length=10)
    college = models.CharField(verbose_name='단과대학명', default='인문대학', max_length=30)
    total = models.IntegerField(verbose_name='총인원')
    
    def __str__(self):
        return self.college

def validate_stu_id(value): # 학번 제한
    # 프론트에 에러메시지 넘겨서 에러페이지 만드는 경우 아래코드 수정필요
    if len(value) != 8:
        raise ValidationError('학번은 8자여야 합니다.')
    if not value.startswith('20'):
        raise ValidationError('학번은 "20"으로 시작해야 합니다.')

class Student(models.Model) : # 학생
    stu_id = models.CharField(verbose_name='학번', primary_key=True, max_length=8, validators=[validate_stu_id]) # pk
    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name="소속단과대학")
    
    def __str__(self):
        return self.stu_id

class Booth(models.Model) : # 부스 
    booth_id = models.IntegerField(verbose_name="부스 커스텀 ID", primary_key=True)
    name = models.CharField(verbose_name="부스이름", max_length=128)
    category = models.CharField(verbose_name="부스 카테고리(날짜별)", choices=DATES, default='day1', max_length=10)
    date = models.TextField(verbose_name="일시", default="10.04 - 10.06")
    place = models.TextField(verbose_name="장소", default="동덕여자대학교")
    introduce = models.TextField(verbose_name="내용")
    image = models.ImageField(verbose_name="부스 사진", blank=True, null=True, upload_to='booth-image')

    def __str__(self):
        return self.name

class Book(models.Model) : # 방명록
    time = models.DateTimeField(verbose_name='생성시간', unique=True)
    content = models.TextField(verbose_name='방명록')
    
    # 방명록 시간으로 구분
    def save(self, *args, **kwargs):
        # 현재 시간을 마이크로세컨드로 변환
        now = datetime.now()
        microsecond = now.microsecond

        self.time = now
        super(Book, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.time.strftime('%Y-%m-%d %H:%M:%S') #수정
