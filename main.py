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

    #receive predefined rotation angle 
    _, _, _, rxi, ryi, rzi, _ = arm.baannai()
    gripper.open()
    time.sleep(1.5)

    @s.listen
    def handle_message(msg: str):
        #split message from vision builder into python list
        msg = msg[1:-2].split(",")
        processed_msg = [e if e != "" else "None" for e in msg]
        if processed_msg[0] == 'True':

                #check length of the message to avoid false data from buffer
                if len(processed_msg) == 5:
                    x = int(processed_msg[1])/1000 + 0.29279 - offset
                    y = int(processed_msg[2])/1000 - 0.32984 + 0.015
                    time.sleep(2)
                    #flip the robot 180 degree
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
                    #move the UR arm to pick up point
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
                    #pick up the box
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
                    #return to initial position
                    arm.home() 
                    gripper.open()
                    time.sleep(0.5)

    

            
if __name__ == "__main__":
    main()




