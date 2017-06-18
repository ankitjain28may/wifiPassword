import argparse
import subprocess
import sys


class wifiPassword:

    def __init__(self, name):
        self.system = sys.platform
        self.wifiName = name
        self.getPassword()

    def getResult(self, command):
        output, err = subprocess.Popen(
            command, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        ).communicate()
        output, err = self.decodeResult(output, err)
        return output, err

    def getPassword(self):
        if self.system == "linux" or self.system == "linux2":
            command = "sudo cat /etc/NetworkManager/system-connections/" + \
                self.wifiName + "| grep psk="
        elif self.system == "darwin":
            command = ""
        elif self.system == "win32":
            command = "netsh wlan show profile name=" + \
                self.wifiName + " key=clear | findstr Key"
        print(self.getResult(command))

    def decodeResult(self, output, err):
        if sys.version_info[0] == 3:
            output = output.decode()
            err = err.decode()
        output = output.strip('\r|\n')
        err = err.strip('\r|\n')
        return output, err


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('wifi_name', nargs='?',
                        help="Name of the WIFI Network", type=str)
    args = parser.parse_args()
    if args.wifi_name != None:
        ob = wifiPassword(args.wifi_name)
