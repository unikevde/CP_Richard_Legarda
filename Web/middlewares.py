from Web.models import Usuario, Switch

class SessionVariablesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("[Middleware] Ejecutando SessionVariablesMiddleware")

        if request.user.is_authenticated:  # Solo para usuarios autenticados
            print(f"[Middleware] Usuario autenticado: {request.user.username}")
            try:
                usuario = Usuario.objects.get(user=request.user.username)
                agencia = usuario.agencia
                switch = Switch.objects.filter(agencia=agencia).first()
                # Configurar las variables de la sesión
                request.session['user_name'] = usuario.nombre
                request.session['agencia_nombre'] = agencia.nombre if agencia else "Sin agencia"
                if switch:
                    request.session['switch_ip'] = switch.ip
                    request.session['switch_user'] = switch.userssh
                    request.session['switch_password'] = switch.passwordssh

                # Depuración
                print(f"[Middleware] Usuario: {usuario.nombre}")
                print(f"[Middleware] Agencia: {agencia.nombre if agencia else 'Sin agencia'}")
                print(f"[Middleware] Switch IP: {switch.ip if switch else 'No switch'}")   

            except Usuario.DoesNotExist:
                pass  # Maneja casos en que el usuario no está configurado correctamente

        response = self.get_response(request)
        return response