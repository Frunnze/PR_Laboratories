from flask import jsonify, request
from flasgger import swag_from

from __main__ import app, crud
from models.electro_scooter import ElectroScooter


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['DELETE'])
@swag_from("ymls/electro_scooter_delete.yml")
def delete_electro_scooter(scooter_id):
    headers = dict(request.headers)
    if not crud.leader and ("Token" not in headers or headers["Token"] != "leader"):
        return jsonify({"message" : "Access denied!"}), 403
    else:
        # Find the Electro Scooter by ID
        scooter = ElectroScooter.query.get(scooter_id)
        if scooter is not None:
            # Get the password from the request headers
            password = request.headers.get('X-Delete-Password')
            # Check if the provided password is correct
            if password == 'your_secret_password': # Replace with your actual password
                crud.delete(scooter_id, scooter, password)
                return jsonify({"message": "Electro Scooter deleted successfully"}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "Electro Scooter not found"}), 404


@app.route('/api/electro-scooters/<int:scooter_id>', methods=['PUT'])
@swag_from("ymls/electro_scooter_put.yml")
def update_electro_scooter(scooter_id):
    headers = dict(request.headers)
    if not crud.leader and ("Token" not in headers or headers["Token"] != "leader"):
        return jsonify({"message" : "Access denied!"}), 403
    else:
        # Find the Electro Scooter by ID
        scooter = ElectroScooter.query.get(scooter_id)
        if scooter is not None:
            crud.update(scooter_id, scooter, request.get_json())
            return jsonify({"message": "Electro Scooter updated successfully"}), 200
        else:
            return jsonify({"error": "Electro Scooter not found"}), 404
    
        
@app.route('/api/electro-scooters', methods=['POST'])
@swag_from("ymls/electro_scooter_post.yml")
def create_electro_scooter():
    headers = dict(request.headers)
    if not crud.leader and ("Token" not in headers or headers["Token"] != "leader"):
        return jsonify({"message" : "Access denied!"}), 403
    else:
        crud.create(request.get_json())
        return jsonify({"message": "Electro Scooter created successfully"}), 201
    

@app.route('/api/electro-scooters/<int:scooter_id>', methods=['GET'])
@swag_from("ymls/electro_scooter_get.yml")
def get_electro_scooter_by_id(scooter_id):
    # Find the Electro Scooter by ID
    scooter = ElectroScooter.query.get(scooter_id)
    if scooter is not None:
        return jsonify({
            "id": scooter.id,
            "name": scooter.name,
            "battery_level": scooter.battery_level
        }), 200
    else:
        return jsonify({"error": "Electro Scooter not found"}), 404 