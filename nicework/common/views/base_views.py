from django.shortcuts import render, redirect, get_object_or_404
from common.models import MyUser
import logging
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    user_ip = get_client_ip(request)
    logger.info("접속한 PC의 IP : " + str(user_ip))

    try:
        myuser = get_object_or_404(MyUser, email=request.user.email)
    except Exception as e:
        myuser = ''
        print(f"Exceiption occured:\n{e}")
    context = {'myuser': myuser}
    return render(request, 'common/index.html', context)


def privacy_policy(request):
    context = {}
    return render(request, 'common/privacy_policy.html', context)


def terms_of_service(request):
    context = {}
    return render(request, 'common/terms_of_service.html', context)


def page_not_found(request, exception):
    return render(request, 'common/404.html', {})


def server_error(request, *args, **argv):
    return render(request, 'common/500.html', {})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip