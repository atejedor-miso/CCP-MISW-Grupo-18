# Microservicio de Pedidos (order_service.py)
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

INVENTORY_SERVICE_URL = "http://localhost:5001/actualizar"

@app.route('/realizar-pedido', methods=['POST'])
def create_order():
    data = request.json
    producto = data.get('producto')
    cantidad = data.get('cantidad')

    response = requests.post(INVENTORY_SERVICE_URL, json={"producto": producto, "cantidad": cantidad})

    if response.status_code == 200:
        return jsonify({"message": "Pedido realizado exitosamente"})
    else:
        return jsonify({"error": "No se pudo procesar el pedido"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5002)