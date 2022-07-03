from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from common.models import MyUser
from ..forms import BslHistoryForm
from ..models import BslHistory
from django.utils import timezone
import datetime


@login_required(login_url='common:login')
def registration(request):
    # 오늘 등록했던 일지 가져오기
    myuser = get_object_or_404(MyUser, email=request.user.email)
        
    today_start = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0, 0))
    today_end = datetime.datetime.combine(datetime.date.today(), datetime.time(23, 59 ,59))
    mylist = BslHistory.objects.filter(employee=myuser, created_at__gte=today_start, created_at__lte=today_end).order_by('-created_at')

    if request.method == "POST": # 양식 작성하여 POST
        form = BslHistoryForm(request.POST)
        if form.is_valid():
            contents = form.cleaned_data.get('contents')
            if mylist: # 오늘 일지 있다. -> contents, updated_at 수정
                mylist[0].contents = contents
                mylist[0].updated_at = timezone.now()
                mylist[0].save()
            else: # 오늘 일지 없다. -> 생성
                BslHistory.objects.create(employee=myuser, contents=contents, updated_at=timezone.now())
            return redirect('bsnlog:regt')
    else: # GET 페이지 요청
        form = BslHistoryForm()
    
    context = {
        'myuser': myuser,
        'form': form, 
        'contents': mylist[0].contents if mylist else ''
    }
    return render(request, 'bsnlog/bsnlog_regt.html', context)


@login_required(login_url='common:login')
def situation(request):
    try:
        myuser = get_object_or_404(MyUser, email=request.user.email)
    except Exception as e:
        myuser = ''
        print(f"Exceiption occured:\n{e}")

    # 오늘 등록했던 팀원들의 일지 가져오기
    today_start = datetime.datetime.combine(datetime.date.today(), datetime.time(0, 0, 0))
    today_end = datetime.datetime.combine(datetime.date.today(), datetime.time(23, 59 ,59))
    mylist = BslHistory.objects.filter(created_at__gte=today_start, created_at__lte=today_end).order_by('-created_at')
    context = {'myuser':myuser, 'mylist':mylist}
    return render(request, 'bsnlog/bsnlog_situ.html', context)