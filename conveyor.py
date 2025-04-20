import socket
import time
# "10.10.0.98"
c_ip = "0.0.0.0"
c_port = 2002

class Conveyor:
    client = socket.socket()
    def __init__(self, ip, port):
        self.port = port 
        self.ip = ip
        self.server = None
        self.client = None

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        self.server = s
        s.listen(1)
        #print(f"Server listening at {self.ip}:{self.port}")
        c, addr = s.accept()
        self.client = c
        print(f"[Conveyor] Connected by {addr}")
        c.sendall(b"activate,tcp\n")
        time.sleep(1)
        c.sendall(b"pwr_on,conv,0\n")
        time.sleep(1)
        c.sendall(b'set_vel,conv,30\n')
        time.sleep(1)
        c.sendall(b"jog_fwd,conv,0\n")
        print("[Conveyor] Running")
        print(c.recv(1024).decode("utf-8"))

    def stop_conveyor(self):
        print("[Conveyor] Stopping conveyor")
        time.sleep(1)
        self.client.sendall(b"jog_stop,conv,0\n")
   

if __name__ == "__main__":
    conveyor = Conveyor(c_ip, c_port)
    if input() == "q":
        conveyor.stop_conveyor()


