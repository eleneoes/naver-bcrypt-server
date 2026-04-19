from flask import Flask, request, jsonify
import bcrypt
import time
import base64
import urllib.request

app = Flask(__name__)

@app.route('/ip', methods=['GET'])
def get_ip():
    ip = urllib.request.urlopen('https://ifconfig.me').read().decode('utf-8')
    return jsonify({'ip': ip})

@app.route('/', methods=['GET', 'POST'])
def generate_sign():
    if request.method == 'GET':
        return 'OK', 200
    data = request.get_json()
    client_id = data['clientId']
    client_secret = data['clientSecret'].encode('utf-8')
    timestamp = str(int(time.time() * 1000))
    password = (client_id + '_' + timestamp).encode('utf-8')
    hashed = bcrypt.hashpw(password, client_secret)
    sign = base64.b64encode(hashed).decode('utf-8')
    return jsonify({'timestamp': timestamp, 'client_secret_sign': sign})

if __name__ == '__main__':
    app.run()
