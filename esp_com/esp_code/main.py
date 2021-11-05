from networking import *
import time
import sensing
from machine import Pin


if __name__ == '__main__':
    SSID = 'RADar'
    PASSWORT = 'BDE4Life!'
    FREQUENZ = 10

    just_switched_on = True
    just_switched_off = True
    networker = None

    try:
        networker = Networker('AP',SSID, PASSWORT)
        switch = Pin(3, Pin.IN, Pin.PULL_UP)
        while True:
            if switch.value() == 1:
                if just_switched_on:
                    networker.turn_on()
                    just_switched_on = False
                    just_switched_off = True
                sensing.scan(5)
                msg = sensing.update()
                networker.client.send_udp(msg)
                time.sleep(1/FREQUENZ)
            else:
                if just_switched_off:
                    networker.turn_off()
                    just_switched_off = False
                    just_switched_on = True
                pass
    except Exception as e:
        print('there was an exception:', e)
    finally:
        networker.turn_off()
