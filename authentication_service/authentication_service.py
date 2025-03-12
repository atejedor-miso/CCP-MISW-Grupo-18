from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__)

# Usuario mock
MOCK_USER = {
    "username": "user1",
    "password": "password123"
}

SECRET_KEY = "mysecretkey"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if data["username"] == MOCK_USER["username"] and data["password"] == MOCK_USER["password"]:
        token = jwt.encode({
            "username": MOCK_USER["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")
        
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/verify_token", methods=["POST"])
def verify_token():
    data = request.get_json()
    token = data.get("token")
    
    if not token:
        return jsonify({"error": "Token is required"}), 400

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"valid": True, "username": decoded["username"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5004)
