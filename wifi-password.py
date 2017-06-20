import argparse
import subprocess
import sys
from colorama import Fore, Style, init
init()


class wifiPassword:

    def __init__(self):
        self.system = sys.platform
        self.wifiName = None

    def getResult(self, command, flag=False):
        output, err = subprocess.Popen(
            command, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        ).communicate()
        output, err = self.decodeResult(output, err, flag)
        return output, err

    def getPassword(self, name):
        self.wifiName = name
        if self.system == "linux" or self.system == "linux2":
            command = "sudo cat /etc/NetworkManager/system-connections/" + \
                self.wifiName + "| grep psk="
        elif self.system == "darwin":
            command = ""
        elif self.system == "win32":
            command = "netsh wlan show profile name=" + \
                self.wifiName + " key=clear | findstr Key"
        output, err = self.getResult(command)
        if output == "":
            print(Fore.RED + 'Profile ' + self.wifiName +
                  ' is not found on the system.' + Style.RESET_ALL)
        else:
            print(Fore.GREEN + 'Password for the network ' + Fore.YELLOW +
                  self.wifiName + ': ' + output + Style.RESET_ALL)

    def getProfile(self):
        if self.system == "linux" or self.system == "linux2":
            command = "iwgetid -r"
        elif self.system == "darwin":
            command = ""
        elif self.system == "win32":
            command = "netsh wlan show interfaces | findstr SSID"
        output, err = self.getResult(command, True)
        if output == "":
            print(Fore.RED + 'Either you are not connected to any network or the system doesn\'t find any network' + Style.RESET_ALL)
        else:
            self.getPassword(output)

    def decodeResult(self, output, err, flag=False):
        if sys.version_info[0] == 3:
            output = output.decode()
            err = err.decode()
        if flag == True:
            output = output[0:output.find("\n")]
        output = output.strip('\r|\n')
        err = err.strip('\r|\n')
        if output != "":
            output = output.replace(" ", '')
            output = output[output.find(":") + 1:]
        return output, err


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('wifi_name', nargs='?',
                        help="Name of the WIFI Network", type=str)
    args = parser.parse_args()
    ob = wifiPassword()
    if args.wifi_name != None:
        ob.getPassword(args.wifi_name)
    else:
        ob.getProfile()
