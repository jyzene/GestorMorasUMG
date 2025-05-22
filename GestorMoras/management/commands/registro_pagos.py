import json
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from GestorMoras.models import Estudiante, Cartera, Metodo_Pago, Tipo_cobro, Status_Pago
from datetime import date

class Command(BaseCommand):
    help = 'Registra pagos desde un JSON simulado'

    def handle(self, *args, **kwargs):
        # Supongamos que el JSON viene en un archivo local 'pagos.json'
        with open('data/pagos.json', 'r', encoding='utf-8') as f:
            pagos = json.load(f)

        for pago in pagos:
            try:
                # Obtener estudiante
                estudiante = Estudiante.objects.get(Carnet=pago['carnet_estudiante'])

                # Si tenemos id de cartera, buscamos el pago existente
                cartera = None
                if pago['cartera_id']:
                    cartera = Cartera.objects.filter(id=pago['cartera_id'], Estudiante=estudiante).first()

                # Si es mora o no existe el pago, creamos un registro nuevo
                if pago['es_mora'] or not cartera:
                    fecha_actual = date.today()

                    cartera = Cartera.objects.create(
                        Estudiante=estudiante,
                        Monto_pagar=pago['monto_pagado'],
                        Fecha_cobro=fecha_actual,
                        Metodo_pago=Metodo_Pago.objects.get(id=pago['metodo_pago_id']),
                        Tipo_cobro=Tipo_cobro.objects.get(id=pago['tipo_cobro_id']),
                        Status_pago=Status_Pago.objects.get(id=2),
                    )
                    self.stdout.write(self.style.SUCCESS(f'Pago registrado para estudiante {estudiante.Carnet}, nueva entrada creada.'))
                else:
                    # Actualizamos el pago existente
                    # Parsear fecha
                    fecha_pago = parse_datetime(pago['fecha_pago'])
                    cartera.Monto_pagar = pago['monto_pagado']
                    cartera.Fecha_pago = fecha_pago
                    cartera.Metodo_pago = Metodo_Pago.objects.get(id=pago['metodo_pago_id'])
                    cartera.Tipo_cobro = Tipo_cobro.objects.get(id=pago['tipo_cobro_id'])
                    cartera.Status_pago = Status_Pago.objects.get(id=1)
                    cartera.save()
                    self.stdout.write(self.style.SUCCESS(f'Pago actualizado para estudiante {estudiante.Carnet}, registro existente.'))

            except Estudiante.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Estudiante con carnet {pago["carnet_estudiante"]} no existe.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error procesando pago: {e}'))
