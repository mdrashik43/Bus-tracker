from django.shortcuts import render
from django.http import JsonResponse
from .models import Bus


def home(request):
    return render(request, 'home.html')


def student_map(request):
    return render(request, 'student_map.html')


def supervisor_panel(request):
    buses = Bus.objects.all()
    return render(request, 'supervisor_panel.html', {'buses': buses})


def api_buses(request):
    buses = Bus.objects.all().values('id', 'name', 'route', 'is_active')
    return JsonResponse(list(buses), safe=False)