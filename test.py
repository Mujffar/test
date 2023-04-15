from flask import Flask
import subprocess
import os
import json
import psutil
import socket

app = Flask(__name__)

@app.route('/')
def get_machine_id():
    with open('/etc/machine-id', 'r') as f:
        return {'machine_id': f.read().strip()}

machine_id_json = json.dumps(get_machine_id())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
