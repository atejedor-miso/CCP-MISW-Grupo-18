# Microservicio de Notificaciones (notification_service.py)
from flask import Flask, jsonify, request
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/notificar', methods=['POST'])
def send_notification():
    data = request.json
    socketio.emit('notificacion', data)  # Envía notificación a los clientes conectados
    return jsonify({"message": "Notificación enviada"})

@socketio.on('connect')
def handle_connect():
    print("Cliente conectado a notificaciones")

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5003)