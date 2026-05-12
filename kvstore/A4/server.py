import argparse
import socket
import time

HOST = "127.0.0.1"
PORT = 65432


buffer = b""
def createTCPSocket(hostname, port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
    tcp_socket.bind((hostname, port))
    tcp_socket.listen(2)
    
    print(f"Waiting for connection")

    conn, address = tcp_socket.accept()
    with True:
      msg = recv_line(conn)
      print(f"Connected: {address}")
      print(f"Received message {msg}")

def recv_line(soc: socket.socket):
  stop = False
  while not stop:
    buffer += soc.recv(1024)
    temp_bytes = b""
    for char in buffer:
      if char == "\n":
        stop = True
        break
      else:
        temp_bytes += char
    buffer = buffer[len(temp_bytes)+2:]
  return temp_bytes


def closeSocket(socket: socket):
  print("Closing socket")
  socket.close()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--port", type=int, default=5000)
  parser.add_argument("--hostname", type=str, default="localhost")
  args = parser.parse_args()

  createTCPSocket(args.hostname, args.port)