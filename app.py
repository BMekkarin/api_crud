from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Load data from JSON file
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as json_file:
            return json.load(json_file)
    return []

# Save data to JSON file
def save_data(data):
    with open('data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

@app.route('/items', methods=['GET'])
def get_items():
    data = load_data()
    return jsonify(data)

@app.route('/item/<int:item_id>', methods=['GET'])
def get_item(item_id):
    data = load_data()
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({'message': 'Item not found'}), 404

@app.route('/item', methods=['POST'])
def add_item():
    data = load_data()
    new_item = request.get_json()
    new_item['id'] = len(data) + 1
    data.append(new_item)
    save_data(data)
    return jsonify(new_item), 201

@app.route('/item/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = load_data()
    update_data = request.get_json()
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        item.update(update_data)
        save_data(data)
        return jsonify(item)
    return jsonify({'message': 'Item not found'}), 404

@app.route('/item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    data = load_data()
    item = next((item for item in data if item['id'] == item_id), None)
    if item:
        data.remove(item)
        save_data(data)
        return jsonify({'message': 'Item deleted successfully'})
    return jsonify({'message': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
 