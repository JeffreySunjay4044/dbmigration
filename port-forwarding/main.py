import os
import psycopg2
from flask import Flask, request
from sshtunnel import SSHTunnelForwarder

app = Flask(__name__)

@app.route('/scheduler/backupdelete', methods=['GET', 'POST'])
def route_traffic():
    backup_json = request.get_json(silent=True)
    print(backup_json)
    route_traffic_to_remote(backup_json)


def route_traffic_to_remote(payload):
    try:
        with SSHTunnelForwarder(
             (os.environ.get("host_path"), 22),
             ssh_private_key=os.environ.get("ssh_private_key"),
             ### in my case, I used a password instead of a private key
             ssh_username=os.environ.get("ssh_username"),
             ssh_password=os.environ.get("ssh_password"),
             remote_bind_address=(os.environ.get("remote_bind_address"), 5439)) as server:
             server.start()
             print ("server connected")
             params = {
                 'database': os.environ.get("database"),
                 'user': os.environ.get("user"),
                 'password': os.environ.get("password"),
                 'host': os.environ.get("host"),
                 'port': server.local_bind_port
                 }
             conn = psycopg2.connect(**params)
             cursor = conn.cursor()
             cursor.execute(payload)
             print ("database connected")
    except:
        print ("Connection Failed")

if __name__ == '__main__':
    app.run(debug=True)