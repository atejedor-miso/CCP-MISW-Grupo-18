# Microservicio de Inventario (inventory_service.py)
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
import eventlet

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Simulación del inventario
inventory = {"Producto A": 50, "Producto B": 30, "Producto C": 20}

@app.route('/inventario', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

@app.route('/actualizar', methods=['POST'])
def update_inventory():
    data = request.json
    producto = data.get('producto')
    cantidad = data.get('cantidad')

    if producto in inventory and inventory[producto] >= cantidad:
        inventory[producto] -= cantidad
        socketio.emit('inventario_actualizado', inventory)  # Notificación en tiempo real
        return jsonify({"message": "Inventario actualizado", "inventario": inventory})
    else:
        return jsonify({"error": "Stock insuficiente"}), 400

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)