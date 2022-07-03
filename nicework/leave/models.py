from django.db import models
from common.models import MyUser
from django.core.validators import RegexValidator
import datetime
# Create your models here.


class Reward(models.Model): # 발생한 포상휴가
    employee = models.ForeignKey(MyUser, on_delete=models.CASCADE) # 로그인한 계정
    reason = models.TextField(max_length=500)
    days = models.FloatField(default=1)
    granter = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} : {1}일, 사유 :{2}".format(self.employee.realname, self.days, self.reason)


class LevHistory(models.Model): # 신청된 휴가
    employee = models.ForeignKey(MyUser, on_delete=models.CASCADE) # 로그인한 계정
    reason = models.TextField(max_length=1000) # 휴가 사유
    startdate = models. DateField() # 휴가 시작일시
    enddate = models. DateField() # 휴가 종료일자
    starttime = models.TimeField() # 휴가 시작시간
    endtime = models.TimeField() # 휴가 종료시간
    leaveterm = models.FloatField(default=0) # 휴가 기간
    LEAVECAT_CHOICES = (('AL', '연차'), ('MO', '오전 반차'), ('AO', '오후 반차')
        , ('CV', '경조 휴가'), ('OL', '공가'), ('EL', '조퇴'), ('AB', '결근'), ('SL', '병가'))
    leavecat = models.CharField(max_length=2, choices=LEAVECAT_CHOICES, default='AL') # 휴가 시간구분
    phoneNumberRegex = RegexValidator(regex = r"^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$")
    emgnum = models.CharField(validators = [phoneNumberRegex], max_length=15,) # 비상 연락처
    APPROVAL_CHOICES = (('1', '대기'), ('2', '반려'), ('3', '승인'))
    approval = models.CharField(max_length=1, choices=APPROVAL_CHOICES, default='1') # 결재 상태
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} : {1} ~ {2} ({3}일, {4}) [{5}]".format(self.employee.realname, self.startdate, self.enddate, self.leaveterm, self.leavecat, self.approval)
