from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from wushu.Forms.CompetitionForm import CompetitionForm
from wushu.models import SportClubUser, SportsClub, Competition, Athlete
from wushu.models.EnumFields import EnumFields
from wushu.models.SandaAthlete import SandaAthlete
from wushu.services import general_methods


@login_required
def return_competitions(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    competitions = Competition.objects.all()

    return render(request, 'musabaka/musabakalar.html', {'competitions': competitions})


@login_required
def musabaka_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition_form = CompetitionForm()
    if request.method == 'POST':
        competition_form = CompetitionForm(request.POST)
        if competition_form.is_valid():
            competition_form.save()
            messages.success(request, 'Müsabaka Başarıyla Kaydedilmiştir.')

            return redirect('wushu:musabakalar')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'musabaka/musabaka-ekle.html',
                  {'competition_form': competition_form})


@login_required
def musabaka_duzenle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)
    athletes = SandaAthlete.objects.all()
    if musabaka.subBranch == EnumFields.SANDA:
        athletes = SandaAthlete.objects.filter(competition=musabaka.pk)
    competition_form = CompetitionForm(request.POST or None, instance=musabaka)
    if request.method == 'POST':
        if competition_form.is_valid():
            competition_form.save()
            messages.success(request, 'Müsabaka Başarıyla Güncellenmiştir.')

            return redirect('wushu:musabaka-duzenle', pk=pk)
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'musabaka/musabaka-duzenle.html',
                  {'competition_form': competition_form, 'competition': musabaka, 'athletes': athletes})


@login_required
def musabaka_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Competition.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Competition.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def musabaka_sporcu_sec(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    competition = Competition.objects.get(pk=pk)
    if user.groups.filter(name='KulupUye'):
        sc_user = SportClubUser.objects.get(user=user)
        clubsPk = []
        clubs = SportsClub.objects.filter(clubUser=sc_user)
        for club in clubs:
            clubsPk.append(club.pk)
        athletes = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct()
    elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        athletes = Athlete.objects.all()
    if request.method == 'POST':

        athletes1 = request.POST.getlist('selected_options')
        if athletes1:
            for x in athletes1:
                if competition.subBranch == 'SANDA':
                    athlete = Athlete.objects.get(pk=x)
                    sandaAthlete = SandaAthlete()
                    sandaAthlete.athlete = athlete
                    sandaAthlete.competition = competition
                    sandaAthlete.save()
        return redirect('wushu:musabaka-duzenle', pk=pk)
    return render(request, 'kulup/kusak-sinavi-sporcu-sec.html', {'athletes': athletes})


@login_required
def musabaka_sporcu_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = SandaAthlete.objects.get(pk=pk)
            athlete.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})
