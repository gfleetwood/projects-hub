import time
from adafruit_crickit import crickit
from adafruit_motor import stepper

print("Bi-Polar or Uni-Polar Stepper motor demo!")

# make stepper motor a variable to make code shorter to type!
stepper_motor = crickit.stepper_motor
# increase to slow down, decrease to speed up!
INTERSTEP_DELAY = 0.01

while True:
    print("Single step")
    for i in range(200):
        stepper_motor.onestep(direction=stepper.FORWARD)
        time.sleep(INTERSTEP_DELAY)
    for i in range(200):
        stepper_motor.onestep(direction=stepper.BACKWARD)
        time.sleep(INTERSTEP_DELAY)

    print("Double step")
    for i in range(200):
        stepper_motor.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
        time.sleep(INTERSTEP_DELAY)
    for i in range(200):
        stepper_motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        time.sleep(INTERSTEP_DELAY)

    print("Interleave step")
    for i in range(200):
        stepper_motor.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
        time.sleep(INTERSTEP_DELAY)
    for i in range(200):
        stepper_motor.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
        time.sleep(INTERSTEP_DELAY)
