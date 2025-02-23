import netmiko
from netmiko import ConnectHandler,NetmikoAuthenticationException, NetmikoTimeoutException

def buscar_mac(mac,switch_ip,switch_user,switch_password):
    
    # Datos de conexión al dispositivo
    device = {
        "device_type": "cisco_ios",  # Tipo de dispositivo (puede variar según el fabricante)
        "host": switch_ip,       # Dirección IP o hostname del dispositivo
        "username": switch_user,         # Usuario
        "password": switch_password,   # Contraseña
    }
    try:
        # Establecer conexión con el dispositivo
        connection = ConnectHandler(**device)
        # Ejecutar el comando y obtener la salida
        output = connection.send_command("show mac address-table | include "+mac)
        connection.disconnect()
        return output
    except NetmikoAuthenticationException:
        raise ValueError("Error de autenticación: verifica el usuario o la contraseña.")
    except NetmikoTimeoutException:
        raise ValueError("Error de conexión: el dispositivo no está accesible.")
    except Exception as e:
        raise ValueError(f"Ocurrió un error inesperado: {e}")
def muestra_puerto(interface,switch_ip,switch_user,switch_password):    
    # Datos de conexión al dispositivo
    device = {
        "device_type": "cisco_ios",  # Tipo de dispositivo (puede variar según el fabricante)
        "host": switch_ip,       # Dirección IP o hostname del dispositivo
        "username":switch_user,         # Usuario
        "password":switch_password,   # Contraseña
    }
    try:
        # Establecer conexión con el dispositivo
        connection = ConnectHandler(**device)
        # Ejecutar el comando y obtener la salida
        output = connection.send_command("show running-config interface gigabitEthernet "+interface)
        connection.disconnect()
        return output
    except NetmikoAuthenticationException:
        raise ValueError("Error de autenticación: verifica el usuario o la contraseña.")
    except NetmikoTimeoutException:
        raise ValueError("Error de conexión: el dispositivo no está accesible.")
    except Exception as e:
        raise ValueError(f"Ocurrió un error inesperado: {e}")
def configurar_puerto(vlan,puerto,descripcion,switch_ip,switch_user,switch_password): 
    # Datos de conexión al dispositivo
    device = {
        "device_type": "cisco_ios",  # Tipo de dispositivo (puede variar según el fabricante)
        "host": switch_ip,       # Dirección IP o hostname del dispositivo
        "username":switch_user,         # Usuario
        "password": switch_password,   # Contraseña
    }
    try:
        # Establecer conexión con el dispositivo
        connection = ConnectHandler(**device)
        # Enviar comandos al switch
        connection.send_config_set([
            "interface gigabitEthernet "+puerto,
            "description "+descripcion,
            "switchport access vlan "+vlan,
            "end"
        ]) 
        # Ejecutar el comando y obtener la salida
        connection.disconnect()
        return "Configuracion VLAN ejecutada con Exito.."
    except NetmikoAuthenticationException:
        raise ValueError("Error de autenticación: verifica el usuario o la contraseña.")
    except NetmikoTimeoutException:
        raise ValueError("Error de conexión: el dispositivo no está accesible.")
    except Exception as e:
        raise ValueError(f"Ocurrió un error inesperado: {e}") 
def guardar_configuracion(switch_ip,switch_user,switch_password):
     # Datos de conexión al dispositivo
    device = {
        "device_type": "cisco_ios",  # Tipo de dispositivo (puede variar según el fabricante)
        "host":switch_ip,       # Dirección IP o hostname del dispositivo
        "username":switch_user,         # Usuario
        "password":switch_password,   # Contraseña
    }
    try:
        # Establecer conexión con el dispositivo
        connection = ConnectHandler(**device)
        # Enviar el comando 'wr' y capturar la salida del log
        connection.send_config_set(["wr"]) 
        log_output = connection.send_command("show logging | include CONFIG_I")  # Buscar el mensaje en los logs
        last_log = log_output.strip().splitlines()[-1]  # Obtener solo la última línea de la salida
        #output = connection.send_command("wr")
        connection.disconnect()
        return f"{last_log}."
    except NetmikoAuthenticationException:
        raise ValueError("Error de autenticación: verifica el usuario o la contraseña.")
    except NetmikoTimeoutException:
        raise ValueError("Error de conexión: el dispositivo no está accesible.")
    except Exception as e:
        raise ValueError(f"Ocurrió un error inesperado: {e}")    