from django.contrib.auth import authenticate, login
from common.models import MyUser
from django.shortcuts import render, redirect, get_object_or_404
from common.admin import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from common.tokens import account_activation_token
from django.contrib import messages


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # 이메일로 계정 활성화하면 True로 변경된다.
            user.save()
            # login(request, user)  # 로그인

            current_site = get_current_site(request)
            message = render_to_string('common/user_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "계정을 활성화시키기 위해 발송 요청된 메일입니다."
            mail_to = user.email
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()

            messages.warning(request, "회원가입 시 사용하신 이메일로 인증 메일이 발송되었습니다. 메일을 확인하시고 계정을 활성화한 후 로그인하시기 바랍니다.")
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, 'common/signup.html', {'form': form})


# 계정 활성화 함수(토큰을 통해 인증)
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "계정 활성화가 성공적으로 반영되었습니다.")
        return redirect("index")
    else:
        messages.danger(request, "계정 활성화를 반영하지 못했습니다. 담당자에게 문의바랍니다.")
        return redirect("index")


@login_required(login_url='common:login')
def mypage(request):
    try:
        whois = get_object_or_404(MyUser, email=request.user.email)
    except Exception as e:
        whois = ''
        print(f"Exceiption occured:\n{e}")

    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            myuser = form.save(commit=False)
            myuser.updated_at = timezone.now()
            myuser.save()
            return redirect('index')
        else:
            is_fine = False
    else:
        is_fine = True
        form = UserChangeForm(instance=request.user)
    return render(request, 'common/mypage.html', {'myuser':whois, 'form': form, 'is_fine': is_fine, 'email': request.user.email})



@login_required(login_url='common:login')
def password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            # 비밀번호를 바꾸면 기존 세션과 일치하지 않게 되어 로그아웃된다. 이를 방지하기 위한 auth_hash 갱신.
            update_session_auth_hash(request, user)
            return redirect('common:mypage')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form':form}
    return render(request, 'common/password.html', context)


def send_email(request):
    subject = "message"
    to = ["donggyeong1129@gmail.com"]
    from_email = "saltluxinno22@naver.com"
    message = "네이버 SMTP 메일 발송 테스트"
    EmailMessage(subject=subject, body=message, to=to, from_email=from_email).send()

    return render(request, 'common/index.html')