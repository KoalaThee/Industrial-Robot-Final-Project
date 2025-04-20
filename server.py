import socket
import ast


class Server:
    HOST: str = socket.gethostbyname(socket.gethostname())
    PORT: int = 2024
    _server: socket.socket
    finished = False

    def __init__(self, host: str = None, port: int = None) -> None:
        self.HOST = host or self.HOST
        self.PORT = port or self.PORT
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.HOST, self.PORT))

    def listen(self, func: callable) -> None:
        self._server.listen()
        print(f"[Server] Server listening at {self.HOST}:{self.PORT}")
        while True:
            conn, addr = self._server.accept()
            with conn:
                print(f"[Server] Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    if not self.finished:
                        self.finished = func(data.decode("UTF-8"))
                        if (self.finished == 0):
                            break 
                print(f"[Server] Disconnected by {addr}")
            break
    def close_server(self):
        self._server.close()

if __name__ == "__main__":
    s = Server(port=2024)

    @s.listen
    def handle_message(msg: str):

        # processed_msg = ast.literal_eval(msg)
        print("msg",msg)
        if msg[0] == "[" and msg[-1] == "]":
            processed_msg = [ elm if elm != "" else "None" for elm in msg[1:-1].split(",")]
            # print(processed_msg)
            processed_msg[0] = processed_msg[0] == 'True'
            processed_msg[3] = processed_msg[3] == 'True'
            # print(processed_msg)
            if processed_msg[0]:
                processed_msg[1] = int(processed_msg[1])
                processed_msg[2] = int(processed_msg[2])
            if processed_msg[3]:
                if int(processed_msg[-1]) > 180:
                    processed_msg[-1] = int(processed_msg[-1]) - 360
                else:
                    processed_msg[-1] = int(processed_msg[-1])
            print("processes",processed_msg)
