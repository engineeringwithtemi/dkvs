import marimo

__generated_with = "0.23.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # A2 — Listening and Accepting Connections: Observations

    Server-side code lives in `../kvstore/server.py`. This notebook is for connecting clients and observing what happens.

    **BUILD (from curriculum):** Extend A1 with `listen(backlog=5)` and `accept()`. Print the client address when a connection arrives. Test by connecting from a separate process.

    **Workflow:** start your server in a terminal (`python kvstore/server.py`), then run cells here to connect to it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Single client connection

    Expected: the server prints the client's address (something like `('127.0.0.1', 54321)`). Note the client port is ephemeral — the kernel picked it for you because you didn't `bind()` on the client side.
    """)
    return


@app.cell
def _():
    import socket
    PORT, HOSTNAME = (5001, 'localhost')

    def socketClient(hostname: str, port: int):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((hostname, port))
        print('Connected to socket: ', tcp_socket.getsockname())
    socketClient(HOSTNAME, PORT)
    return HOSTNAME, PORT, socket, socketClient


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Rapid multiple clients

    Open 3 client connections in quick succession. The server, looping on `accept()`, dequeues them one at a time. The kernel holds any that arrive while the server is busy elsewhere — that's the **backlog queue**.

    Expected: all 3 connect successfully and the server logs three addresses. Note the client ports — each is different (different ephemeral port per process/socket).
    """)
    return


@app.cell
def _(HOSTNAME, PORT, socketClient):
    for _i in range(3):
        socketClient(HOSTNAME, PORT)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Overflow the backlog (optional)

    To see what happens when the backlog fills up, modify your server to *not* call `accept()` (or sleep before calling it). Then try to open more than `backlog` connections from here.

    Expected behavior is OS-dependent: on macOS/Linux, additional connections may be silently dropped or refused once the queue is full. The exact symptom varies. Note what you actually observe.
    """)
    return


@app.cell
def _(HOSTNAME, PORT, socket, socketClient):
    import time
    clients = []
    for _i in range(5):
        try:
            s = socketClient(HOSTNAME, PORT)
            clients.append(s)
        except (socket.timeout, ConnectionRefusedError) as e:
            print(f'client {_i}: failed - {type(e).__name__}')
        time.sleep(0.1)
    return


if __name__ == "__main__":
    app.run()
