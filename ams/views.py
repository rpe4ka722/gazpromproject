from django.shortcuts import render


def ams(request):
    return render(request, 'ams/templates/main_ams.html')
