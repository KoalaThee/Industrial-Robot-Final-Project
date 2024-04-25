import socket
import time

class Arm:
    ip: str = "10.10.0.14"
    port: int = 30003
    client: socket.socket

    def __init__(self, ip: str = None, port: int = None):
        self.port = port or self.port
        self.ip = ip or self.ip
        print(f"[ARM] Connecting to arm at {self.ip}:{self.port}...")
        self.connect()

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.ip, self.port))
        print("[ARM] Connected to arm.")

    def send(self, cmd):
        self.client.send(f"{cmd}\n".encode(encoding="utf-8", errors="ignore"))

    def movej(self, x, y, z, rx, ry, rz, relative):
        if relative:
            move_cmd = f"movej(pose_add(get_actual_tcp_pose(),p[{x or 0},{y or 0},{z or 0},{rx or 0},{ry or 0},{rz or 0}]),2,4,0,0)"
        else:
            move_cmd = f"movej(p[{x or 0},{y or 0},{z or 0},{rx or 0},{ry or 0},{rz or 0}],2,4,0,0)"
        print(f"[ARM] Sending move command: {move_cmd}")
        self.send(move_cmd)

    def movel(self, x, y, z, rx, ry, rz, relative):
        move_cmd = f"movel(pose_add(get_actual_tcp_pose(),p[{x or 0},{y or 0},{z or 0},{rx or 0},{ry or 0},{rz or 0}]),1,0.25,0,0)\n"
        self.send(move_cmd)

    def baannai(self): 
        self.movej( 
            x=0.11665,
            y=-0.30096,
            z=0.06519,
            rx=2.208,
            ry=2.239,
            rz=-0.047,
            relative=False
        )
        return 0.11665,0.32096,-0.05419,2.208,2.239,-0.047,False
    
    def baannoon(self):
        self.movej( 
            x=0.11665,
            y=-0.32096,
            z=-0.15419,
            rx=2.208,
            ry=2.239,
            rz=-0.047,
            relative=False
        )

        time.sleep(2)

        self.movej( 
            x=-0.3069,
            y=-0.34098,
            z=-0.15419,
            rx=2.208,
            ry=2.239,
            rz=-0.047,
            relative=False
        )

        time.sleep(2)

        self.movej( 
            x=-0.3069,
            y=-0.34098,
            z=-0.25,
            rx=2.208,
            ry=2.239,
            rz=-0.047,
            relative=False
        )
        return -0.3069,0.34098,-0.20696,2.208,2.239,-0.047,False


if __name__ == "__main__":
    arm = Arm()
    arm.movej(
                x=0.115,
                y=-0.3,
                z=0.200,
                rx=0,
                ry=3.14,
                rz=0,
                relative=False
            )
