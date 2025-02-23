from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
import re
from .procesamientoLenguajeN import predecir_intencion, obtener_respuesta
from .configurarSw import buscar_mac,muestra_puerto,configurar_puerto,guardar_configuracion

# Cargar el archivo de intenciones
with open("Web/intents.json", "r", encoding="utf-8") as file:
    intents = json.load(file)

def validar_mac(mac):
    # Expresión regular para validar formato direccion MAC
    patron_mac = re.compile(r"^[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}$")
    return bool(patron_mac.match(mac))

def es_vlan_valida(vlan):
    """
    Valida si la VLAN es 12 o 13.
    """
    return vlan in ['12', '13']

# @login_required  # Proteger la vista
@login_required(login_url='/inicio/')
@csrf_exempt

def chatbot_view(request):
    if request.method == 'GET':
         # Las variables de sesión deberían estar configuradas aquí
        print(f"[chatbot_view] user_name: {request.session.get('user_name')}")
        print(f"[chatbot_view] agencia_nombre: {request.session.get('agencia_nombre')}")
        print(f"[chatbot_view] switch_ip: {request.session.get('switch_ip')}")
        print(f"[chatbot_view] switch_user: {request.session.get('switch_user')}")
        print(f"[chatbot_view] switch_password: {request.session.get('switch_password')}")

        # Las variables necesarias ya están disponibles en la sesión gracias al middleware
        return render(request, 'chat.html', {
            'user_name': request.session.get('user_name'),
            'agencia_nombre': request.session.get('agencia_nombre'),
            'switch_ip': request.session.get('switch_ip'),
            'switch_user': request.session.get('switch_user'),
            'switch_password': request.session.get('switch_password'),
        })

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje', '').strip()

            if not mensaje:
                return JsonResponse({'respuesta': "Por favor, ingresa un mensaje válido."})

            switch_ip = request.session.get('switch_ip')
            switch_user = request.session.get('switch_user')
            switch_password = request.session.get('switch_password')

            estado_intencion = request.session.get('estado_intencion')
            # Obtener el estado actual de la sesión
            estado_intencion = request.session.get('estado_intencion')

            if estado_intencion == "buscar_equipo":
                # Verificar si el mensaje es una dirección MAC
                if validar_mac(mensaje):
                    try:
                        resultado = buscar_mac(mensaje,switch_ip,switch_user,switch_password)
                        #ultimos_seis = resultado[-10:]
                        request.session['estado_intencion'] = None  # Reiniciar estado
                        return JsonResponse({'respuesta': f"<strong>Resultado de la búsqueda:</strong><br>"
                                             f"Tu equipo está conectado en el puerto <span style='color: blue;'>{resultado[-6:]}</span><br>"
                                             f"Te sugiero revisar la configuracion del puerto <span style='color: blue;'>{resultado[-6:]}</span><br><br>"
                                             f"<strong>¿Que deseas hacer?</strong> "})
                    except ValueError as e:
                        return JsonResponse({'respuesta': str(e)})
                else:
                    return JsonResponse({'respuesta': "<span style='color: red;'>Por favor, ingresa una dirección MAC válida.El formato correcto es:tres grupos de cuatro dígitos hexadecimales separados por puntos,ejemplo:ab12.cd34.56ef</span>"})

            if estado_intencion == "ver_puerto":
                # Verificar el formato del puerto (e.g., 1/0)
                if "/" in mensaje and len(mensaje.split("/")) == 2:
                    try:
                        resultado = muestra_puerto(mensaje,switch_ip,switch_user,switch_password)
                        request.session['estado_intencion'] = None  # Reiniciar estado

                        return JsonResponse({'respuesta': f"La configuración del puerto <span style='color: blue;'>Gi{mensaje}</span> es la siguiente:<br>"
                                  #f"{resultado[60:]}\n\n"
                                  f"<pre style='font-family: monospace; color: #4a90e2;'>{resultado[60:]}</pre><br>"
                                  f"Ahora que conoces los detalles del puerto puedes seguir con la configuracion te sugiero que configures la <span style='color: blue;'>VLAN</span><br><br>"
                                  f"<strong>¿ Que deseas hacer ?</strong>"})
                    except ValueError as e:
                        return JsonResponse({'respuesta': str(e)})
                else:
                    return JsonResponse({'respuesta': "<span style='color: red;'>Por favor, ingresa un puerto válido en el formato número/número.</span>"})
                

            if estado_intencion == "configurar_vlan":
                if "vlan" not in request.session:
                    if mensaje.isdigit() and es_vlan_valida(mensaje):  # Validar si el mensaje es un número (VLAN)
                        request.session['vlan'] = mensaje
                        vlan = request.session['vlan']
                        return JsonResponse({'respuesta': f"<span style='color: blue;'>VLAN {vlan} registrada. </span> <br>" 
                                                          f"<strong> Ahora ingresa el número puerto con el formato (número / número).</strong>"})
                    else:
                        return JsonResponse({'respuesta': "<span style='color: red;'>Por favor, ingresa un número válido para la VLAN.</span>"})

                elif "puerto" not in request.session:
                    if "/" in mensaje and len(mensaje.split("/")) == 2:  # Validar formato del puerto
                        request.session['puerto'] = mensaje
                        puerto = request.session['puerto']
                        return JsonResponse({'respuesta': f"<span style='color: blue;'>Puerto {puerto} registrado.</span> <br>"
                                                          f"<strong>Ahora ingresa una descripción para el puerto.</strong>"})
                    else:
                        return JsonResponse({'respuesta': "<span style='color: red;'>Por favor, ingresa un puerto válido en el formato (número / número).</span>"})

                elif "descripcion" not in request.session:
                    request.session['descripcion'] = mensaje
                    descripcion = request.session['descripcion']
                    vlan = request.session['vlan']
                    puerto = request.session['puerto']
                    try:
                        resultado = configurar_puerto(vlan, puerto, descripcion, switch_ip, switch_user, switch_password)
                        # Limpiar variables de sesión relacionadas
                        del request.session['vlan']
                        del request.session['puerto']
                        del request.session['descripcion']
                        request.session['estado_intencion'] = None
                        return JsonResponse({'respuesta': f"<span style='color: blue;'>Descripción registrada</span> <br>"
                                                          f"Procediendo a configurar el puerto con los parámetros ingresados.....<br>"
                                                          f"<pre style='font-family: monospace; color: #4a90e2;'>Switch:{switch_ip}... {resultado}</pre><br>"})
                    except ValueError as e:
                        return JsonResponse({'respuesta': str(e)})
        
            # Modificado 23/01/2025
           
            if estado_intencion == "guardar_configuracion":
                if mensaje.lower() == "si":
                    try:
                        resultado = guardar_configuracion(switch_ip,switch_user,switch_password)
                        request.session['estado_intencion'] = None  # Reiniciar estado
                        return JsonResponse({'respuesta': f"<strong>Resultado:</strong><br>"
                                            f"<pre style='font-family: monospace; color: #4a90e2;'>GRUB configuration was written to disk successfully Switch {switch_ip}</pre>"
                                            f"<pre style='font-family: monospace; color: #4a90e2;'>{resultado}</pre>"})
                    except ValueError as e:
                        return JsonResponse({'respuesta': str(e)})
                else:
                     # Si el mensaje no es "si", pedir confirmación nuevamente
                 return JsonResponse({'respuesta': "¿Estás seguro de que deseas guardar la configuración? Responde 'SI' para confirmar."})
            # Si no hay estado, predecir intención
            intencion = predecir_intencion(mensaje)
            if intencion is None:
                return JsonResponse({'respuesta': "Estoy diseñado para configurar los puertos de un switch.¿ Podrías darme más detalles ?"})

            # Manejo de intenciones
            if intencion == "saludo":
                request.session['estado_intencion'] = None
                respuesta = obtener_respuesta(intencion, intents)
                return JsonResponse({'respuesta': respuesta})

            elif intencion == "red":
                request.session['estado_intencion'] = None
                # Obtener la respuesta original desde los intents
                respuesta_original = obtener_respuesta(intencion, intents)
                # Reemplazar las comas con saltos de línea
                respuesta_formateada = respuesta_original.replace(",", "<br>")
                #return JsonResponse({'respuesta': respuesta_formateada})
                return JsonResponse({'respuesta': f"{respuesta_formateada}<br><br>"
                                     f"<strong>¿Dime que vas a realizar?</strong>"})

            elif intencion == "buscar_equipo":
                request.session['estado_intencion'] = "buscar_equipo"
                # Obtener la respuesta original desde los intents
                respuesta_original = obtener_respuesta(intencion, intents)
                # Reemplazar las comas con saltos de línea
                respuesta_formateada = respuesta_original.replace(",", "<br>")
                #return JsonResponse({'respuesta': respuesta_formateada})
                return JsonResponse({'respuesta': f"{respuesta_formateada}<br><br>"
                                     f"<strong>El paso siguiente es ingresar la direccion MAC</strong>"})

            elif intencion == "ver_puerto":
                request.session['estado_intencion'] = "ver_puerto"
                respuesta = obtener_respuesta(intencion, intents)
                #return JsonResponse({'respuesta': respuesta})
                return JsonResponse({'respuesta': f"{respuesta}<br><br>"
                                     f"<strong>¿Cual es el numero de puerto?</strong>"})

            if intencion == "configurar_vlan":
                request.session['estado_intencion'] = "configurar_vlan"
                respuesta = obtener_respuesta(intencion, intents)
               # respuesta_formateada = respuesta.replace(".", "<br>")
               # return JsonResponse({'respuesta': respuesta})
                return JsonResponse({'respuesta': f"{respuesta}<br><br>"
                                     f"<strong>¿Cual es el numero de Vlan a configurar en el puerto?</strong>"})

            elif intencion == "guardar_configuracion":
                request.session['estado_intencion'] = "guardar_configuracion"
                respuesta = obtener_respuesta(intencion, intents)
                return JsonResponse({'respuesta': f"{respuesta}<br>"
                                     f"Escribe <span style='color: blue;'>Si </span> para <span style='color: blue;'>Guardar </span>" })

            else:
                request.session['estado_intencion'] = None
                respuesta = "Lo siento, no entiendo tu solicitud.Utiliza terminos relacionados con la red"

            return JsonResponse({'respuesta': respuesta})

        except json.JSONDecodeError:
            return JsonResponse({'respuesta': "Formato de solicitud no válido. Asegúrate de enviar datos JSON correctamente."})

    return JsonResponse({'error': 'Método no permitido'}, status=405)