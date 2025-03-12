from flask import Flask, Response, request, redirect, jsonify
import requests

app = Flask(__name__)


MICROSERVICES = {
    'inventory': 'http://localhost:5001',
    'order': 'http://localhost:5002',
    'notification': 'http://localhost:5003'
}

AUTH_SERVICE_URL = 'http://localhost:5004/verify_token'
LOGIN_SERVICE_URL = 'http://localhost:5004/login'

@app.before_request
def handle_request():
    if request.path == "/login" and request.method == "POST":
        response = requests.post(LOGIN_SERVICE_URL, json=request.get_json())
        return Response(response.text, status=response.status_code, content_type=response.headers['Content-Type'])
    
    if request.path.startswith(('/inventory', '/notification', '/order')):
        token = request.headers.get("Authorization")
        
        if not token:
            return jsonify({"error": "Authorization token is missing"}), 403
        
        token = token.split(" ")[1] if token.startswith("Bearer ") else token
        
        response = requests.post(AUTH_SERVICE_URL, json={"token": token})
        
        if response.status_code != 200:
            return jsonify({"error": "Invalid or expired token"}), 403

    service_name = request.path.strip('/').split('/')[0]
    
    if service_name in MICROSERVICES:
        target_url = MICROSERVICES[service_name] + request.full_path[len('/' + service_name):]
        # Imprimir para depuración
        print(f"Redirigiendo a {target_url}")
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=request.headers,
            data=request.get_data(),
            cookies=request.cookies
        )
        return Response(response.text, status=response.status_code, content_type=response.headers['Content-Type'])
    
    return jsonify({"error": "Microservice not found"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)