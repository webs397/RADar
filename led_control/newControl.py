#!/usr/bin/env python

"""
shiftreg.py
Shift register control module.  Provides the :class:`Shiftter` class which
makes it easy to control shift registers.
.. note::
    The default pin values are 22, 18, and 16 for data (DS), latch (ST_CP), and
    clock (SH_CP).  These numbers represent GPIO18, GPIO23, and GPIO24
    (`GPIO.BOARD` mode).
"""

import RPi.GPIO as GPIO

# Pinout reference: http://www.raspberrypi-spy.co.uk/wp-content/uploads/2014/07/Raspberry-Pi-GPIO-Layout-Worksheet.pdf

HIGH = True
LOW = False



class Shifter(object):
    """
    A class for controlling one or more shift registers.  When instantiated you
    can choose which pins to use for the *data_pin*, *latch_pin*. and,
    *clock_pin*.
    Optionally, if the *invert* keyword argument is ``True`` then all bitwise
    operations will be inverted (bits flipped) before being sent to the shift
    register.  This is a convenient way to invert things like LED matrices and
    deal with relays that are "active low" (i.e. all relays are on when the
    pins are low instead of high).
    .. note::
        You must ensure that the numbers you pass for the pins match the mode
        you're using with `RPi.GPIO`. 
    """
    def __init__(self, data_pin=13, latch_pin=6, clock_pin=5, invert=False):
        GPIO.setmode(GPIO.BCM)
        self.data_pin = data_pin
        self.latch_pin = latch_pin
        self.clock_pin = clock_pin
        self.invert = invert
        GPIO.setup(self.latch_pin, GPIO.OUT) ## Setup GPIO Pin to OUT
        GPIO.setup(self.clock_pin, GPIO.OUT) ## Setup GPIO Pin to OUT
        GPIO.setup(self.data_pin, GPIO.OUT) ## Setup GPIO Pin to OUT
        self.led_counter = {
            '0': [0b00000000, 0b00000000, 0b00000000],
            '1': [0b00000001, 0b00000000, 0b00000000],
            '2': [0b00000011, 0b00000000, 0b00000000],
            '3': [0b00000111, 0b00000000, 0b00000000],
            '4': [0b00001111, 0b00000000, 0b00000000],
            '5': [0b00011111, 0b00000000, 0b00000000],
            '6': [0b00111111, 0b00000000, 0b00000000],
            '7': [0b01111111, 0b00000000, 0b00000000],
            '8': [0b11111111, 0b00000000, 0b00000000],
            '9': [0b11111111, 0b00000001, 0b00000000],
            '10': [0b11111111, 0b00000011, 0b00000000],
            '11': [0b11111111, 0b00000111, 0b00000000],
            '12': [0b11111111, 0b00001111, 0b00000000],
            '13': [0b11111111, 0b00011111, 0b00000000],
            '14': [0b11111111, 0b00111111, 0b00000000],
            '15': [0b11111111, 0b01111111, 0b00000000],
            '16': [0b11111111, 0b11111111, 0b00000000],
            '17': [0b11111111, 0b11111111, 0b00000001],
            '18': [0b11111111, 0b11111111, 0b00000011],
            '19': [0b11111111, 0b11111111, 0b00000111],
            '20': [0b11111111, 0b11111111, 0b00001111]
        }

    def shift_out(self, *values):
        """
        Shifts out an arbitrary number of *values* which should be integers
        representing a binary values for the shift register.  For example::
            >>> s = ShiftRegister()
            >>> s.shift_out(0b00000001) # Set pin 0 HIGH (all other pins LOW)
            >>> s.shift_out(0b10000000) # Set pin 7 HIGH (all other pins LOW)
            >>> s.shift_out(0b11111111) # Set all pins to HIGH
        If using more than one shift register simply pass multiple values::
            >>> s.shift_out(0b11111111, 0b10101010)
        In the above example, 0b11111111 would go to the first shift register
        while 0b10101010 would go to the second.
        """
        bits = {"0": False, "1": True}
        if self.invert:
            bits = {"1": False, "0": True}
        GPIO.output(self.latch_pin, LOW)
        for val in reversed(values):
            for bit in '{0:08b}'.format(val):
                GPIO.output(self.clock_pin, LOW)
                GPIO.output(self.data_pin, bits[bit])
                GPIO.output(self.clock_pin, HIGH)
        GPIO.output(self.latch_pin, HIGH)

    def test(self):
        """
        Performs a test of the shift register by setting each pin HIGH for .25
        seconds then LOW for .25 seconds in sequence.
        """
        import time
        for i in range(8):
            self.shift_out(1 << i)
            time.sleep(0.25)
            self.shift_out(0)
            time.sleep(0.25)


    def setLights(self, led):
        register_entry = self.led_counter[str(led)]
        self.shift_out(register_entry[0], register_entry[1])


    def all(self, state=LOW):
        """
        Sets all pins on the shift register to the given *state*.  Can be
        either HIGH or LOW (1 or 0, True or False).
        """
        if state:
            self.shift_out(0b11111111)
        else:
            self.shift_out(0)

'''
if __name__=="__main__":
    print("Testing shift register connection...")
    print("Each pin should go HIGH and LOW in order until you press Ctrl-C.")
    GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
    s = Shifter()
    try:
        while True:
            s.test()
    except KeyboardInterrupt:
        print("Ctrl-C detected.  Quitting...")
        '''