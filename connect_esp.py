from wifi_helper import *

if __name__ == "__main__":
    server_name = "RADar"
    password = "BDE4Life!"
    interface_name = "wlan0" # i. e wlp2s0  
    F = Finder(server_name=server_name,
               password=password,
               interface=interface_name)
    F.run()