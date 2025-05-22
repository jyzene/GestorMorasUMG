from django.db import models

# Create your models here.
class Status_Estudiante(models.Model):
    descripcion = models.CharField(max_length=25)

    def __str__(self):
        return self.descripcion
    
class Status_Pago(models.Model):
    descripcion = models.CharField(max_length=25)

    def __str__(self):
        return self.descripcion
    
class Metodo_Pago(models.Model):
    descripcion = models.CharField(max_length=25)

    def __str__(self):
        return self.descripcion
    
class Tipo_cobro(models.Model):
    descripcion = models.CharField(max_length=25)

    def __str__(self):
        return self.descripcion


class Estudiante(models.Model):
    Nombres = models.CharField(max_length=100)
    Apellidos = models.CharField(max_length=100)
    Carnet = models.IntegerField()
    Direccion = models.CharField(max_length=100)
    Telefono = models.IntegerField()
    Correo_electronico = models.EmailField(unique=True)
    Estatus = models.ForeignKey(Status_Estudiante,on_delete = models.CASCADE,related_name='status_estudiante')

    def __str__(self):
        return self.Carnet
    
class Cartera(models.Model):
    Estudiante = models.ForeignKey(Estudiante,on_delete = models.CASCADE,related_name='estudiante')
    Monto_pagar = models.DecimalField(max_digits=8,decimal_places=2)
    Fecha_cobro = models.DateField()
    Fecha_pago = models.DateTimeField(null=True)
    Metodo_pago = models.ForeignKey(Metodo_Pago,on_delete = models.CASCADE,related_name='metodos')
    Tipo_cobro = models.ForeignKey(Tipo_cobro,on_delete = models.CASCADE,related_name='tipo_cobro')
    Status_pago = models.ForeignKey(Status_Pago,on_delete = models.CASCADE,related_name='status_pago')

    def __str__(self):
        return self.Estudiante