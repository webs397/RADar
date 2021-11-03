from networking import *
import random
import time

SSID = 'RADar'
PASSWORT = 'BDE4Life!'

# Handler


# LED WERTE
if __name__ == '__main__':
    led = {'led' : 0}
    try:
        networker = Networker('AP',SSID, PASSWORT)
        for i in range(0,20):
            # LED Werte erfinden
            led['led'] = random.randint(1,20)
            print('gesendet: ', led)
            networker.client.send_udp(led)
            time.sleep(0.01)
    except:
        print('there was an exception')
    finally:
        networker.network.acive(False)
        networker.close_connection()
