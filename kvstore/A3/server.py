import argparse
import socket
import time
import selectors
import types
from typing import cast

sel = selectors.DefaultSelector()
HOST = "127.0.0.1"
PORT = 65432

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.setblocking(False)
sock.listen()
sel.register(sock, selectors.EVENT_READ, data=None)


def create_event_loop():
  try:
    while True:
      events = sel.select(timeout=None)
      print(f"Received events={len(events)}")
      for key, mask in events:
        if key.data is None:
          print(f"Accepting connection")
          accept_conn(key.fileobj)
        else:
          print(f"Serving request")
          service_request(key, mask)
  except KeyboardInterrupt:
    print("Closing event loop")
  finally:
    sock.close()
    sel.close()

def accept_conn(soc:socket.socket):
  conn, addr = sock.accept()
  print(f"Accepted connection from {addr}!")
  conn.setblocking(False)
  data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
  events = selectors.EVENT_READ | selectors.EVENT_WRITE
  sel.register(conn, events, data)

def service_request(key, mask):
  sock = cast(socket.socket, key.fileobj)
  data = cast(types.SimpleNamespace, key.data)
  if mask & selectors.EVENT_READ:
    recv_data = sock.recv(1024)
    if recv_data:
      data.outb += recv_data
    else:
      print("Connection to server from {data.addr} closed.")
      sel.unregister(sock)
      sock.close()
  if mask & selectors.EVENT_WRITE:
    if data.outb:
      print(f"Echoing {data.outb!r} to {data.addr}")
      sent = sock.send(data.outb)
      data.outb = data.outb[sent:]





def createTCPSocket(hostname, port):
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
    tcp_socket.bind((hostname, port))
    tcp_socket.listen(2)
    
    print(f"Waiting for connection")
    time.sleep(30)

    # conn, address = tcp_socket.accept()
    # with conn:
    #   print(f"Connected: {address}")
    #   conn.close()


def closeSocket(socket: socket):
  print("Closing socket")
  socket.close()


if __name__ == "__main__":
  # parser = argparse.ArgumentParser()
  # parser.add_argument("--port", type=int, default=5000)
  # parser.add_argument("--hostname", type=str, default="localhost")
  # args = parser.parse_args()

  # createTCPSocket(args.hostname, args.port)
  create_event_loop()