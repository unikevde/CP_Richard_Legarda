from django.shortcuts import render,redirect
#from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.db import IntegrityError
from .registro import RegistroFrom,LoginForm
from .models import Agencia,Usuario,Switch
from django.core.mail import send_mail  # Importar la función para enviar correos
from django.contrib import messages  # Importa el módulo de mensajes
from django.contrib.auth.hashers import make_password

# Create your views here.
"""
def inicio(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            password = form.cleaned_data['password']
            try:
                usuario = Usuario.objects.get(user=user, password=password)
                # Autenticación exitosa
                request.session['user_id'] = usuario.id
                request.session['user_name'] = usuario.nombre  # Guarda el nombre en la sesión
                 # Obtener datos de la agencia y el switch
                agencia = usuario.agencia
                switch = Switch.objects.filter(agencia=agencia).first()
                if switch:
                    request.session['agencia_nombre'] = agencia.nombre
                    request.session['switch_ip'] = switch.ip
                    request.session['switch_user'] = switch.userssh
                    request.session['switch_password'] = switch.passwordssh
                else:
                    # Si no hay un switch asociado, manejar el caso
                    request.session['switch_ip'] = None 
                    
                return redirect('chatbot')  # Asegúrate de que 'inicio' sea el nombre correcto de tu URL
            except Usuario.DoesNotExist:
                form.add_error(None, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'inicio.html', {'form': form})

"""
"""
def registro(request):
    if request.method == 'GET':
        form = RegistroFrom()
        return render(request, 'registro.html', {'form': form})
    else:
        form = RegistroFrom(request.POST)
        if form.is_valid():
            #form.save()--Modificado 15/01/2025-

            usuario = form.save(commit=False)  # Crea el objeto pero no lo guarda aún
            #usuario.password = encriptar_contraseña(form.cleaned_data['password'])  # Modificación personalizada
            usuario.save()

            #----------Modificado 15/01/2025-----------------
            # Enviar un correo al administrador
            asunto = 'Nuevo registro de usuario'
            mensaje = f"El usuario {usuario.nombre} {usuario.apellido} ({usuario.user}) se ha registrado exitosamente."
            remitente = 'ricktkd@gmail.com'  # Cambia por tu correo
            destinatario = ['e1717193864@gmail.com']  # Correo del administrador

            try:
                send_mail(asunto, mensaje, remitente, destinatario)
                 # Agregar mensaje de éxito
                messages.success(request, 'El correo fue enviado correctamente.')
            except Exception as e:
                #messages.error(request, f"El registro fue exitoso, pero no se pudo enviar el correo: {e}")
                return render(request, 'registro.html', {
                "form": form, 
                "error": f"El registro fue exitoso, pero no se pudo enviar el correo: {e}"
                })
            #-----------------------------------------------   

            return redirect('inicio')  # Asegúrate de que 'inicio' sea el nombre correcto de tu URL
        return render(request, 'registro.html', {"form": form, "error": "Datos inválidos."})
    """
def inicio(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            password = form.cleaned_data['password']
            try:
                usuario = Usuario.objects.get(user=user, password=password)
                # Autenticar al usuario en el sistema de Django
                django_user = authenticate(request, username=user, password=password)
                if django_user:
                    login(request, django_user)  # Autenticación de Django
                    return redirect('chatbot')
                else:
                    form.add_error(None, 'Autenticación de Django fallida.')

            except Usuario.DoesNotExist:
                form.add_error(None, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'inicio.html', {'form': form})


def registro(request):
    if request.method == 'GET':
        form = RegistroFrom()
        return render(request, 'registro.html', {'form': form})
    else:
        form = RegistroFrom(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # Crea el objeto pero no lo guarda aún
            
            # Crea también el usuario en el modelo User de Django
            django_user = User.objects.create_user(
                username=usuario.user,
                password=usuario.password,  # Considera usar un campo de contraseña encriptada
            )

            usuario.save()  # Guarda el usuario en el modelo personalizado
            
            #---------------------------------------------
            # Enviar correo de confirmación
            asunto = 'Confirmación de registro'
            mensaje =f"""
    Hola {usuario.nombre},
    Tu registro en nuestra aplicación ha sido exitoso.Los datos de Registro son los siguientes:
        Usuario: {usuario.user}
        Nombre:{usuario.nombre}
        Apellido:{usuario.apellido}
        Agencia:{usuario.agencia}
                    
    Para la activación del servicio debes enviar por mesa de soporte el formulario F06V01-PRO-GTI-IOT-003 con la autorización de su Jefe Inmediato.

    Saludos,
    Unidad de Redes y Comunicaciones
    """

            remitente = 'ricktkd@gmail.com'
            destinatario = [usuario.mail]  # Debe ser una lista

            try:
                send_mail(asunto, mensaje, remitente, destinatario)
                messages.success(request, 'Registro exitoso. Se ha enviado un correo de confirmación.')
                print("Correo Enviado")
            except Exception as e:
                messages.error(request, f"El registro fue exitoso, pero no se pudo enviar el correo: {e}")
                print(f"Error al enviar el correo: {e}")
            #-------------------------------------------------------------------
            return redirect('condiciones')
        return render(request, 'registro.html', {"form": form, "error": "Datos inválidos."})

def salir(request):
    logout(request)
    return redirect('inicio')  # Redirige a la página de login u otra página de tu elección  

def chatbot(request):
    return render(request, 'chat.html')

def condiciones(request):
    return render(request, 'condiciones.html')
