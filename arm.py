import socket
import time

class Arm:
    HOME_X = 0.116
    HOME_Y = -0.300
    HOME_Z = 0.08
    HOME_RX = 2.233
    HOME_RY = 2.257
    HOME_RZ = -0.039 
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
    
    def home(self):
        print('Robot start moving to home position')
        cmd_move = str.encode(f'movel(p[{self.HOME_X},{self.HOME_Y},{self.HOME_Z},{self.HOME_RX},{self.HOME_RY},{self.HOME_RZ}],a=0.5,v=0.5,t=1,r=0)\n')
        self.client.send(cmd_move)
        time.sleep(2)
    
    def rotate_TCP(self, rz):
        cmd_move = str.encode(f'movel(p[{self.HOME_X},{self.HOME_Y},{self.HOME_Z},{self.HOME_RX},{self.HOME_RY},{rz}],a=0.5,v=0.5,t=1,r=0)\n')
        self.client.send(cmd_move)

    def movej(self, x, y, z, rx, ry, rz, relative, t=0):
        if relative:
            move_cmd = f"movej(pose_add(get_actual_tcp_pose(),p[{x or 0},{y or 0},{z or 0},{rx or 0},{ry or 0},{rz or 0}]),2,4,{t},0)"
        else:
            move_cmd = f"movej(p[{x or 0},{y or 0},{z or 0},{rx or 0},{ry or 0},{rz or 0}],2,4,{t},0)"
        print(f"[ARM] Sending move command: {move_cmd}")
        self.send(move_cmd)

    def movel(self, x, y, z, rx, ry, rz):
        move_cmd = f"movel(p[{x or 0},{y or 0},{z or 0},{rx or 0},{ry or 0},{rz or 0}],1,4,0,0)"
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
    arm.baannai()
    time.sleep(1.5)
    arm.baannoon()
    time.sleep(1.5)    
    
