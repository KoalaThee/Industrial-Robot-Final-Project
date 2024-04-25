import socket
import time

ip = "10.10.0.98"
port = 2002

SPEED = 0.4

class Conveyor:
    client = socket.socket()
    def __init__(self, ip, port):
        self.port = port or self.port
        self.ip = ip or self.ip
        self.speed = SPEED
        print(f"[Conveyor] Conveyor connection from {self.ip}:{self.port}...")
        #self.conveyor_connect()

    def conveyor_connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen()
        #print(f"Server listening at {self.ip}:{self.port}")
        c, addr = s.accept()
        print(f"[Conveyor] Connected by {addr}")
        c.sendall(b"activate,tcp,0.0\n")
        c.sendall(b"pwr_on,conv,0\n")
        self.client = c

    def run_conveyor(self,speed):
        time.sleep(1)
        set_vel = f"set_vel,conv,{speed}\n".encode()
        self.client.sendall(set_vel)
        self.client.sendall(b"jog_fwd,conv,0\n")
        #print(self.client.recv(20))

    def stop_conveyor(self):
        print("[Conveyor] Stopping conveyor")
        time.sleep(1)
        self.client.sendall(b"jog_stop,conv,0\n")
        #print(self.client.recv(20))

if __name__ == "__main__":
    conveyor = Conveyor(ip,port)
    conveyor.conveyor_connect()
    conveyor.run_conveyor(SPEED)
    if input() == "q":
        conveyor.stop_conveyor()

