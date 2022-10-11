# IMPORT CÁC ĐỐI TƯỢNG TỪ THƯ VIỆN

import sys
from drivetrain import Drivetrain
from random import randint
from timer import Timer

from vex import (
    Gyro, Motor, Ports, DEGREES, FORWARD, REVERSE, LEFT, RIGHT, MM, PERCENT,
    Touchled, ColorHue,
    Bumper, Sonar, DistanceUnits,
    Controller,
)
# KHỞI TẠO CÁC BỘ PHẬN ROBOT
# ==========================
#brain           = vex.Brain()

# khởi tạo bộ điều khiển từ xa
ctl = Controller()
# nếu joystick không di chuyển hơn 3% thì coi như joystick không di chuyển
ctl.set_deadband(3)

#Assign 4 legs of crocodile
motor_right_front = Motor(Ports.PORT6)
motor_right_rear = Motor(Ports.PORT12)
motor_left_front = Motor(Ports.PORT1)
motor_left_rear = Motor(Ports.PORT7)

dt_front        = Drivetrain(motor_right_front, motor_left_front, 300, 190, DistanceUnits.MM, 1)
dt_rear        = Drivetrain(motor_right_rear, motor_left_rear, 300, 190, DistanceUnits.MM, 1)
dt_right        = Drivetrain(motor_right_front, motor_right_front, 300, 190, DistanceUnits.MM, 1)
dt_left        = Drivetrain(motor_left_front, motor_left_front, 300, 190, DistanceUnits.MM, 1)

#Control mode
touch_led_mode = Touchled(Ports.PORT7) 
touch_led_right = Touchled(Ports.PORT10) 
touch_led_left = Touchled(Ports.PORT8)
touch_led_mouth = Touchled(Ports.PORT9)

#Distance sensor
distance_sensor = Sonar(Ports.PORT3)

# Main mode: normal and shake a tail
CROC_SYS_MODE_SHAKE_TAIL = 0                #go and shake a tail
CROC_SYS_MODE_NORM = 1                      #normmal
CROC_SYS_MODE_MANUAL = 2                    #manipulate by controller
CROC_SYS_MODE_MAX = CROC_SYS_MODE_MANUAL

croc_sys_mode = CROC_SYS_MODE_SHAKE_TAIL

# LED mode
CROC_LED_MODE_OFF = 0
CROC_LED_MODE_SINGLE_CLR = 1                #single color
CROC_LED_MODE_AMBIENCE = 2                  #multiple colors depend on specific context
CROC_LED_MODE_MAX = CROC_LED_MODE_AMBIENCE
croc_led_mode = CROC_LED_MODE_SINGLE_CLR

# SOUND mode
SOUND_RAND = 99 #random sound id

# CHƯƠNG TRÌNH CHÍNH
#================

dt = dt_front
# Đặt tốc độ của động cơ
dt.set_drive_velocity(30)
# Điều khiển robot di chuyển 1000 mm
#dt.start_drive_for(FORWARD, 1000, DistanceUnits.MM)

dt = dt_rear
# Đặt tốc độ của động cơ
dt.set_drive_velocity(30)
# Điều khiển robot di chuyển 1000 mm
#dt.start_drive_for(FORWARD, 1000, DistanceUnits.MM)

dt = dt_right
# Đặt tốc độ của động cơ
dt.set_drive_velocity(30)
# Điều khiển robot di chuyển 1000 mm
#dt.start_drive_for(FORWARD, 1000, DistanceUnits.MM)

dt = dt_left
# Đặt tốc độ của động cơ
dt.set_drive_velocity(30)
# Điều khiển robot di chuyển 1000 mm
#dt.start_drive_for(FORWARD, 1000, DistanceUnits.MM)

def Input_proc():
    if touch_led_mode.pressing():
        sound_play(15)
        croc_sys_mode = croc_sys_mode + 1
        if croc_sys_mode > CROC_SYS_MODE_MAX:
            croc_sys_mode = CROC_SYS_MODE_SHAKE_TAIL
    
    if touch_led_mouth.pressing():
        sound_play(SOUND_RAND)
    
    if touch_led_right.pressing():
        sound_play(15)
        croc_led_mode = croc_led_mode + 1
        if croc_led_mode > CROC_LED_MODE_SIGLE_MAX:
            croc_led_mode = CROC_LED_MODE_OFF
    
    if touch_led_left.pressing():
        sound_play(15)
        #change original color of all LED

def move_and_shake_tail():
    dt_front.start_turn_for(LEFT, 30)
    #dt_front.start_turn_for(LEFT,30,DEG,100,0,False)
    sys.sleep(0.5)
    
    dt_front.start_turn_for(RIGHT, 30)
    #dt_front.start_turn_for(RIGHT,30,RotationUnits.DEG,100,0,False)
    sys.sleep(0.5)
    move_forward(50)

def move_forward(distance):
    dt_front.drive_for(FORWARD, distance, DistanceUnits.MM)
    dt_rear.drive_for(FORWARD, distance, DistanceUnits.MM)

def Interact_proc():
    distance = distance_sensor.distance()
    if distance < 300:
        move_backward(30)
        turn_right(30)

def LED_proc():
    if croc_led_mode == CROC_LED_MODE_SINGLE_CLR:
        touch_led_mode.on_hue(7,100)
        touch_led_right.on_hue(7,100)
        touch_led_left.on_hue(7,100)
        touch_led_mouth.on_hue(7,100)

    elif croc_led_mode == CROC_LED_MODE_AMBIENCE:
        color = randint(0, 15)
        touch_led_mode.on_hue(color,100)
        touch_led_right.on_hue(color,100)
        touch_led_left.on_hue(color,100)
        touch_led_mouth.on_hue(color,100)

def Moving_proc():
    if croc_sys_mode == CROC_SYS_MODE_SHAKE_TAIL:
        move_and_shake_tail()
    elif croc_sys_mode == CROC_SYS_MODE_NORM:
        move_forward()
    #delay litle bit

def Controller_proc():
    if ctl.buttonEDown.pressing() and ctl.buttonFDown.pressing():
        if croc_sys_mode == CROC_SYS_MODE_MANUAL:
            croc_sys_mode = CROC_SYS_MODE_NORM
        else:
            croc_sys_mode = CROC_SYS_MODE_MANUAL
        
        #immidately impact 
        return
    
    if ctl.buttonEUp.pressing():
        sound_play(1)  
    
    elif ctl.buttonFUp.pressing():
        touch_led_mouth.blink_hue(GREEN,0.5,0.5)
        #Turn on led in green
        #touch_led_mouth.on_rgb(0,255,0,100)
        sound_play(2)
    
    elif ctl.buttonLUp.pressing():
        sound_play(15)
    elif ctl.buttonLDown.pressing():
        sound_play(15)
    elif ctl.buttonRUp.pressing():
        sound_play(15)
    elif ctl.buttonRDown.pressing():
        sound_play(15)
        
    # manipulate by controller
    #if croc_sys_mode == CROC_SYS_MODE_MANUAL:
     #   drive_by_controller()

# lái 2 bánh xe bằng 2 joystick (A + D) của bộ điều khiển từ xa
def drive_by_controller():
    # lái bánh xe bên trái bằng joystick A
    motor_right_front.spin(FORWARD, ctl.axisA.position(), PERCENT)
    motor_right_rear.spin(BACKWARD, ctl.axisA.position(), PERCENT)

    # lái bánh xe bên phải bằng joystick D
    motor_left_front.spin(FORWARD, ctl.axisD.position(), PERCENT)
    motor_left_rear.spin(BACKWARD, ctl.axisD.position(), PERCENT)

def sound_play(sound_id):
    if sound_id == SOUND_RAND or sound_id > 15:
        brain.sound.play_wave(randint(0, 15))
    else:
        brain.sound.play_wave(sound_id)
    
while True:
    # Handling all input
    Input_proc()
    
    # Moving croc     
    Moving_proc()

    # Interact with student, sonar sensor
    Interact_proc() 

    # Manipulate robot manually by controller
    Controller_proc()
    LED_proc()
