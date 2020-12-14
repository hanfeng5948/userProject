
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password, make_password
import random

def registerView(request):
    title = '注册'
    pageTitle = '用户注册'
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        if User.objects.filter(username=u):
            tips = '用户已存在'
        else:
            d = dict(username=u, password=p, is_staff=1, is_superuser=1)
            user = User.objects.create_user(**d)
            user.save()
            tips = '注册成功，请登录'
    return render(request, 'user.html', locals())


def loginView(request):
    title = '登录'
    pageTitle = '用户登录'
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        if User.objects.filter(username=u):
            user = authenticate(username=u, password=p)
            if user:
                if user.is_active:
                    login(request, user)
                return HttpResponse('登录成功')
            else:
                tips = '账号密码错误，请重新输入'
        else:
            tips = '用户不存在，请注册'
    return render(request, 'user.html', locals())


def setpsView(request):
    title = '修改密码'
    pageTitle = '密码修改'
    password2 = True
    if request.method == 'POST':
        u = request.POST.get('username', '')
        p = request.POST.get('password', '')
        p2 = request.POST.get('password2', '')
        if User.objects.filter(username=u):
            user = authenticate(username=u, password=p)
            if user:
                dj_ps = make_password(p2, None, 'pbkdf2_sha256')
                if check_password(p, dj_ps):
                    tips = '和原始密码相同，请更改密码'
                else:
                    user.set_password(p2)
                    user.save()
                    tips = '密码修改成功'
            else:
                tips = '原始密码不正确'
        else:
            tips = '用户不存在'
    return render(request, 'user.html', locals())


def logoutView(request):
    logout(request)
    return HttpResponse('注销成功')


def findpsView(request):
    button = '获取验证码'
    VCodeInfo = False
    password = False
    if request.method == 'POST':
        u = request.POST.get('username')
        VCode = request.POST.get('VCode', '')
        p = request.POST.get('password')
        user = User.objects.filter(username=u)
        if not user:
            tips = '用户不存在'
        else:
            if not request.session.get('VCode', ''):
                button = '重置密码'
                tips = '验证码已经发送'
                password = True
                VCodeInfo = True
                VCode = str(random.randint(1000,9999))
                request.session['VCode'] = VCode
                user[0].email_user('找回密码', VCode)
            elif VCode == request.session.get('VCode'):
                dj_ps = make_password(p, None, 'pbkdf2_sha256')
                user[0].password = dj_ps
                user[0].save()
                del request.session['VCode']
                tips = '密码已经重置'
            else:
                tips = '验证码错误，请重新获取'
                VCodeInfo = False
                password = False
                del request.session['VCode']
        return render(request, 'user.html', locals())
