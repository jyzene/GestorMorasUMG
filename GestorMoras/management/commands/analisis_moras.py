from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from GestorMoras.models import Cartera, Estudiante, Status_Pago, Tipo_cobro, Status_Estudiante,Metodo_Pago
from datetime import datetime, date

def obtener_fecha_diez_mes_actual():
    """
    Retorna una fecha con el día 10 del mes y año actual.
    Ejemplo: si hoy es 21 de mayo de 2025, devuelve 2025-05-10
    """
    hoy = datetime.now()
    return date(hoy.year, hoy.month, 10)

class Command(BaseCommand):
    help = 'Valida pagos vencidos y asigna moras'

    def handle(self, *args, **kwargs):
        fecha_hoy = date.today()

        # IDs de estados relevantes
        status_pendiente = Status_Pago.objects.get(descripcion ='Pendiente')
        status_mora = Status_Pago.objects.get(descripcion ='En mora')
        tipo_mora = Tipo_cobro.objects.get(descripcion ='Multa')
        estatus_mora = Status_Estudiante.objects.get(descripcion='Moroso')
        metodo_pago = Metodo_Pago.objects.get(descripcion='Sin Especificar')

        # Iterar sobre todas las carteras con pagos pendientes
        carteras_pendientes = Cartera.objects.filter(Status_pago=status_pendiente)

        for cartera in carteras_pendientes:
            fecha_limite = obtener_fecha_diez_mes_actual()
            print('date ', fecha_limite)
            print('date ', fecha_hoy)
            if fecha_limite and fecha_hoy > fecha_limite:
                estudiante = cartera.Estudiante
                print('estudiante con mora')

                # Cambiar el status del pago original
                cartera.Status_pago = status_mora
                print(cartera.Status_pago)
                cartera.save()

                # Crear nueva mora (si aún no existe una para ese estudiante y fecha)

                Cartera.objects.create(
                    Estudiante=estudiante,
                    Monto_pagar=45.00,  # o el valor que decidas como mora
                    Fecha_pago=None,
                    Metodo_pago=metodo_pago,
                    Tipo_cobro=tipo_mora,
                    Status_pago=status_pendiente,
                    Fecha_cobro=date.today(),
                )

                # print(str(estudiante))
                print('monto a pagar: 45.00')
                print(tipo_mora)
                print(status_pendiente)

                # Cambiar el estado del estudiante si aún no está marcado
                if estudiante.Estatus != estatus_mora:
                    estudiante.Estatus = estatus_mora
                    print(estudiante.Estatus)
                    estudiante.save()

                self.stdout.write(self.style.WARNING(
                    f"Mora generada para {estudiante.Carnet} y status actualizado."
                ))

        self.stdout.write(self.style.SUCCESS("Proceso de moras finalizado."))
