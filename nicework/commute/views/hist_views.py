from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from common.models import MyUser
from leave.models import LevHistory
from ..models import CmtHistory
from django.core.paginator import Paginator
import datetime
from django.db.models import Q
from operator import itemgetter
from django.contrib import messages


@login_required(login_url='common:login')
def history(request):
    # 로그인한 계정의 출퇴근 내역 가져오기
    myuser = get_object_or_404(MyUser, email=request.user.email)
    mylist = CmtHistory.objects.filter(employee=myuser).order_by('-startdatetime')

    today_week = datetime.datetime.now().isocalendar()[1]
    this_week_cmtlist = CmtHistory.objects.filter(employee=myuser, weeknum=today_week).order_by('-startdatetime')
    sum_workinghours = 0
    sum_overtime = 0
    for i in this_week_cmtlist:
        sum_workinghours = sum_workinghours + i.workinghours
        sum_overtime = sum_overtime + i.overtime

    # 페이지 당 10개씩 보여주기
    page = request.GET.get('page', '1')
    dt = request.GET.get('dt', '') # 검색일자
    ct = request.GET.get('ct', '') # 검색구분
    kw = request.GET.get('kw', 0)  # 오버타임
    
    if dt!='' and ct!='':
        mylist = mylist.filter(overtime__gte=kw, todaycat__icontains=ct, startdatetime__gte=dt).distinct()
    elif dt == '' and ct != '':
        mylist = mylist.filter(overtime__gte=kw, todaycat__icontains=ct).distinct()
    elif dt != '' and ct == '':
        mylist = mylist.filter(overtime__gte=kw, startdatetime__gte=dt).distinct()
    else:
        mylist = mylist.filter(overtime__gte=kw).distinct()
    paginator = Paginator(mylist, 10)
    page_obj = paginator.get_page(page)

    context = {'myuser':myuser, 'mylist': page_obj, 'page': page, 'kw': kw, 'dt':dt, 'ct': ct, 'sum_workinghours':round(sum_workinghours, 1), 'sum_overtime':round(sum_overtime, 1)}
    return render(request, 'commute/commute_hist.html', context)


@login_required(login_url='common:login')
def situation(request):

    try:
        myuser = get_object_or_404(MyUser, email=request.user.email)
    except Exception as e:
        myuser = ''
        print(f"Exceiption occured:\n{e}")

    today = datetime.date.today()
    today_start = datetime.datetime.combine(today, datetime.time(0, 0, 0))
    today_end = datetime.datetime.combine(today, datetime.time(23, 59 ,59))
    commuters = CmtHistory.objects.filter(startdatetime__gte=today_start, startdatetime__lte=today_end).order_by('startdatetime', 'enddatetime')
    commuting_list = []
    for i in commuters:
        commuting_list.append(i.employee.realname)
    mgr_or_admin = MyUser.objects.filter(Q(is_admin=True) | Q(is_manager=True))
    for i in mgr_or_admin:
        commuting_list.append(i.realname)
    noncommute_users = MyUser.objects.filter().exclude(realname__in=commuting_list).order_by('realname')
    today_leave_list = LevHistory.objects.filter(startdate__lte=today, enddate__gte=today, approval='3').order_by('startdate')
    leave_dict = {'AL':'연차', 'MO':'오전 반차', 'AO':'오후 반차', 'CV':'경조 휴가', 'OL':'공가', 'EL':'조퇴', 'AB':'결근', 'SL':'병가'}
    noncommuters = []
    for i in noncommute_users:
        todaycat = '평일'
        for j in today_leave_list:
            if str(j.employee_id) == str(i.id):
                todaycat = leave_dict.get(str(j.leavecat))
        noncommuters.append({'todaycat':todaycat, 'openingtime':i.openingtime, 'realname':i.realname})
    noncommuters = sorted(noncommuters, key=itemgetter('todaycat', 'openingtime', 'realname'))
     
    context = {'myuser':myuser, 'commuters': commuters, 'noncommuters': noncommuters}
    return render(request, 'commute/commute_situ.html', context)


@login_required(login_url='common:login')
def totalhistory(request):
    try:
        myuser = get_object_or_404(MyUser, email=request.user.email)
    except Exception as e:
        myuser = ''
        print(f"Exceiption occured:\n{e}")

    # 전체 출근내역 가져오기
    mylist = CmtHistory.objects.filter().order_by('-startdatetime')

    # 페이지 당 10개씩 보여주기
    page = request.GET.get('page', '1')
    dt = request.GET.get('dt', '') # 검색일자
    ct = request.GET.get('ct', '') # 검색구분
    kw = request.GET.get('kw', 0)  # 오버타임

    if dt!='' and ct!='':
        mylist = mylist.filter(overtime__gte=kw, todaycat__icontains=ct, startdatetime__gte=dt).distinct()
    elif dt == '' and ct != '':
        mylist = mylist.filter(overtime__gte=kw, todaycat__icontains=ct).distinct()
    elif dt != '' and ct == '':
        mylist = mylist.filter(overtime__gte=kw, startdatetime__gte=dt).distinct()
    else:
        mylist = mylist.filter(overtime__gte=kw).distinct()
    paginator = Paginator(mylist, 10)
    page_obj = paginator.get_page(page)

    context = {'myuser':myuser, 'email': request.user.email, 'mylist': page_obj, 'page': page, 'kw': kw, 'dt': dt, 'ct': ct}

    return render(request, 'commute/commute_toth.html', context)


@login_required(login_url='common:login')
def overtimehist(request):
    # 로그인한 계정의 출퇴근 내역 가져오기
    myuser = get_object_or_404(MyUser, email=request.user.email)
    mylist = CmtHistory.objects.filter(employee=myuser).order_by('-startdatetime')

    today_week = datetime.datetime.now().isocalendar()[1]
    this_week_cmtlist = CmtHistory.objects.filter(employee=myuser, weeknum=today_week).order_by('-startdatetime')

    sum_overtime = 0
    for i in this_week_cmtlist:
        sum_overtime = sum_overtime + i.overtime

    # 페이지 당 10개씩 보여주기
    page = request.GET.get('page', '1')
    dt = request.GET.get('dt', '') # 검색일자
    ct = request.GET.get('ct', '') # 검색구분
    kw = request.GET.get('kw', 0)  # 오버타임
    
    if dt!='' and ct!='':
        mylist = mylist.filter(overtime__gte=kw, todaycat__icontains=ct, startdatetime__gte=dt).distinct()
    elif dt == '' and ct != '':
        mylist = mylist.filter(overtime__gte=kw, todaycat__icontains=ct).distinct()
    elif dt != '' and ct == '':
        mylist = mylist.filter(overtime__gte=kw, startdatetime__gte=dt).distinct()
    else:
        mylist = mylist.filter(overtime__gte=kw).distinct()
    paginator = Paginator(mylist, 10)
    page_obj = paginator.get_page(page)

    context = {'myuser':myuser, 'mylist': page_obj, 'page': page, 'kw': kw, 'dt':dt, 'ct': ct, 'sum_overtime':round(sum_overtime, 1)}
    return render(request, 'commute/commute_ovth.html', context)


@login_required(login_url='common:login')
def delete(request, myreg_id):
    myuser = get_object_or_404(MyUser, email=request.user.email)
    commute = get_object_or_404(CmtHistory, pk=myreg_id)
    # 관리자 또는 매니저인 경우
    if myuser.is_manager | myuser.is_admin:
        pass
    else:
        if request.user != commute.employee:
            messages.error(request, '삭제권한이 없습니다')
            return redirect('commute:ovtt')
    commute.delete()
    return redirect('commute:ovth')


@login_required(login_url='common:login')
def overtimesitu(request):
    myuser = get_object_or_404(MyUser, email=request.user.email)

    today_week = datetime.datetime.now().isocalendar()[1]
    users = MyUser.objects.all().exclude(Q(is_manager=True) | Q(is_active=False)).order_by('realname')
    so_list = []
    for i in users:
        email = i.email
        realname = i.realname
        this_week_cmtlist = CmtHistory.objects.filter(employee=i, weeknum=today_week).order_by('-startdatetime')
        sum_overtime = 0
        for j in this_week_cmtlist:
            sum_overtime = sum_overtime + j.overtime
        so_list.append({'email': email, 'realname': realname, 'sum_overtime': str(round(sum_overtime, 1)), 'remain_overtime': str(12-round(sum_overtime, 1))})

    context = {'myuser':myuser, 'today_week': today_week, 'so_list': so_list}
    return render(request, 'commute/commute_ovts.html', context)


@login_required(login_url='common:login')
def overtimewait(request):
    # 로그인 계정으로 등록한 휴가 리스트 가져오기
    myuser = get_object_or_404(MyUser, email=request.user.email)
    mylist = CmtHistory.objects.filter(approval='1').order_by('-startdatetime')
    
    # 페이지 당 10개씩 보여주기
    page = request.GET.get('page', '1')
    dt = request.GET.get('dt', '') # 검색일자
    ct = request.GET.get('ct', '') # 검색구분
    kw = request.GET.get('kw', '')  # 사용자

    if dt!='' and ct!='':
        mylist = mylist.filter(employee__realname__icontains=kw, todaycat__icontains=ct, startdatetime__gte=dt).distinct()
    elif dt == '' and ct != '':
        mylist = mylist.filter(employee__realname__icontains=kw, todaycat__icontains=ct).distinct()
    elif dt != '' and ct == '':
        mylist = mylist.filter(employee__realname__icontains=kw, startdatetime__gte=dt).distinct()
    else:
        mylist = mylist.filter(employee__realname__icontains=kw).distinct()
    paginator = Paginator(mylist, 10)
    page_obj = paginator.get_page(page)

    context = {'myuser': myuser, 'mylist': page_obj, 'page': page, 'kw': kw, 'dt': dt, 'ct': ct, 'totallist': mylist}
    return render(request, 'commute/commute_ovtw.html', context)



@login_required(login_url='common:login')
def overtimeaprv(request):
    myuser = get_object_or_404(MyUser, email=request.user.email)
    myreg_id = request.GET.get('myreg_id')
    result = request.GET.get('result')
    commute = get_object_or_404(CmtHistory, pk=myreg_id)
    # 관리자 또는 매니저인 경우
    if myuser.is_manager or myuser.is_admin:
        if result == "ok":
            commute.approval = "3"
            commute.save()
        elif result == "rtn":
            commute.approval = "2"
            commute.save()
        elif result == "bck":
            commute.approval = "1"
            commute.save()
    else:
        messages.error(request, '결재 권한이 없습니다')
    return redirect('commute:ovtw')


@login_required(login_url='common:login')
def overtimetoth(request):
    try:
        myuser = get_object_or_404(MyUser, email=request.user.email)
    except Exception as e:
        myuser = ''
        print(f"Exceiption occured:\n{e}")

    # 전체 출근내역 가져오기
    mylist = CmtHistory.objects.exclude(approval=1).order_by('-startdatetime')
    
    # 페이지 당 10개씩 보여주기
    page = request.GET.get('page', '1')
    dt = request.GET.get('dt', '') # 검색일자
    ct = request.GET.get('ct', '') # 검색구분
    kw = request.GET.get('kw', '')  # 오버타임

    if dt!='' and ct!='':
        mylist = mylist.filter(employee__realname__icontains=kw, todaycat__icontains=ct, startdatetime__gte=dt).distinct()
    elif dt == '' and ct != '':
        mylist = mylist.filter(employee__realname__icontains=kw, todaycat__icontains=ct).distinct()
    elif dt != '' and ct == '':
        mylist = mylist.filter(employee__realname__icontains=kw, startdatetime__gte=dt).distinct()
    else:
        mylist = mylist.filter(employee__realname__icontains=kw).distinct()
    paginator = Paginator(mylist, 10)
    page_obj = paginator.get_page(page)

    context = {'myuser':myuser, 'email': request.user.email, 'mylist': page_obj, 'page': page, 'kw': kw, 'dt': dt, 'ct': ct, 'totallist': mylist}

    return render(request, 'commute/commute_ovtt.html', context)