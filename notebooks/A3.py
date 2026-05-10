import marimo

__generated_with = "0.23.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What is a BUFFER ?
    A buffer is a temporary storage area that holds transient (inflight) data in memory.

    It is a chunk of contiguous memory that allows processes compesate for differences in processing speed.

    Using buffers, you can reduce slow operations and facilitate async comms between processes.
    """)
    return


@app.cell
def _():
    import sys
    import selectors
    import socket
    import types
    from typing import cast
    sel = selectors.DefaultSelector()

    HOST = "127.0.0.1"
    PORT = 64321
    return HOST, PORT, cast, sel, selectors, socket, types


@app.cell
def _(HOST, PORT, accept_wrapper, sel, selectors, service_connection, socket):
    def create_event_loop(host=HOST, port=PORT):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.bind((host, port))
            soc.listen()
            print(f"Listening on {(host, port)}")
            soc.setblocking(False)
            sel.register(soc, selectors.EVENT_READ, data=None)
            while True:
                events = sel.select(timeout=None)
                print(f"Received events with {len(events)}")
                for key, mask in events:
                    if key.data is None:
                        accept_wrapper(key.fileobj)
                    else:
                        service_connection(key, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting...")
        finally:
            soc.close()
            sel.close()

    return (create_event_loop,)


@app.cell
def _(sel, selectors, socket, types):
    def accept_wrapper(sock:socket.socket):
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

    return (accept_wrapper,)


@app.cell
def _(cast, sel, selectors, socket, types):
    def service_connection(key:selectors.SelectorKey , mask):
        sock = cast(socket.socket, key.fileobj)
        data = cast(types.SimpleNamespace, key.data)
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                data.outb += recv_data
            else:
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
                print(f"Echoing {data.outb!r} to {data.addr}")
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]

    return (service_connection,)


@app.cell
def _(create_event_loop):
    create_event_loop()
    return


@app.cell
def _(HOST, PORT, sel, selectors, socket, types):
    client_sele = selectors.DefaultSelector()

    messages = [b"Message 1 from client.", b"Message 2 from client."]

    def start_connections(host=HOST, port=PORT, num_connections=6):
        serv_addr = (host, port)

        for i in range(num_connections):
            connid = i + 1
            print(f"Starting connection {connid} to {serv_addr}")
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.setblocking(False)
            soc.connect_ex(serv_addr)

            events = selectors.EVENT_READ | selectors.EVENT_WRITE

            data = types.SimpleNamespace(
                connid=connid, 
                msg_total = sum(len(m) for m in messages),
                recv_total = 0,
                messages = messages.copy(),
                outb=b"",
            )

            sel.register(soc, events, data=data)


    return (start_connections,)


@app.cell
def _(cast, sel, selectors, socket, types):
    def service_client_connection(key:selectors.SelectorKey , mask):
        sock = cast(socket.socket, key.fileobj)
        data = cast(types.SimpleNamespace, key.data)
        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)
            if recv_data:
                print(f"Received {recv_data!r} from connection {data.connid}")
                data.recv_total += len(recv_data)
            if not recv_data or data.recv_total == data.msg_total:
                print(f"Closing connection to {data.connid}")
                sel.unregister(sock)
                sock.close()
        if mask & selectors.EVENT_WRITE:
            if not data.outb and data.messages:
                data.outb = data.messages.pop(0)
            if data.outb:
                print(f"Sending {data.outb!r} to connection {data.connid}")
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]

    return (service_client_connection,)


@app.cell
def _(service_client_connection, start_connections):
    start_connections()
    service_client_connection()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
