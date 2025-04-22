from gripper import Gripper
from conveyor import Conveyor
from arm import Arm
from server import Server
import time
import math

g_ip = "10.10.0.14"
g_port = 63352

# c_ip="10.10.0.98"
c_ip = "0.0.0.0"
c_port = 2002

a_ip  = "10.10.0.14"
a_port  = 30003

conveyor_speed = 20

s_port = 2024

offset = 0.2

gripper = Gripper(g_ip,g_port)
# conveyor = Conveyor(c_ip,c_port)
arm = Arm(a_ip, a_port)
s = Server()

def main():

    # connect
    
    gripper.gripper_connect()
    arm.connect()
    arm.home()
    # go to home position

    _, _, _, rxi, ryi, rzi, _ = arm.baannai()
    gripper.open()
    time.sleep(1.5)

    @s.listen
    def handle_message(msg: str):
        msg = msg[1:-2].split(",")
        # print(msg)
        processed_msg = [e if e != "" else "None" for e in msg]
        # print(processed_msg)
        if processed_msg[0] == 'True':

                if len(processed_msg) == 5:
                    x = int(processed_msg[1])/1000 + 0.29279 - offset
                    y = int(processed_msg[2])/1000 - 0.32984 + 0.015
                    time.sleep(2)
                    arm.movej(
                         x=arm.HOME_X,
                         y=arm.HOME_Y,
                         z=arm.HOME_Z,
                         rx=arm.HOME_RX,
                         ry= -arm.HOME_RY,
                         rz=arm.HOME_RZ,
                         relative=False
                    )
                    time.sleep(3)
                    arm.movel(
                        x = x,
                        y = y,
                        z = -0.225,
                        rx=rxi,
                        ry=-ryi,
                        rz=rzi,
                        # relative=False
                    )
                    time.sleep(1)

                    gripper.close()
                    time.sleep(1)
                    arm.movej(
                         x=arm.HOME_X,
                         y=arm.HOME_Y,
                         z=arm.HOME_Z,
                         rx=3.14,
                         ry= 0,
                         rz=0,
                         relative=False,
                         t=1
                    )
                    time.sleep(1)
                    arm.home() 
                    gripper.open()
                    time.sleep(0.5)

    

            
if __name__ == "__main__":
    main()
    # if input() == "q":
    #     conveyor.stop_conveyor()



