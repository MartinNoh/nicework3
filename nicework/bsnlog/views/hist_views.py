from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from common.models import MyUser
from ..forms import BslHistoryForm
from ..models import BslHistory
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q


@login_required(login_url='common:login')
def history(request):
    # 로그인 계정으로 등록한 일지 리스트 가져오기
    myuser = get_object_or_404(MyUser, email=request.user.email)
    mylist = BslHistory.objects.filter(employee=myuser).order_by('-created_at')

    # 페이지 당 10개씩 보여주기
    page = request.GET.get('page', '1')
    dt = request.GET.get('dt', '') # 검색일자
    kw = request.GET.get('kw', '')  # 검색어
    if dt != '':
        mylist = mylist.filter(contents__icontains=kw, created_at__gte=dt).distinct()
    else:
        mylist = mylist.filter(contents__icontains=kw).distinct()
    paginator = Paginator(mylist, 10)    
    page_obj = paginator.get_page(page)

    context = {'myuser': myuser, 'mylist': page_obj, 'page': page, 'kw': kw, 'dt':dt}
    return render(request, 'bsnlog/bsnlog_hist.html', context)


@login_required(login_url='common:login')
def update(request, bsnlog_id):
    myuser = get_object_or_404(MyUser, email=request.user.email)
    
    businesslog = get_object_or_404(BslHistory, pk=bsnlog_id)

    # 관리자 또는 매니저인 경우
    if myuser.is_manager | myuser.is_admin:
        pass
    else:
        # 일지 작성자가 로그인한 계정과 다른지 확인
        if request.user != businesslog.employee:
            messages.error(request, '수정권한이 없습니다')
            return redirect('bsnlog:hist')

    if request.method == "POST": # 양식 작성하여 POST
        form = BslHistoryForm(request.POST)
        if form.is_valid():
            businesslog.contents = form.cleaned_data.get('contents')
            businesslog.updated_at = timezone.now()
            businesslog.save()

            if myuser.is_manager | myuser.is_admin:
                return redirect('bsnlog:toth')
            else:
                return redirect('bsnlog:hist')
    else: # GET 페이지 요청
        form = BslHistoryForm()

    context = {'form': form, 'bsnlog_id': businesslog.id, 'contents': businesslog.contents}
    return render(request, 'bsnlog/bsnlog_updt.html', context)


@login_required(login_url='common:login')
def delete(request, bsnlog_id):
    myuser = get_object_or_404(MyUser, email=request.user.email)

    businesslog = get_object_or_404(BslHistory, pk=bsnlog_id)
    # 관리자 또는 매니저인 경우
    if myuser.is_manager | myuser.is_admin:
        pass
    else:
        if request.user != businesslog.employee:
            messages.error(request, '삭제권한이 없습니다')
            return redirect('bsnlog:updt', bsnlog_id=businesslog.id)
    businesslog.delete()
    return redirect('bsnlog:hist')


@login_required(login_url='common:login')
def totalhistory(request):
    myuser = get_object_or_404(MyUser, email=request.user.email)

    # 전체 일지 리스트 가져오기
    mylist = BslHistory.objects.filter().order_by('-created_at')

    # 페이지 당 10개씩 보여주기
    page = request.GET.get('page', '1')
    dt = request.GET.get('dt', '') # 검색일자
    kw = request.GET.get('kw', '')  # 검색어
    if dt != '':
        mylist = mylist.filter(contents__icontains=kw, created_at__gte=dt).distinct()
    else:
        mylist = mylist.filter(contents__icontains=kw).distinct()
    paginator = Paginator(mylist, 10)    
    page_obj = paginator.get_page(page)

    context = {'myuser': myuser, 'mylist': page_obj, 'page': page, 'kw': kw, 'dt': dt, 'totallist': mylist}
    return render(request, 'bsnlog/bsnlog_toth.html', context)