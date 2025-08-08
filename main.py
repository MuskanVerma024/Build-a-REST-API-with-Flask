from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory user store (for demonstration)
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}

# Home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the User API!"})

# GET: Get all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

# GET: Get a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# POST: Add a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and Email are required"}), 400
    user_id = max(users.keys(), default=0) + 1
    users[user_id] = {"name": data["name"], "email": data["email"]}
    return jsonify({"message": "User created", "user": users[user_id]}), 201

# PUT: Update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    return jsonify({"message": "User updated", "user": user})

# DELETE: Delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        deleted = users.pop(user_id)
        return jsonify({"message": "User deleted", "user": deleted})
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
