from django.db import models
from common.models import MyUser
from django.core.validators import RegexValidator
import datetime
# Create your models here.


class CmtHistory(models.Model): # 출퇴근
    employee = models.ForeignKey(MyUser, on_delete=models.CASCADE) # 로그인한 계정

    weeknum = models.PositiveSmallIntegerField() # 오늘 몇 주차

    TODAYCAT_CHOICES = (('AL', '연차'), ('MO', '오전 반차'), ('AO', '오후 반차')
        , ('CV', '경조 휴가'), ('OL', '공가'), ('EL', '조퇴'), ('AB', '결근'), ('SL', '병가')
        , ('HD', '공휴일'), ('WE', '주말'), ('WD', '평일'))
    todaycat = models.CharField(max_length=2, choices=TODAYCAT_CHOICES, default='WD') # 휴일 여부

    openingtime = models.TimeField(null=True) # 시업 시간
    closingtime = models.TimeField(null=True) # 종업 시간

    startdatetime = models.DateTimeField() # 출근한 시간이었다가 연장근로 시작시간으로 변경
    enddatetime = models.DateTimeField(null=True, blank=True) # 퇴근한 시간이었다가 연장근로 종료시간으로 변경

    workinghours = models.FloatField(default=0) # 근로한 시간
    breaktime = models.FloatField(default=0) # 휴게한 시간
    overtime = models.FloatField(default=0) # 연장근로한 시간

    is_abnormal = models.BooleanField(default=False) # 철야 또는 퇴근 버튼 안눌렀다.
    is_dayofflunch = models.BooleanField(default=False) # 연장근로시간 점심식사 여부
    is_ovtimedinner= models.BooleanField(default=False) # 연장근로시간 저녁식사 여부

    notice = models.TextField(max_length=1000) # 비고, 연장근로 사유
    APPROVAL_CHOICES = (('1', '대기'), ('2', '반려'), ('3', '승인'))
    approval = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='1') # 결재 상태

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "{0} : 출근시간 {1}".format(self.employee.realname, self.startdatetime)