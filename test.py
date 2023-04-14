from flask import Flask, jsonify
import json
app = Flask(__name__)
@app.route('/machine-id', methods=['GET'])
def machine_id():
    machine_id = get_machine_id()
    return jsonify(machine_id)
def get_machine_id():
    with open('/etc/machine-id', 'r') as f:
        return {'machine_id': f.read().strip()}
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

