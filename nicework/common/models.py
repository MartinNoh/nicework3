from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, realname, phonenum, department, rank, effcdate, openingtime, closingtime, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('이메일 주소는 반드시 필요합니다.')

        user = self.model(
            email=self.normalize_email(email),
            realname=realname,
            phonenum=phonenum,
            department=department,
            rank=rank,
            effcdate=effcdate,
            openingtime=openingtime,
            closingtime=closingtime
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, realname, phonenum, department, rank, effcdate, openingtime, closingtime, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            realname=realname,
            phonenum=phonenum,
            department=department,
            rank=rank,
            effcdate=effcdate,
            openingtime=openingtime,
            closingtime=closingtime
        )
        user.is_manager = True
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='이메일',
        max_length=40,
        unique=True,
    )
    realname = models.CharField(
        verbose_name='이름',
        max_length=10,
    )
    phoneNumberRegex = RegexValidator(regex = r"^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$")
    phonenum = models.CharField(
        verbose_name='휴대폰 번호',
        validators = [phoneNumberRegex],
        max_length=15,
        unique = True
    )
    RANK_CHOICES = (('AS', '주임'), ('SN', '대리'), ('PC', '책임'), ('CF', '수석'))
    rank = models.CharField(verbose_name='직급', max_length=2, choices=RANK_CHOICES, default='AS')
    DEPARTMENT_CHOICES = (('DEV', '개발팀'), ('KNG', '지식큐레이션팀'))
    department = models.CharField(verbose_name='부서', max_length=3, choices=DEPARTMENT_CHOICES, default='KNG')
    effcdate = models.DateField(verbose_name='입사 일자')
    openingtime = models.TimeField(verbose_name='평소 근무 시작시간')
    closingtime = models.TimeField(verbose_name='평소 근무 종료시간')
    adminmemo = models.TextField(verbose_name='관리자 메모', max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_sbstt = models.BooleanField(verbose_name='연장근로 대체휴가 변환', default=True)
    is_over80p = models.BooleanField(verbose_name='출근 1년간 80% 이상', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['realname', 'phonenum', 'department', 'rank', 'effcdate', 'openingtime', 'closingtime']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin