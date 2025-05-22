from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, date
from GestorMoras.models import Cartera, Estudiante, Status_Pago, Tipo_cobro, Status_Estudiante

class Command(BaseCommand):
    help = 'Valida pagos vencidos y asigna moras'

    def handle(self, *args, **kwargs):
        hoy = timezone.now().date()

        # IDs de estados relevantes
        status_pendiente = Status_Pago.objects.get(descripcion ='Pendiente')
        status_mora = Status_Pago.objects.get(descripcion ='En mora')
        tipo_mora = Tipo_cobro.objects.get(descripcion ='Multa')
        estatus_mora = Status_Estudiante.objects.get(descripcion='Moroso')

        # Iterar sobre todas las carteras con pagos pendientes
        carteras_pendientes = Cartera.objects.filter(Status_pago=status_pendiente)

        for cartera in carteras_pendientes:
            fecha_limite = cartera.Fecha_cobro.date() if cartera.Fecha_cobro else None

            if fecha_limite and hoy > fecha_limite:
                estudiante = cartera.Estudiante

                # Cambiar el status del pago original
                cartera.Status_pago = status_mora
                cartera.save()

                # Crear nueva mora (si aún no existe una para ese estudiante y fecha)
                Cartera.objects.create(
                    Estudiante=estudiante,
                    Monto_pagar=45.00,  # o el valor que decidas como mora
                    Fecha_pago=None,
                    Metodo_pago=None,
                    Tipo_cobro=tipo_mora,
                    Status_pago=status_pendiente,
                    Fecha_cobro=date.today(),
                )

                # Cambiar el estado del estudiante si aún no está marcado
                if estudiante.Estatus != estatus_mora:
                    estudiante.Estatus = estatus_mora
                    estudiante.save()

                self.stdout.write(self.style.WARNING(
                    f"Mora generada para {estudiante.Carnet} y status actualizado."
                ))

        self.stdout.write(self.style.SUCCESS("Proceso de moras finalizado."))
