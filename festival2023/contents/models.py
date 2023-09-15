from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError

COLLEGES = (
    ('college1', '인문대학'),
    ('college2', '사회과학대학'),
    ('college3', '자연정보과학대학'),
    ('college4', '약학대학'),
    ('college5', '예술대학'),
    ('college6', '디자인대학'),
    ('college7', '공연예술대학'),
    ('college8', '문화지식융합대학'),
    ('college9', '미래인재융합대학'),
)

DATES = (
    ('day1', datetime(2023, 10, 4)),
    ('day2', datetime(2023, 10, 5)),
    ('day3', datetime(2023, 10, 6)),
)

# 단과대학 
class College(models.Model) :
    college = models.CharField(verbose_name='단과대학', choices=COLLEGES, default='college1', max_length=20)
    total = models.IntegerField(verbose_name='총인원')
    
    def __str__(self):
        return self.college

def validate_stu_id(value):
    # 프론트에 에러메시지 넘겨서 에러페이지 만드는 경우 아래코드 수정필요
    if len(value) != 8:
        raise ValidationError('학번은 8자여야 합니다.')
    if not value.startswith('20'):
        raise ValidationError('학번은 "20"으로 시작해야 합니다.')

# 학생
class Student(models.Model) :
    stu_id = models.CharField(verbose_name='학번', primary_key=True, max_length=8, validators=[validate_stu_id])
    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name="소속단과대학")
    
    def __str__(self):
        return self.stu_id
    
# 부스 
class Booth(models.Model) :
    name = models.CharField(verbose_name="부스이름", max_length=128)
    date = models.DateField(verbose_name="부스날짜", choices=COLLEGES, default='day1')
    introduce = models.TextField(verbose_name="한줄소개")
    notice = models.TextField(verbose_name="공지사항")
    image = models.ImageField(verbose_name="부스 사진", blank=True, null=True, upload_to='booth-image')

    def __str__(self):
        return self.name

class Book(models.Model) : # 방명록
    time = models.DateTimeField(verbose_name='생성시간', unique=True)
    content = models.TextField(verbose_name='방명록')
    
    def save(self, *args, **kwargs):
        # 현재 시간을 마이크로세컨드로 변환
        now = datetime.now()
        microsecond = now.microsecond

        self.time = now
        super(Book, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.time
