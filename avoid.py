from dronekit import connect, VehicleMode, LocationGlobal
import time
from math import radians, cos, sin, degrees, atan2, sqrt
import requests
import os

# Conectar al vehículo
vehicle = connect('tcp:127.0.0.1:5763', wait_ready=True)

# Cambiar al modo GUIDED
vehicle.mode = VehicleMode("GUIDED")

#Orientar vehículo de acuerdo a obstaculos, 
def orientar(vehicle, obstaculo):
    a = vehicle.heading
    b = a
    
    casos = {
        (True, True, False): a - 90,
        (False, True, True): a + 90,
        (True, True, True): a + 90,
        (False, True, False): a + 90,
    }
    
    if tuple(obstaculo) in casos:
        b = casos[tuple(obstaculo)]
        
    return b 

#Genera coordenada a 10 metros a 90 o -90 grados con respecto al ángulo de avance
def generar_coordenadas(a, vehicle):
    distance_meters = 10  # Distancia en metros
    lat_base = vehicle.location.global_frame.lat
    lon_base = vehicle.location.global_frame.lon

    # Convertir distancia en metros a diferencia en grados decimales
    lat_correction = (distance_meters / 111111) * cos(radians(lat_base))
    lon_correction = (distance_meters / (111111 * cos(radians(lat_base))))

    # Convertir ángulo a radianes
    angle_rad = radians(a)

    # Calcular las nuevas coordenadas
    lat_nueva = lat_base + degrees(lat_correction)
    lon_nueva = lon_base + degrees(lon_correction / cos(radians(lat_base))) / sin(atan2(1, 1) * 4 + angle_rad)

    return lat_nueva, lon_nueva


# Función para obtener el estado actual de los obstáculos desde el servidor Flask
def obtener_estado_obstaculos():
    response = requests.get('http://localhost:5000/obstaculos')
    obstaculos = response.json()

    resp = [int(obstaculo) for obstaculo in obstaculos]

    return resp
    
def calcular_distancia(coord1, coord2):
    # Coordenadas en formato (latitud, longitud)
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Radio de la Tierra en metros
    r = 6371000.0

    # Convertir las coordenadas a radianes
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

    # Diferencia de latitud y longitud
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    # Distancia entre los dos puntos en metros
    distancia = r * c

    return distancia

# Definir la clase LocationGlobal
# Definir la clase LocationGlobal
class LocationGlobal:
    def __init__(self, lat, lon, alt=None):
        self.lat = lat
        self.lon = lon
        # Si alt es None, significa que es solo latitud y longitud (sin altitud)
        self.alt = alt if alt is not None else None

    def __repr__(self):
        # Mostrar la altitud solo si no es None
        if self.alt is None:
            return f"LocationGlobal({self.lat}, {self.lon})"
        else:
            return f"LocationGlobal({self.lat}, {self.lon}, {self.alt})"


def procesar_coordenadas(path):
    # Inicializamos una lista para almacenar las coordenadas formateadas
    waypoints = []

    # Verificamos si el archivo existe en la ruta especificada
    if os.path.exists(path):
        with open(path, 'r') as file:
            for index, line in enumerate(file):
                # Remover comentarios y espacios en blanco
                line = line.split("#")[0].strip()

                # Eliminar comas adicionales al final de la línea
                line = line.rstrip(',')  # Eliminar cualquier coma al final

                # Saltar líneas vacías
                if not line:
                    continue

                try:
                    # Convertir la línea en una lista de coordenadas numéricas
                    coords = list(map(float, line.split(',')))

                    # Solo para el primer punto, agregar un valor de altitud si falta
                    if index == 0 and len(coords) == 2:
                        coords.append(0)  # Agregar altitud 0 al primer punto

                    # Crear una instancia de LocationGlobal con las coordenadas procesadas
                    # Si el punto tiene 2 valores, significa latitud y longitud, sin altitud
                    if len(coords) == 2:
                        location = LocationGlobal(coords[0], coords[1])
                    elif len(coords) == 3:
                        # Si ya tiene 3 valores, latitud, longitud y altitud
                        location = LocationGlobal(coords[0], coords[1], coords[2])

                    waypoints.append(location)

                except ValueError as e:
                    print(f"Error al procesar la línea {index + 1}: '{line}' - {e}")

        return waypoints
    else:
        return "El archivo no se encuentra en la ruta especificada."


# Uso del código:
# Suponiendo que tienes el archivo con las coordenadas en el escritorio
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "coordenadas.txt")
waypoints = procesar_coordenadas(desktop_path)


# Imprimir el resultado
for wp in waypoints:
    print(wp)


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

