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

offset = 0.075

gripper = Gripper(g_ip,g_port)
conveyor = Conveyor(c_ip,c_port)
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
        if msg[0] == "[" and msg[-1] == "]":
            processed_msg = [ elm if elm != "" else "None" for elm in msg[1:-1].split(",")]
            processed_msg[0] = processed_msg[0] == 'True'
            print('processed_msg', processed_msg)
            if processed_msg[0]:
                # move to target and clamp

                x = int(processed_msg[1])/1000 + 0.29279 - offset
                y = int(processed_msg[2])/1000 - 0.32984 + 0.015
                # rzi = int(processed_msg[4])
                # if rzi:
                #     if rzi > 180:
                #         rzi = rzi - 360
                #         rzi = rzi * math.pi / 180
                #     else:
                #         rzi = rzi * math.pi / 180
                # arm.rotate_TCP(rz=rzi)
                # time.sleep(0.5)
                
                arm.movej(
                    x = x,
                    y = y,
                    z = -0.25,
                    rx=rxi,
                    ry=ryi,
                    rz=rzi,
                    relative=False
                )
                time.sleep(1.5)

                gripper.close()
                time.sleep(0.5)

                # move to destination and place

                # arm.baannoon()
                # time.sleep(1)

                # gripper.open()
                # time.sleep(1)

                # return to home position

                arm.home()
                gripper.open()
                time.sleep(0.5)

    

            
if __name__ == "__main__":
    main()
    if input() == "q":
        conveyor.stop_conveyor()



