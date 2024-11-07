import os

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
