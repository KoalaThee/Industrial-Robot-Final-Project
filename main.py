from gripper import Gripper
from conveyor import Conveyor
from arm import Arm
from server import Server
import time

g_ip = "10.10.0.14"
g_port = 63352

c_ip = "10.10.0.98"
c_port = 2002

a_ip  = "10.10.0.14"
a_port  = 30003

conveyor_speed = 40

s_port = 3000

offset = 0.075

def main():

    # initialize

    gripper = Gripper(g_ip,g_port)
    conveyor = Conveyor(c_ip,c_port)
    arm = Arm(a_ip, a_port)
    s = Server(port = s_port)

    # connect
    
    gripper.gripper_connect()
    conveyor.conveyor_connect()

    # run

    conveyor.run_conveyor(conveyor_speed)

    # go to home position

    xi, yi, zi, rxi, ryi, rzi, reli = arm.baannai()
    gripper.open()
    time.sleep(1.5)

    @s.listen
    def handle_message(msg: str):
        if msg[0] == "[" and msg[-1] == "]":
            processed_msg = [ elm if elm != "" else "None" for elm in msg[1:-1].split(",")]
            processed_msg[0] = processed_msg[0] == 'True'

            if processed_msg[0]:

                # move to target and clamp

                processed_msg[1] = int(processed_msg[1])
                x = int(processed_msg[1])/1000 + 0.29279 - offset
                processed_msg[2] = int(processed_msg[2])
                y = int(processed_msg[2])/1000 - 0.32984 + 0.015
            
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

                arm.baannai()
                time.sleep(2)

                gripper.open()
                time.sleep(0.5)
    

            
if __name__ == "__main__":
    main()