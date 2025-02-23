from django.db import models

# Create your models here.
class Agencia(models.Model):
     nombre = models.CharField(max_length=50)
     direccion = models.CharField(max_length=50)
     piso= models.PositiveIntegerField() 
     def __str__(self):
        return self.nombre       

class Usuario(models.Model):
    user = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    mail= models.CharField(max_length=50)
    activa = models.BooleanField(default=False)
    ultimoLogin = models.DateTimeField(auto_now=True)
    agencia= models.ForeignKey(Agencia, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    
class Switch(models.Model):
    nombre=models.CharField(max_length=50)
    userssh=models.CharField(max_length=30,default='NULL')  # Valor predeterminado)
    passwordssh= models.CharField(max_length=10,default='NULL')  # Valor predeterminado)
    ip = models.GenericIPAddressField()  # Cambiado a GenericIPAddressField
    piso = models.PositiveIntegerField()  # Cambiado a PositiveIntegerField
    agencia= models.ForeignKey(Agencia, on_delete=models.CASCADE)
    def __str__(self):
        return self.ip

