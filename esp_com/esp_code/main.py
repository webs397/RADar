from networking import *
import time
import sensing
from machine import Pin


if __name__ == '__main__':
    SSID = 'RADar'
    PASSWORT = 'BDE4Life!'
    FREQUENZ = 10
    SWITCH = 16
    LED = 0

    just_switched_on = True
    just_switched_off = True
    networker = None
    was_turned_on = False

    try:
        networker = Networker('AP',SSID, PASSWORT)
        switch = Pin(SWITCH, Pin.IN)
        led = Pin(LED, Pin.OUT)
        while True:
            if switch.value() == 1:
                if just_switched_on:
                    was_turned_on = True
                    led.on()
                    networker.turn_on()
                    just_switched_on = False
                    just_switched_off = True
                sensing.scan(5)
                msg = sensing.update()
                '''
                for i in range(10):
                    msg = {'i' : i}
                    networker.client.send_udp(msg)
                '''
                networker.client.send_udp(msg)
                time.sleep(1/FREQUENZ)
            else:
                if just_switched_off:
                    if was_turned_on:
                        networker.turn_off()
                    just_switched_off = False
                    just_switched_on = True
                    led.off()
                pass
    except Exception as e:
        print('there was an exception:', e)
    finally:
        if was_turned_on:
            networker.turn_off()
