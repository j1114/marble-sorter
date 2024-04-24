#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
stir_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
optical_sensor = Optical(Ports.PORT2)
door_one_clear = Servo(brain.three_wire_port.a)
door_two_plastic = Servo(brain.three_wire_port.b)
door_three_metal = Servo(brain.three_wire_port.c)
marble_gate = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

#two main variables
#close_state is True whenever the "closing" event activates. So whenever all the doors close, close_state = True
#close_level tells the machine what marble it is sorting, which is helpful in timing for different marbles because their sorting process have different timings
myVariable = 0
closing = Event()
close_state = True
close_level = 3

def when_started1():
    global myVariable, closing, close_state, close_level

#marble_gate is the motor that controls the red wheel acts as the mechanism that only lets one marble through
#optical_sensor is the sensor that determines which marble is which, and if a marble is in front of the first door

#marble_gate's velocity is halved
#optical_sensor's light percent is 50%
#set LED on
    marble_gate.set_velocity(50 ,PERCENT)
    wait(15, MSEC)
    closing.broadcast()
    optical_sensor.set_light_power(50, PERCENT)
    optical_sensor.set_light(LedStateType.ON)
    
#forever loop
    while True:

        #brightness value as a decimal is listed on the brain and refreshes every second
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print(optical_sensor.brightness())
        brain.screen.print(" ")
        wait(1, SECONDS)

        # stir_motor.spin(FORWARD, 6, VOLT)



        #clear inspection
        #if close_level is 1, if the doors are closed, and if it has been .8 seconds from when a marble was inspected
        #dispense one marble, set close_state to False, and set timer to 0
        if close_level == 1 and close_state == True and brain.timer.time(SECONDS) > .8:
            marble_gate.spin_for(REVERSE, 90, DEGREES)
            wait(15, MSEC)
            close_state = False
            brain.timer.clear()

        #plastic inspection
        #if close_level is 2, if the doors are closed, and if it has been 2 seconds from when a marble was inspected
        #dispense one marble, set close_state to False, and set timer to 0
        if close_level == 2 and close_state == True and brain.timer.time(SECONDS) > 2:
            marble_gate.spin_for(REVERSE, 90, DEGREES)
            wait(15, MSEC)
            close_state = False
            brain.timer.clear()

        #metal inspection
        #if close_level is 3, if the doors are closed, and if it has been 2.2 seconds from when a marble was inspected
        #dispense one marble, set close_state to False, and set timer to 0
        if close_level == 3 and close_state == True and brain.timer.time(SECONDS) > 2.2:
            marble_gate.spin_for(REVERSE, 90, DEGREES)
            wait(15, MSEC)
            close_state = False
            brain.timer.clear()

        #clear sorter
        #statement that determines how a marble should be sorted based on its brightness, which is an indicator of what marble type it is
        #if the brightness from the optical sensor is between 7.5 and 13, then the close_level is set to 1, the first door opens, close_state = True, and the doors close
        if 7.5 < optical_sensor.brightness() < 12:
            close_level = 1
            door_one_clear.set_position(100 - 50.0, DEGREES)
            wait(500, MSEC)
            close_state = True
            closing.broadcast()
            
        #plastic sorter
        #if the brightness from the optical sensor is greater than or equal to 33, then the close_level is set to 2, the second door then first door opens, close_state = True, and the doors close
        elif 33 <= optical_sensor.brightness():
            close_level = 2
            door_two_plastic.set_position(30 - 50.0, DEGREES)
            wait(100, MSEC)
            door_one_clear.set_position(100 - 50.0, DEGREES)
            wait(540, MSEC)
            close_state = True
            closing.broadcast()
            
        #metal sorter
        #if the brightness from the optical sensor is between or equal to 12 and 33, then the close_level is set to 3, the second and third doors open, then the first door opens, close_state = True, and the doors close
        elif 12 <= optical_sensor.brightness() < 33:
            close_level = 3
            door_two_plastic.set_position(30 - 50.0, DEGREES)
            door_three_metal.set_position(30 - 50.0, DEGREES)
            wait(100, MSEC)
            door_one_clear.set_position(100 - 50.0, DEGREES)
            wait(1070, MSEC)
            close_state = True
            closing.broadcast()

        #command for if there isn't a marble fed into the system for some reason
        #wait for 5 seconds to pass, then set close_state to True, which essentially allows for marble_gate to turn
        else:
            # closing.broadcast()
            if brain.timer.time(SECONDS) > 2.5:
                close_state = True
                stir_motor.spin(FORWARD, 9, VOLT)
                wait(2, SECONDS)
                stir_motor.stop()

#closing event
#all the servo doors close
def onevent_closing_0():
    global myVariable, closing, close_state, close_level
    door_one_clear.set_position(15 - 50.0, DEGREES)
    door_two_plastic.set_position(100 - 50.0, DEGREES)
    door_three_metal.set_position(100 - 50.0, DEGREES)
    wait(.5, SECONDS)

#system event handlers
closing(onevent_closing_0)
#add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started1()
