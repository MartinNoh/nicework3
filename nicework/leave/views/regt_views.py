from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from common.models import MyUser
from ..models import LevHistory, Reward
from commute.models import CmtHistory
from ..forms import LevHistoryForm
import datetime
from dateutil.relativedelta import relativedelta
from .hist_views import get_leave_hwp


@login_required(login_url='common:login')
def registration(request):
    # 오전반차의 경우 종료시간, 오후반차의 경우 시작시간 계산
    myuser = get_object_or_404(MyUser, email=request.user.email)
    if myuser.is_manager or myuser.is_admin:
        return redirect('leave:wait')

    closing_time = myuser.closingtime
    opening_time = myuser.openingtime
    time_diff = datetime.datetime.combine(datetime.date.today(), closing_time) - datetime.datetime.combine(datetime.date.today(), opening_time)
    t_diff = time_diff.days*24 + time_diff.seconds/3600
    if t_diff >= 8:
        breaktime = 1
    elif t_diff >= 4:
        breaktime = 0.5
    else:
        breaktime = 0
    h_diff = (t_diff - breaktime)/2
    mo_endtime = datetime.datetime.combine(datetime.date.today(), opening_time) + datetime.timedelta(hours=h_diff)
    ao_starttime = datetime.datetime.combine(datetime.date.today(), closing_time) - datetime.timedelta(hours=h_diff)
    mo_endtime = mo_endtime.time()
    ao_starttime = ao_starttime.time()

    # 총 누적 연장근로시간
    commute_history_list = CmtHistory.objects.filter(employee=myuser, approval=3)
    sum_overtime = 0
    for i in commute_history_list:
        sum_overtime = sum_overtime + i.overtime
    sum_overtime = round(sum_overtime, 1)
    # 연장근로시간 휴가 대체 여부
    is_sbstt = myuser.is_sbstt
    # 총 누적 연차
    if myuser.is_over80p:
        sum_annual = 15
    else:
        delta = relativedelta(datetime.date.today(), myuser.effcdate)
        sum_annual = 12 * delta.years + delta.months
    sum_annual = round(sum_annual, 1)
    # 총 누적 포상휴가
    reward_history_list = Reward.objects.filter(employee=myuser)
    sum_reward = 0
    for i in reward_history_list:
        sum_reward = sum_reward + i.days
    sum_reward = round(sum_reward, 1)
    # 총 누적 휴가
    workinghours = 0
    if is_sbstt:
        closingtime = myuser.closingtime
        openingtime = myuser.openingtime
        time_diff = datetime.datetime.combine(datetime.date.today(), closingtime) - datetime.datetime.combine(datetime.date.today(), openingtime)
        t_diff = time_diff.days*24 + time_diff.seconds/3600
        if t_diff >= 8:
            breaktime = 1
        elif t_diff >= 4:
            breaktime = 0.5
        else:
            breaktime = 0
        workinghours = t_diff-breaktime
        div_cal = sum_overtime/workinghours
        div_share = sum_overtime//workinghours
        div_remain = div_cal - div_share
        sum_ovt = div_share + 0.5 if div_remain >= 0.5 else div_share
        total_leave = round(sum_ovt, 1) + sum_annual + sum_reward
    else:
        total_leave = sum_annual + sum_reward
    total_leave = round(total_leave, 1)
    # 사용한 휴가
    used_leave_list = LevHistory.objects.filter(employee=myuser, approval__in=['1', '3'])
    sum_used_leave = 0
    for i in used_leave_list:
        sum_used_leave = sum_used_leave + i.leaveterm
    # 잔여 휴가
    remained = total_leave - sum_used_leave
    remained = round(remained, 1)

    if request.method == "POST":
        form = LevHistoryForm(request.POST)
        # POST 요청 저장
        if form.is_valid():
            # 기존 휴가와 겹치는 내용의 신청은 기각
            startdate = str(request.POST.get('startdate'))
            enddate = str(request.POST.get('enddate'))
            start_within_period = LevHistory.objects.filter(employee=myuser, startdate__range=[startdate, enddate])
            start_within_period = LevHistory.objects.filter(employee=myuser, startdate__gte=startdate, startdate__lte=enddate)
            end_within_period = LevHistory.objects.filter(employee=myuser, enddate__gte=startdate, enddate__lte=enddate)
            if start_within_period or end_within_period:
                messages.error(request, '휴가 신청 내역에 겹치는 기간이 있습니다.')
            else:
                if str(request.POST.get('leavecat')) in ["MO", "AO", "EL"]:
                    starttime = form.cleaned_data.get('starttime')
                    endtime = form.cleaned_data.get('endtime')
                    leave_time_diff = datetime.datetime.combine(datetime.date.today(), endtime) - datetime.datetime.combine(datetime.date.today(), starttime)
                    l_diff = leave_time_diff.days*24 + leave_time_diff.seconds/3600
                    leaveterm = l_diff / (t_diff - breaktime)
                else:
                    start_date = datetime.datetime(int(startdate.split("-")[0]), int(startdate.split("-")[1]), int(startdate.split("-")[2]))
                    end_date = datetime.datetime(int(enddate.split("-")[0]), int(enddate.split("-")[1]), int(enddate.split("-")[2]))
                    leaveterm = end_date - start_date + datetime.timedelta(days=1)
                    leaveterm = float(leaveterm.days)

                if leaveterm > remained:
                    messages.error(request, '잔여 연차는 ' + str(remained) + '일이므로, ' + str(leaveterm) + '일 신청은 불가합니다.')
                    return redirect('leave:regt')
                else:
                    leave_reg = form.save(commit=False)
                    leave_reg.employee = myuser
                    leave_reg.leaveterm = leaveterm    
                    leave_reg.save()

                    # return redirect('leave:hist')
                    data = {'created_at': leave_reg.created_at, 'reason': leave_reg.reason, 'startdate': leave_reg.startdate, 'enddate': leave_reg.enddate, 'leaveterm': leave_reg.leaveterm, 'leavecat': leave_reg.leavecat}
                    context = {'source_html': get_leave_hwp(data, myuser)}
                    return render(request, 'leave/leave_temp.html', context)
    else: # GET 페이지 요청
        form = LevHistoryForm()
    context = {'myuser':myuser, 'form': form, 'sum_overtime':sum_overtime, 'is_sbstt':is_sbstt, 'sum_annual':sum_annual, 'sum_reward':sum_reward, 'total_leave':total_leave, 'sum_used_leave':sum_used_leave, 'remained':remained,
        'opening_time': str(opening_time), 'closing_time': str(closing_time), 'mo_endtime': str(mo_endtime), 'ao_starttime': str(ao_starttime), 't_diff': t_diff, 'h_diff': h_diff}
    
    return render(request, 'leave/leave_regt.html', context)