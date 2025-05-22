# moras/forms.py

from django import forms

class BuscarEstudianteForm(forms.Form):
    carnet = forms.IntegerField(
        label="Número de Carnet",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el número de carnet'
        })
    )
