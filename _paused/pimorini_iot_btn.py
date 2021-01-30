#!/usr/bin/env python

# https://www.pishop.us/product/sleepy-pi-2-power-management-shield-raspberry-pi/
# https://www.amazon.com/Anker-16000mAh-Portable-External-Technology/dp/B00N2T7U90
# https://www.pishop.us/product/compact-rechargeable-battery-for-raspberry-pi-10400mah/

import signal
import buttonshim

print("""Button SHIM: rainbow.py. Light up the LED a different colour of the rainbow with each button pressed. Press Ctrl+C to exit.""")

@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    buttonshim.set_pixel(0x94, 0x00, 0xd3)


@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    buttonshim.set_pixel(0x00, 0x00, 0xff)


@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    buttonshim.set_pixel(0x00, 0xff, 0x00)


@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
    buttonshim.set_pixel(0xff, 0xff, 0x00)


@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):
    buttonshim.set_pixel(0xff, 0x00, 0x00)


signal.pause()


