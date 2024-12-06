VARUN="E03970000-3100-3D00-0F51-313239373239"
def is_id(id):
    return id==hub.hardware_id()+hub.device_uuid()
import app
import hub
from motor import BRAKE, run as __spike3_run, stop as __spike3_stop, run_for_degrees as __spike3_run_for_degrees, READY as __spike3_READY, RUNNING as __spike3_RUNNING, STALLED as __spike3_STALLED, CANCELLED as __spike3_CANCELED, ERROR as __spike3_ERROR, run_for_time as __spike3_run_for_time, SHORTEST_PATH as __spike3_SHORTEST_PATH, CLOCKWISE as __spike3_CLOCKWISE, COUNTERCLOCKWISE as __spike3_COUNTERCLOCKWISE, run_to_absolute_position as __spike3_run_to_absolute_position, DISCONNECTED as __spike3_DISCONNECTED
import motor
import motor_pair as __motor_pair
from color_sensor import color as __spike3_color, reflection as __spike3_reflection
import distance_sensor
import force_sensor
from hub import port, light_matrix, button, motion_sensor, button
from time import sleep_us, time
from runloop import run, sleep_ms, until
from math import pi
from app import sound
from color import *
import color_sensor
import random
import utime

class Motor:
    def __init__(self, port_letter: str):
        self.port = getattr(port, port_letter)
        self.degrees_ran=0
    def set_degrees_counted(self, degrees: int):
        self.degrees_ran=degrees
    def get_degrees_counted(self):
        return self.degrees_ran
    # Eery async function will have a wrapper that is not for async for compatibility
    def set_default_speed(self, default_speed):
        self.default_speed=default_speed
    def run_for_degrees(self, degrees, speed=None):
        run(self.__run_for_degrees(degrees, self.default_speed if speed is None else speed))
    async def __run_for_degrees(self, degrees, speed):
        ret = await __spike3_run_for_degrees(self.port, degrees, speed)
        if ret == __spike3_DISCONNECTED:
            raise RuntimeError('Motor got unexpectedly removed from port.')
        self.degrees_ran+=degrees
        return

    def run_for_rotations(self, rotations, speed):
        self.run_for_degrees(rotations*360, speed)
    def run_for_seconds(self, seconds, speed):
        run(self.__run_for_seconds(seconds, speed))
    async def __run_for_seconds(self, seconds, speed):
        ret = await __spike3_run_for_time(self.port, seconds, speed)
        if ret == __spike3_DISCONNECTED:
            raise RuntimeError('Motor got unexpectedly removed from port.')
        self.degrees_ran+=seconds*speed
        return

    def start(self, speed):
        __spike3_run(self.port, speed)

    def stop(self):
        __spike3_stop(self.port)

    def run_to_position(self, degrees: int, direction='shortest path', speed: int|None = None, stop=motor.BRAKE):
        '''
    Runs the motor to an absolute position.

    The motor will always travel in the direction specified by the 'direction' parameter.
    If the sign of the speed is positive, it will go in the same direction at that speed. Otherwise, it will go in the different direction at the opposite sign speed.
    If the speed is greater than 650, it will be limited to 650.

    Parameters:
    ----------
    degrees : int
        The target position for the motor. Must be an integer in the range of 0 to 359 (inclusive).

    direction : str
        The direction to use to reach the target position. Must be one of the following:
        - 'shortest path': The motor will choose the shortest route to the target position.
        - 'clockwise': The motor will run clockwise until it reaches the target position.
        - 'counterclockwise': The motor will run counterclockwise until it reaches the target position.

    speed : int, optional
        The motor’s speed as a velocity (0 to 650). If no value is specified, it will use the default speed
        set by `set_default_speed()`.

    Raises:
    -------
    TypeError
        If degrees or speed is not an integer, or if direction is not a string.

    ValueError
        If direction is not one of the allowed values or if degrees is not within the range of 0-359 (inclusive).

    RuntimeError
        If the motor has been disconnected from the port.

    Example:
    --------
    motor = Motor('A')
    motor.run_to_position(90, 'clockwise', speed=75)
    '''
        run(self.__run_to_position(degrees, direction, self.default_speed if speed is None else speed, stop))

    async def __run_to_position(self, degrees, direction, speed, stop):
        if not isinstance(degrees, int):
            raise TypeError('Degrees must be an integer')
        if not isinstance(speed, int):
            raise TypeError('Speed must be an integer')
        if not isinstance(direction, str):
            raise TypeError('Direction must be an string')
        if direction == 'shortest path':
            direction=__spike3_SHORTEST_PATH
        elif direction == 'clockwise':
            direction=__spike3_CLOCKWISE
        elif direction == 'counterclockwise':
            direction=__spike3_COUNTERCLOCKWISE
        else:
            raise ValueError('Direction is not "shortest path", "clockwise" or "counterclockwise"')
        if not 0 <= degrees <= 359:
            raise ValueError('Degrees not in range of 0-359')
        ret = await __spike3_run_to_absolute_position(self.port, degrees%360, speed if speed is not None else self.default_speed, direction=direction, stop=stop)
        if ret == __spike3_DISCONNECTED:
            raise RuntimeError('Motor has been disconnected from port')

class MotorPair:
    def __init__(self, left_port, right_port, wheel_diameter_mm=None, one_motor_rotation_in_cm=None, color_sensor=None):
        assert (not ((wheel_diameter_mm is None) ^ bool(one_motor_rotation_in_cm is None))) |(wheel_diameter_mm is None) ^ bool(one_motor_rotation_in_cm is None), 'either wheel_diameter_mm or one_motor_rotation_in_cm must be specified'
        if wheel_diameter_mm:
            self.set_wheel_diameter(wheel_diameter_mm)
        else:
            self.set_motor_rotation(one_motor_rotation_in_cm)
        self.pair = __motor_pair.PAIR_1
        self.steering=(0-motion_sensor.tilt_angles()[0])*1.4
        self.left_motor=left_port
        self.right_port=right_port
        self.set_speed(100)
        self.color_sensor=color_sensor

        __motor_pair.pair(self.pair, getattr(port, left_port), getattr(port, right_port))
    async def tank(self, amount, unit, left_speed=None, right_speed=None):
        run(self.__move_tank(amount, unit, left_speed, right_speed))
    def set_left_speed(self, left_speed):
        self.left_speed=left_speed
    def set_right_speed(self, right_speed):
        self.right_speed=right_speed
    async def __move_tank(self, amount, unit, left_speed=None, right_speed=None):
        amount = self.__cm_to_degrees(amount, self.wheel_diameter_mm)# Convert cm to degrees
        print("move tank")
        print(amount)
        await __motor_pair.move_tank_for_degrees(self.pair, amount, left_speed*11, right_speed*11)
    def start_tank(self, left_speed, right_speed):
        __motor_pair.move_tank(self.pair, left_speed, right_speed)
    def forward(self, left_speed, right_speed):
        self.start_tank(left_speed, right_speed)
    def stop(self):
        __motor_pair.stop(self.pair)
    def backward(self, left_speed, right_speed):
        self.start_tank(-left_speed, -right_speed)

    def set_speed(self, speed):
        self.left_speed=speed
        self.right_speed=speed

    def forward_for(self, amount, unit, left_speed=None, right_speed=None):
        run(self.__forward_for(amount, unit, left_speed, right_speed))
    async def __forward_for(self, amount, unit, left_speed=None, right_speed=None):
        await self.tank(amount, unit, left_speed, right_speed)
    def backward_for(self, amount, unit, left_speed, right_speed):
        run(self.__backward_for(amount, unit, left_speed, right_speed))
    async def __backward_for(self, amount, unit, left_speed, right_speed):
        await self.tank(amount, unit, -left_speed, -right_speed)
    def left_motor_left_for(self, speed, yaw):
        run(self.__left_motor_left_for(speed, yaw))
    async def __left_motor_left_for(self, speed, yaw):
        self.start_tank(-speed, 0)
        def func():
            current_yaw, _, _ = motion_sensor.tilt_angles()
            current_yaw/=10
            return current_yaw >= yaw
        await until(func)
        self.stop()
    def right_motor_left_for(self, speed, yaw):
        run(self.__right_motor_left_for(speed, yaw))
    async def __right_motor_left_for(self, speed, yaw):
        self.start_tank(0, speed)
        def func():
            current_yaw, _, _ = motion_sensor.tilt_angles()
            current_yaw/=10
            return current_yaw >= yaw
        await until(func)
        self.stop()
    def left_motor_right_for(self, speed, yaw):
        run(self.__left_motor_right_for(speed, yaw))
    async def __left_motor_right_for(self, speed, yaw):
        self.start_tank(speed, 0)
        def func():
            current_yaw, _, _ = motion_sensor.tilt_angles()
            current_yaw/=10
            return current_yaw <= yaw
        await until(func)
        self.stop()
    def right_motor_right_for(self, speed, yaw):
        run(self.__right_motor_right_for(speed, yaw))
    async def __right_motor_right_for(self, speed, yaw):
        self.start_tank(0, -speed)
        def func():
            current_yaw, _, _ = motion_sensor.tilt_angles()
            current_yaw/=10
            return current_yaw <= yaw
        await until(func)
        self.stop()

    @staticmethod
    def __cm_to_degrees(distance_cm, wheel_diameter_mm):
        wheel_circumference_mm = wheel_diameter_mm * pi
        return int((distance_cm * 360) / (wheel_circumference_mm / 10))
    @staticmethod
    def __in_to_cm(distance_in):
        return distance_in*2.54
    def set_motor_rotation(self, distance: float):
        self.wheel_diameter_mm=(distance / pi) * 10
    def set_wheel_diameter(self, wheel_diameter_mm):
        self.wheel_diameter_mm = wheel_diameter_mm
    def forward_to(self, color: list[int], left_speed=None, right_speed=None):
        run(self.__forward_to(color, left_speed, right_speed))
    async def __forward_to(self, color: list[int], left_speed=None, right_speed=None):
        self.forward(left_speed, right_speed)
        def color_sensor_is():
            if self.pair is not None:
                return color_sensor.color(self.color_sensor) in color
            raise ValueError("Color sensor not supplied when creating class")
        await until(color_sensor_is)
        self.stop()
    def backward_to(self, color: list[int], left_speed=None, right_speed=None):
        self.forward_to(color, -left_speed if left_speed is not None else None, -right_speed if right_speed is not None else None)
    def forward_to_blue_border(self, left_speed, right_speed):
        self.forward_to([BLUE,AZURE], left_speed, right_speed)
    def forward_to_red_border(self, left_speed, right_speed):
        self.forward_to([RED], left_speed, right_speed)
class ColorSensor:
    def __init__(self, port_letter):
        self.port = getattr(port, port_letter)

    def get_color(self):
        return __spike3_color(self.port)

    def get_reflected_light(self):
        return __spike3_reflection(self.port)

class DistanceSensor:
    def __init__(self, port_letter):
        self.port = getattr(port, port_letter)

    def get_distance_cm(self):
        return distance_sensor.distance(self.port) / 10# Convert mm to cm

class ForceSensor:
    def __init__(self, port_letter):
        self.port = getattr(port, port_letter)

    def is_pressed(self):
        return force_sensor.pressed(self.port)

    def get_force_newton(self):
        return force_sensor.force(self.port) / 100# Convert centinewtons to newtons
class PrimeHub:
    def __init__(self):
        self.light_matrix = light_matrix
        self.left_button = button.LEFT
        self.right_button = button.RIGHT
        self.motion_sensor = motion_sensor
        self.speaker = sound


    def play_sound(self, sound_name):
        self.speaker.play(getattr(self.speaker, sound_name))

    @staticmethod
    async def wait_for_seconds(seconds):
        await sleep_ms(seconds*1000)

class MotionSensor:
    @staticmethod
    def get_yaw():
        yaw, _, _=motion_sensor.tilt_angles()
        yaw=(-yaw)/10
        return yaw
    @staticmethod
    def reset_yaw(yaw):
        motion_sensor.reset_yaw(yaw)
if __name__ == '__main__':
    gyro=MotionSensor()
    motion_sensor.reset_yaw(0)
async def __wait_for_no_button(resume_button):
    def func():
        return (button.pressed(resume_button) == 0)
    await until(func)
async def __wait_for_button(resume_button):
    def func():
        return not (button.pressed(resume_button) == 0)
    await until(func)
def breakpoint(button):
    run(__wait_for_button(button))
    run(__wait_for_no_button(button))
MotionSensor().reset_yaw(0)
front_arm=Motor("F")
move=MotorPair("A", "D", wheel_diameter_mm=55.25, color_sensor=port.C)
back_arm=Motor("E")
async def main():
    ...
    async def init():
        hub.light.color(hub.light.POWER,ORANGE)

        #hub.light_matrix.show_image(1)
        #run(motor.run_to_absolute_position(port.E, 200, 100, stop=motor.HOLD))
        #hub.light_matrix.show_image(2)
        run(motor.run_to_absolute_position(port.F, 100, 50, direction=motor.SHORTEST_PATH, stop=motor.HOLD))
        run(motor.run_to_absolute_position(port.E, 100, 650, direction=motor.COUNTERCLOCKWISE, stop=motor.HOLD))
        run(motor.run_to_absolute_position(port.E, 62, 10, direction=motor.SHORTEST_PATH, stop=motor.HOLD))
        #print("E pos",motor.absolute_position(port.E))

    def scuba():
        #all the way front
#        move.forward_for(59, "cm", 100,100)
        #print("calling 315")
        run(__motor_pair.move_tank_for_degrees(__motor_pair.PAIR_1, 456,-7150,-7150))#move.backward_for(22,"cm",650,650)
        move.forward_to([RED],-100,-100)
        #print("calling 318")

        run(__motor_pair.move_tank_for_degrees(__motor_pair.PAIR_1, 487,-7150,-7150))#move.backward_for(23.5,"cm",650,650)
        

        #position for scuba
        move.right_motor_left_for(650, 38)
        ##Vihaan=58. Varun=56
        if is_id(VARUN):
            move.right_motor_left_for(50, 56)
        else:          
            move.right_motor_left_for(50, 58)                                                   
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!get guy first",MotionSensor.get_yaw(),"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        #first ram in
        sleep_ms(50)
        #print("calling 330")

        run(__motor_pair.move_tank_for_degrees(__motor_pair.PAIR_1, 290,-110,-110))
        #move.backward_for(14,"cm", 10,10)
        sleep_ms(50)
        #global get_guy
        #get_guy=MotionSensor.get_yaw()
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!get guy",MotionSensor.get_yaw(),"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #get the guy
        breakpoint(button.LEFT)
        run(motor.run_for_degrees(port.E, 40, 20, stop=motor.HOLD))
        sleep_ms(100)
        #print("calling 339")

        
        run(__motor_pair.move_tank_for_degrees(__motor_pair.PAIR_1, 41,110,110))#move.forward_for(2 ,"cm", 10,10)
        run(motor.run_for_degrees(port.E, 100, 50, stop=motor.HOLD))
    def ensure_coral_reef():
        # second ram in
        #print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!get guy",MotionSensor.get_yaw(),"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        #print("calling 346")

        run(__motor_pair.move_tank_for_degrees(__motor_pair.PAIR_1, 207,-2200,-2200))#move.backward_for(10,"cm",200,200)
    def go_home():
        
        run(__motor_pair.move_tank_for_degrees(__motor_pair.PAIR_1, 207,7150,7150))#move.forward_for(10, "cm",650, 650)
        move.left_motor_left_for(650, 110)
        move.left_motor_left_for(300, 136)
        #move.left_motor_left_for(50, 136)

        #print("calling 355")

        
        run(__motor_pair.move_tank_for_degrees(__motor_pair.PAIR_1, 456,-7150,-7150))#move.backward_for(22, "cm", 650, 650)
        breakpoint(button.LEFT)

        move.left_motor_left_for(300, 160)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!grab",MotionSensor.get_yaw(),"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        #print(get_guy, MotionSensor.get_yaw(), sep=",")
        run(motor.run_to_absolute_position(port.F, 20, 650, stop=motor.HOLD))
        run(motor.run_to_absolute_position(port.F, 330, 150, stop=motor.HOLD))
        #print("calling 364")

        
        run(__motor_pair.move_tank_for_degrees(__motor_pair.PAIR_1, 725,-7150,-7150))#move.backward_for(35, "cm", 650, 650)
    front_arm.run_to_position(95, speed=650)
    back_arm.run_to_position(300, speed=650)
    await init()
    scuba()
    ensure_coral_reef()
    go_home()
if __name__ == '__main__':
    run(main())