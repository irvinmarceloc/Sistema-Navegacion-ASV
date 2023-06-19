from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from math import sin, cos, sqrt, atan2, radians
import requests
import random

# Conectar al vehículo
vehicle = connect('tcp:127.0.0.1:5763', wait_ready=True)

# Cambiar al modo GUIDED
vehicle.mode = VehicleMode("GUIDED")

#Orientar vehículo de acuerdo a obstaculos, 
#Orientar vehículo de acuerdo a obstaculos, 
def orientar(obstaculos, vehicle):
    #Todos los estados estan permitidos
    permitir_oeste=1
    permitir_sur=1
    permitir_norte=1 
    permitir_este=1
    # Obtener la orientación del vehículo en grados
    orientacion_grados = vehicle.heading
    # Calcular la orientación de la derecha sumando 90 grados y asegurando que esté dentro del rango 0-360 grados
    orientacion_derecha_grados = (orientacion_grados + 90) % 360
    # Determinar el punto cardinal correspondiente a la orientación actual
    if orientacion_grados >= 337.5 or orientacion_grados < 22.5:
        punto_cardinal_actual = "Norte"
    elif orientacion_grados >= 22.5 and orientacion_grados < 67.5:
        punto_cardinal_actual = "Noreste"
    elif orientacion_grados >= 67.5 and orientacion_grados < 112.5:
        punto_cardinal_actual = "Este"
    elif orientacion_grados >= 112.5 and orientacion_grados < 157.5:
        punto_cardinal_actual = "Sureste"
    elif orientacion_grados >= 157.5 and orientacion_grados < 202.5:
        punto_cardinal_actual = "Sur"
    elif orientacion_grados >= 202.5 and orientacion_grados < 247.5:
        punto_cardinal_actual = "Suroeste"
    elif orientacion_grados >= 247.5 and orientacion_grados < 292.5:
        punto_cardinal_actual = "Oeste"
    else:
        punto_cardinal_actual = "Noroeste"
    # Determinar el punto cardinal correspondiente a la orientación hacia la derecha
    if orientacion_derecha_grados >= 337.5 or orientacion_derecha_grados < 22.5:
        punto_cardinal_derecha = "Norte"
    elif orientacion_derecha_grados >= 22.5 and orientacion_derecha_grados < 67.5:
        punto_cardinal_derecha = "Noreste"
    elif orientacion_derecha_grados >= 67.5 and orientacion_derecha_grados < 112.5:
        punto_cardinal_derecha = "Este"
    elif orientacion_derecha_grados >= 112.5 and orientacion_derecha_grados < 157.5:
        punto_cardinal_derecha = "Sureste"
    elif orientacion_derecha_grados >= 157.5 and orientacion_derecha_grados < 202.5:
        punto_cardinal_derecha = "Sur"
    elif orientacion_derecha_grados >= 202.5 and orientacion_derecha_grados < 247.5:
        punto_cardinal_derecha = "Suroeste"
    elif orientacion_derecha_grados >= 247.5 and orientacion_derecha_grados < 292.5:
        punto_cardinal_derecha = "Oeste"
    else:
        punto_cardinal_derecha = "Noroeste"

    #Determinar si permitir_oeste, permitir_sur, permitir_norte, permitir_este de acuerdo a la orientación del vehículo y sus obstaculos
    #Solo hay obstaculos en el centro, entonces el punto aleatorio para seguir navegando no se genera en dirección de avance del vehículo
    if not obstaculos[0] and  not obstaculos[2]:
        if punto_cardinal_actual=="Norte":
            permitir_norte=0
        if punto_cardinal_actual=="Noreste":
            permitir_norte=0
            permitir_este=0
        if punto_cardinal_actual=="Este":
            permitir_este=0
        if punto_cardinal_actual=="Sureste":
            permitir_este=0
            permitir_sur=0
        if punto_cardinal_actual=="Sur":
            permitir_sur=0
        if punto_cardinal_actual=="Suroeste":
            permitir_oeste=0
            permitir_sur=0
        if punto_cardinal_actual=="Oeste":
            permitir_oeste=0
        if punto_cardinal_actual=="Noroeste":
            permitir_norte=0
            permitir_oeste=0
    #Cuando hay obstaculos solo en la derecha
    elif obstaculos[0] and  not obstaculos[2]:
        #No avanzar al frente
        if punto_cardinal_actual=="Norte":
            permitir_norte=0
        if punto_cardinal_actual=="Noreste":
            permitir_norte=0
            permitir_este=0
        if punto_cardinal_actual=="Este":
            permitir_este=0
        if punto_cardinal_actual=="Sureste":
            permitir_este=0
            permitir_sur=0
        if punto_cardinal_actual=="Sur":
            permitir_sur=0
        if punto_cardinal_actual=="Suroeste":
            permitir_oeste=0
            permitir_sur=0
        if punto_cardinal_actual=="Oeste":
            permitir_oeste=0
            permitir_norte=0
        if punto_cardinal_actual=="Noroeste":
            permitir_norte=0
            permitir_oeste=0
        #No avanzar a la derecha
        if punto_cardinal_derecha=="Norte":
            permitir_norte=0
        if punto_cardinal_derecha=="Noreste":
            permitir_norte=0
            permitir_este=0
        if punto_cardinal_derecha=="Este":
            permitir_este=0
        if punto_cardinal_derecha=="Sureste":
            permitir_este=0
            permitir_sur=0
        if punto_cardinal_derecha=="Sur":
            permitir_sur=0
        if punto_cardinal_derecha=="Suroeste":
            permitir_oeste=0
            permitir_sur=0
        if punto_cardinal_derecha=="Oeste":
            permitir_oeste=0
        if punto_cardinal_derecha=="Noroeste":
            permitir_norte=0
            permitir_oeste=0
    #Cuando hay obstaculos solo en la izquierda
    elif not obstaculos[0] and  obstaculos[2]:
        #No avanzar al frente
        if punto_cardinal_actual=="Norte":
            permitir_norte=0
        if punto_cardinal_actual=="Noreste":
            permitir_norte=0
            permitir_este=0
        if punto_cardinal_actual=="Este":
            permitir_este=0
        if punto_cardinal_actual=="Sureste":
            permitir_este=0
            permitir_sur=0
        if punto_cardinal_actual=="Sur":
            permitir_sur=0
        if punto_cardinal_actual=="Suroeste":
            permitir_oeste=0
            permitir_sur=0
        if punto_cardinal_actual=="Oeste":
            permitir_oeste=0
        if punto_cardinal_actual=="Noroeste":
            permitir_norte=0
            permitir_oeste=0
        #No avanzar a la derecha
        if punto_cardinal_derecha=="Norte":
            permitir_sur=0
        if punto_cardinal_derecha=="Noreste":
            permitir_sur=0
            permitir_oeste=0
        if punto_cardinal_derecha=="Este":
            permitir_oeste=0
        if punto_cardinal_derecha=="Sureste":
            permitir_oeste=0
            permitir_norte=0
        if punto_cardinal_derecha=="Sur":
            permitir_norte=0
        if punto_cardinal_derecha=="Suroeste":
            permitir_este=0
            permitir_norte=0
        if punto_cardinal_derecha=="Oeste":
            permitir_este=0
        if punto_cardinal_derecha=="Noroeste":
            permitir_sur=0
            permitir_este=0
    #Cuando hay obstaculos en todo el frente    
    elif obstaculos[0] and  obstaculos[2]:
        if punto_cardinal_actual=="Norte":
            permitir_oeste=0
            permitir_norte=0
            permitir_este=0
        if punto_cardinal_actual=="Noreste":
            permitir_norte=0 
            permitir_este=0
        if punto_cardinal_actual=="Este":
            permitir_sur=0
            permitir_norte=0 
            permitir_este=0
        if punto_cardinal_actual=="Sureste":
            permitir_sur=0
            permitir_este=0
        if punto_cardinal_actual=="Sur":
            permitir_oeste=0
            permitir_sur=0
            permitir_este=0
        if punto_cardinal_actual=="Suroeste":
            permitir_oeste=0
            permitir_sur=0
        if punto_cardinal_actual=="Oeste":
            permitir_oeste=0
            permitir_sur=0
            permitir_norte=0 
        if punto_cardinal_actual=="Noroeste":
            permitir_oeste=0
            permitir_norte=0

    return permitir_oeste, permitir_sur, permitir_norte, permitir_este

#Genera coordenada aleatoria a no mas de 10 metros de un punto inicial en la dirección indicada
def generar_coordenadas_aleatorias(latitud_base, longitud_base, permitir_oeste, permitir_sur, permitir_norte, permitir_este):
    direcciones_posibles = []
    
    if permitir_oeste:
        direcciones_posibles.append("oeste")
    if permitir_sur:
        direcciones_posibles.append("sur")
    if permitir_norte:
        direcciones_posibles.append("norte")
    if permitir_este:
        direcciones_posibles.append("este")

    direccion = random.choice(direcciones_posibles)
    #Por lo menos girar el vehículo
    latitud, longitud = latitud_base, longitud_base

    if direccion == "oeste":
        longitud = round(random.uniform(longitud_base - 0.0002 - 0.0001, longitud_base - 0.0001), 6)
    elif direccion == "sur":
        latitud = round(random.uniform(latitud_base - 0.0002 - 0.0001, latitud_base - 0.0001), 6)
    elif direccion == "norte":
        latitud = round(random.uniform(latitud_base + 0.0001, latitud_base + 0.0002), 6)
    elif direccion == "este":
        longitud = round(random.uniform(longitud_base + 0.0001, longitud_base + 0.0002), 6)
    
    return latitud, longitud

# Función para obtener el estado actual de los obstáculos desde el servidor Flask
def obtener_estado_obstaculos():
    response = requests.get('http://localhost:5000/obstaculos')
    obstaculos = response.json()
    resp = obstaculos
    if obstaculos[0] == "0":
        resp[0] = 1
    if obstaculos[1] == "0":
        resp[1] = 1
    if obstaculos[2] == "0":
        resp[2] = 1
    return resp
    
def calcular_distancia(coord1, coord2):
    # Coordenadas en formato (latitud, longitud)
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Radio de la Tierra en metros
    r = 6371000

    # Convertir las coordenadas a radianes
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Diferencia de latitud y longitud
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # Distancia entre los dos puntos en metros
    distancia = r * c

    return distancia

# Definir los puntos de navegación
waypoints = [
    LocationGlobalRelative(-25.313745, -57.297215, 0),
    LocationGlobalRelative(-25.313810, -57.298706),
    LocationGlobalRelative(-25.314205, -57.299401),
    LocationGlobalRelative(-25.315291, -57.297706),
    LocationGlobalRelative(-25.314651, -57.297052),
    LocationGlobalRelative(-25.313745, -57.297215, 0)  # Punto de inicio
]
logrados = []
no_logrados = [] 
# Armar el vehículo si no está armado
if not vehicle.armed:
    vehicle.armed = True
    time.sleep(1)

# Obtener la altitud de inicio
altitud_inicio = vehicle.location.global_relative_frame.alt
# Navegar a cada punto de forma secuencial
waypoint_index = 0
obstaculo = False

print("Iniciando navegación...")
while waypoint_index < len(waypoints):
    waypoint = waypoints[0]
    waypoint.alt = altitud_inicio  # Establecer la altitud del waypoint igual a la altitud de inicio
    vehicle.simple_goto(waypoint)
    print(f"Navegando hacia el punto {waypoint_index + 1}...")
    obstaculo = [False,False,False]
    obstaculo_anterior = False
    # Numero de intentos de evadir un obstaculos
    num_man_evas = 0
    # Esperar hasta que se alcance el punto o se reciba un obstáculo
    while True:
        remaining_distance = calcular_distancia(
            (vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon),
            (waypoint.lat, waypoint.lon)
        )

        if remaining_distance <= 1:  # Puedes ajustar esta distancia según tu precisión requerida
            print(f"Llegado al punto {waypoint_index + 1}")
            logrados.append(waypoints[0])
            waypoints.append(waypoints.pop(0))
            break
        if  num_man_evas > 20:
            print(f"Me rindo, no se pudo llegar al punto {waypoint_index + 1}")
            no_logrados.append(waypoints[0])
            waypoints.append(waypoints.pop(0))
            break
        # Comprobar si se ha detectado un obstáculo
        obstaculo = obtener_estado_obstaculos()
        print(str(obstaculo[1]))
        if obstaculo[1]:
            print("Detectado obstáculo. Preparando maniobra evasiva...")
            # Obtener las coordenadas globales (latitud y longitud) del vehículo
            lat_base = vehicle.location.global_frame.lat
            lon_base = vehicle.location.global_frame.lon
            #Definir de acuerdo a si hay obstaculos ademas de en el centro a la izquierda o derecha
            permitir_oeste, permitir_sur, permitir_norte, permitir_este = orientar(obstaculo,vehicle)
            lat_dest, lon_dest = generar_coordenadas_aleatorias(lat_base, lon_base, permitir_oeste, permitir_sur, permitir_norte, permitir_este)
            # Crear el objeto LocationGlobalRelative para el simple_goto
            target_location = LocationGlobalRelative(lat_dest, lon_dest, 0)
            # Realizar el simple_goto al punto de destino
            vehicle.simple_goto(target_location)
            num_man_evas += 1
        if obstaculo_anterior and not obstaculo[1]:
            vehicle.simple_goto(waypoint)
        obstaculo_anterior = obstaculo[1]
        # Esperar un tiempo antes de realizar la siguiente verificación
        time.sleep(1)

    waypoint_index += 1


# Cambiar al modo RTL (Return to Launch)
vehicle.mode = VehicleMode("RTL")

# Esperar hasta que el vehículo aterrice
while vehicle.mode.name != 'LAND':
    time.sleep(1)

# Desarmar el vehículo si estaba armado al inicio
if vehicle.armed:
    vehicle.armed = False

# Cerrar la conexión
vehicle.close()

