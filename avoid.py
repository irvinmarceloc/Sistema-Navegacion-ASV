from dronekit import connect, VehicleMode, LocationGlobal
import time
from math import sin, cos, sqrt, atan2, radians
import requests


# Conectar al vehículo
vehicle = connect('tcp:127.0.0.1:5763', wait_ready=True)

# Cambiar al modo GUIDED
vehicle.mode = VehicleMode("GUIDED")

#Orientar vehículo de acuerdo a obstaculos, 
def orientar(vehicle, obstaculo):
    a = vehicle.heading
    b = a
    if obstaculo[1]:
        if obstaculo[2]:
            b = a - 90
        if obstaculo[0]:
            b = a + 90
    return b 

#Genera coordenada a 10 metros a 90 o -90 grados con respecto al ángulo de avance
def generar_coordenadas(a, vehicle):
    distance = 10
    angle_rad = radians(a)
    lat_base = vehicle.location.global_frame.lat
    lon_base = vehicle.location.global_frame.lon
    return lat_base + (distance * cos(angle_rad))  , lon_base + (distance * sin(angle_rad)) 

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
    LocationGlobal(-25.313745, -57.297215, 0),
    LocationGlobal(-25.314205, -57.299401),
    LocationGlobal(-25.315291, -57.297706),
    LocationGlobal(-25.314651, -57.297052),
    LocationGlobal(-25.313745, -57.297215, 0)  # Punto de inicio
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
while waypoint_index <= len(waypoints):
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
        if obstaculo[1]:
            print("Detectado obstáculo. Preparando maniobra evasiva...")
            #Definir de acuerdo a si hay obstaculos ademas de en el centro a la izquierda o derecha
            lat_dest, lon_dest = generar_coordenadas(orientar(vehicle, obstaculo), vehicle)
            # Crear el objeto LocationGlobalRelative para el simple_goto
            target_location = LocationGlobal(lat_dest, lon_dest, 0)
            # Realizar el simple_goto al punto auxiliar de destino
            vehicle.airspeed = 0.5
            vehicle.simple_goto(target_location)
        #Contador de maniobras evasibas fallidas 
            num_man_evas += 1
        if obstaculo_anterior and not obstaculo[1]:
            vehicle.airspeed = 2
            vehicle.simple_goto(waypoint)
        obstaculo_anterior = obstaculo[1]
        # Esperar un tiempo antes de realizar la siguiente verificación
        time.sleep(1)
    waypoint_index += 1


# Cambiar al modo RTL (Return to Launch)
vehicle.mode = VehicleMode("RTL")

# Cerrar la conexión
vehicle.close()

