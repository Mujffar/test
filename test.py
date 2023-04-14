from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def get_machine_id():
    with open('/etc/machine-id', 'r') as f:
        machine_id = f.read().strip()
    return json.dumps({'machine_id': machine_id})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
