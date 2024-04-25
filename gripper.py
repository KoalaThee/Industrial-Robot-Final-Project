import socket 
import time

ip = "10.10.0.14"
port = 63352

class Gripper:
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.gripper = None
    
    def gripper_connect(self):
        g = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        addr = tuple((self.ip,self.port))
        g.connect(addr)
        print(f"[Gripper] Gripper connection from {addr}")
        g.send(b"GET ACT\n")
        g_recv = str(g.recv(10),"utf-8")
        g.send(b"SET SPE 255\n")

        if '1' in g_recv:
            print("[Gripper] Gripper Activated")

        self.gripper = g

    def open(self):
        self.gripper.send(b'SET POS 0\n')
        print("[Gripper] Opening Gripper")

    def close(self):
        self.gripper.send(b'SET POS 255\n')
        print("[Gripper] Closing Gripper")
        

if __name__ == "__main__":
    gripper = Gripper(ip,port)
    gripper.gripper_connect()
    gripper.open()
    time.sleep(2)
    gripper.close()

