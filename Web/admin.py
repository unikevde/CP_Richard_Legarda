from django.contrib import admin
from .models import Agencia,Usuario,Switch # Importa los modelos necesarios

# Register your models here.
# Registra los modelos en la interfaz de administración
admin.site.register(Agencia)
admin.site.register(Usuario)
admin.site.register(Switch)
