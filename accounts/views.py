from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission, User
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, render_to_response
from accounts.forms import LoginForm, PermForm
from django.contrib import auth, messages

from wushu import urls
from wushu.models import MenuAthlete, MenuCoach, MenuReferee, MenuDirectory, MenuAdmin, MenuClubUser
from wushu.services import general_methods
from wushu.services.general_methods import show_urls


def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    if request.user.is_authenticated is True:
        return redirect('wushu:admin')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)

            if user.groups.all()[0].name == 'Antrenor':
                return redirect('wushu:antrenor')

            elif user.groups.all()[0].name == 'Hakem':
                return redirect('wushu:hakem')

            elif user.groups.all()[0].name == 'Sporcu':
                return redirect('wushu:sporcu')

            elif user.groups.all()[0].name == 'Yonetim':
                return redirect('wushu:federasyon')

            elif user.groups.all()[0].name == 'Admin':
                return redirect('wushu:admin')

            elif user.groups.all()[0].name == 'KulupUye':
                return redirect('wushu:kulup-uyesi')


            else:
                return redirect('accounts:logout')

        else:
            messages.add_message(request, messages.SUCCESS, 'Mail Adresi Ve Şifre Uyumsuzluğu')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


def forgot(request):
    if request.method == 'POST':
        mail = request.POST.get('username')
        obj = User.objects.filter(username=mail)
        if obj.count() != 0:
            obj = obj[0]
            password = User.objects.make_random_password()
            obj.set_password(password)
            # form.cleaned_data['password'] = make_password(form.cleaned_data['password'])
            user = obj.save()
            html_content = ''
            subject, from_email, to = 'TWF Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@twf.gov.tr', obj.email
            html_content = '<h2>Aşağıda ki bilgileri kullanarak sisteme giriş yapabilirsiniz.</h2>'
            html_content = html_content+'<p> <strong>Site adresi:</strong> <a href="http://sbs.twf.gov.tr:81"></a>sbs.twf.gov.tr:81</p>'
            html_content = html_content + '<p><strong>Kullanıcı Adı:</strong>' + obj.username + '</p>'
            html_content = html_content + '<p><strong>Şifre:</strong>' + password + '</p>'
            msg = EmailMultiAlternatives(subject, '', from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Giriş bilgileriniz mail adresinize gönderildi. ")
            return redirect("accounts:login")
        else:
            messages.warning(request, "Geçerli bir mail adresi giriniz.")
            return redirect("accounts:forgot")

    return render(request, 'registration/forgot-password.html')


def pagelogout(request):
    logout(request)
    return redirect('accounts:login')


def groups(request):
    group = Group.objects.all()

    return render(request, 'permission/groups.html', {'groups': group})


@login_required
def permission(request, pk):
    general_methods.show_urls(urls.urlpatterns, 0)
    group = Group.objects.get(pk=pk)
    menu = ""
    ownMenu = ""

    groups = group.permissions.all()
    per = []
    menu2 = []

    for gr in groups:
        per.append(gr.codename)

    ownMenu = group.permissions.all()

    menu = Permission.objects.all()

    for men in menu:
        if men.codename in per:
            print("echo")
        else:
            menu2.append(men)

    return render(request, 'permission/izin-ayar.html',
                  {'menu': menu2, 'ownmenu': ownMenu, 'group': group})


@login_required
def permission_post(request):
    if request.POST:
        try:
            permissions = request.POST.getlist('values[]')
            group = Group.objects.get(pk=request.POST.get('group'))

            group.permissions.clear()
            group.save()
            if len(permissions) == 0:
                return JsonResponse({'status': 'Success', 'messages': 'Sınıf listesi boş'})
            else:
                for id in permissions:
                    perm = Permission.objects.get(pk=id)
                    group.permissions.add(perm)

            group.save()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Permission.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
