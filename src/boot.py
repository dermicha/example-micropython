import machine
import time
import ujson as json
from network import WLAN


def connect(ssid: str, password: str, timeout: int, retries: int = 5):
    """
    connect to wifi access point
    :param ssid: the network SSID
    :param password: network password
    :param timeout: a timeout, how long to wait for association
    :return:
    """
    # try to join wifi at startup
    wlan = WLAN(mode=WLAN.STA)
    connected = False
    while not connected:
        nets = wlan.scan()
        print("-- searching for wifi networks...")
        for net in nets:
            if net.ssid == ssid:
                print('-- wifi network ' + net.ssid + ' found, connecting ...')
                wlan.connect(ssid, auth=(net.sec, password), timeout=5000)
                while not wlan.isconnected():
                    machine.idle()  # save power while waiting
                print('-- wifi network connected')
                print('-- IP address: ' + str(wlan.ifconfig()))
                rtc = machine.RTC()
                rtc.ntp_sync('pool.ntp.org', 3600)
                while not rtc.synced():
                    time.sleep(1)
                print('-- current time: ' + str(rtc.now()))
                return
        print("!! no usable networks found, trying again in 30s")
        print("!! available networks:")
        print("!! " + repr([net.ssid for net in nets]))
        if --retries > 0:
            time.sleep(30)
        else:
            raise Exception("network association failed with too many retries")


# try to connect via wifi, throws error if config is missing
try:
    with open('boot.json', 'r') as c:
        cfg = json.load(c)
        connect(cfg.get('ssid'), cfg.get('password'), cfg.get('timeout', 5000), cfg.get('retries'))
except Exception as e:
    print("MISSING WIFI CONFIGURATION: wifi.json")
    raise e