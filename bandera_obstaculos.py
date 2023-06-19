from flask import Flask, request, jsonify

app = Flask(__name__)

obstaculos = [0, 0, 0]  # Estado inicial de los obstáculos

@app.route('/obstaculos', methods=['GET'])
def obtener_estado_obstaculos():
    global obstaculos
    return jsonify(obstaculos)

@app.route('/obstaculos', methods=['POST'])
def cambiar_estado_obstaculos():
    global obstaculos
    nuevo_estado = request.json.get('estado')
    obstaculos = nuevo_estado
    return 'Estado de los obstáculos cambiado'

if __name__ == '__main__':
    app.run()
