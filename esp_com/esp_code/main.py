from networking import *
import time
import sensing

SSID = 'RADar'
PASSWORT = 'BDE4Life!'
FREQUENZ = 10

if __name__ == '__main__':
    try:
        networker = Networker('AP',SSID, PASSWORT)
        
        while True:
            sensing.scan(5)
            msg = sensing.update()
            networker.client.send_udp(msg)
            time.sleep(1/FREQUENZ)
            # check some button for shutdown
            '''
            if button pressed:
                break
            '''
    except Exception as e:
        print('there was an exception:', e)
    finally:
        networker.network.active(False)
        networker.close_connection()
