import tkinter as tk
import os
import subprocess
import requests

# Configuración del programa
server_url = 'http://localhost:5000'  # URL del servidor Flask
endpoint = '/obstaculos'               # Ruta del endpoint

# Realizar la solicitud POST para cambiar el estado de los obstáculos
def cambiar_estado_obstaculos(nuevo_estado):
    payload = {"estado": nuevo_estado}

    response = requests.post(server_url + endpoint, json=payload)

    if response.status_code == 200:
        print("Estado de los obstáculos cambiado con éxito")
    else:
        print("Error al cambiar el estado de los obstáculos")

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Simulación de Obstáculo")

# Funciones de clic para los botones
def clic_derecha():
    cambiar_estado_obstaculos([1,1,0])

def clic_cubierto():
    cambiar_estado_obstaculos([1,1,1])

def clic_centro():
    cambiar_estado_obstaculos([0,1,0])

def clic_izquierda():
    cambiar_estado_obstaculos([0,1,1])

def clic_libre():
    cambiar_estado_obstaculos([0,0,0])

# Botones para las posiciones del obstáculo
btn_derecha = tk.Button(ventana, text="Derecha", command=clic_derecha)
btn_derecha.pack()

btn_libre = tk.Button(ventana, text="Libre", command=clic_libre)
btn_libre.pack()

btn_centro = tk.Button(ventana, text="Centro", command=clic_centro)
btn_centro.pack()

btn_izquierda = tk.Button(ventana, text="Izquierda", command=clic_izquierda)
btn_izquierda.pack()

btn_cubierto = tk.Button(ventana, text="Cubierto Totalmente", command=clic_cubierto)
btn_cubierto.pack()

# Iniciar el bucle de la aplicación
ventana.mainloop()
