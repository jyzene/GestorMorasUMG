# moras/views.py

from django.shortcuts import render, get_object_or_404
from .forms import BuscarEstudianteForm
from .models import Estudiante, Cartera

def buscar_estudiante(request):
    form = BuscarEstudianteForm()
    estudiante = None
    pagos = []

    if request.method == 'POST':
        form = BuscarEstudianteForm(request.POST)
        if form.is_valid():
            carnet = form.cleaned_data['carnet']
            try:
                estudiante = Estudiante.objects.get(Carnet=carnet)
                pagos = Cartera.objects.filter(Estudiante=estudiante)
            except Estudiante.DoesNotExist:
                estudiante = None
                pagos = []

    context = {
        'form': form,
        'estudiante': estudiante,
        'pagos': pagos
    }
    return render(request, 'moras/buscar_estudiante.html', context)
