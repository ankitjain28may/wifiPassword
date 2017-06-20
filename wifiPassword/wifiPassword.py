import argparse
import subprocess
import sys
from colorama import Fore, Style, init
init()

'''
    Author: Ankit Jain
    Email: ankitjain28may77@gmail.com
'''


class WifiPassword:

    def __init__(self):
        self.system = sys.platform
        self.wifiName = None

    def usage(self):
        usage = """
usage: wifiPassword.py [-h] [wifi_name]

positional arguments:
    wifi_name   Name of the WIFI Network

optional arguments:
    -h, --help  show this help message and exit
            """
        print(usage)

    def getresult(self, command, flag=False):
        try:
            output, err = subprocess.Popen(
                command, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            ).communicate()
            output, err = self.decoderesult(output, err, flag)
            return output, err
        except Exception as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
            self.usage()
            sys.exit(2)

    def getpassword(self, name):
        self.wifiName = name
        if self.system == "linux" or self.system == "linux2":
            command = "sudo cat /etc/NetworkManager/system-connections/" + \
                self.wifiName + "| grep psk="
        elif self.system == "darwin":
            print(Fore.RED + "It's not yet available for MAC" +
                  Style.RESET_ALL)
            self.usage()
            sys.exit(2)
        elif self.system == "win32":
            command = "netsh wlan show profile name=" + \
                self.wifiName + " key=clear | findstr Key"
        output, err = self.getresult(command)
        if output == "":
            print(Fore.RED + 'Profile "' + self.wifiName +
                  '" is not found on the system.' + Style.RESET_ALL)
        else:
            print(Fore.GREEN + 'Password for the network ' + Fore.YELLOW +
                  self.wifiName + ': ' + output + Style.RESET_ALL)

    def getprofile(self):
        if self.system == "linux" or self.system == "linux2":
            command = "iwgetid -r"
        elif self.system == "darwin":
            command = ""
        elif self.system == "win32":
            command = "netsh wlan show interfaces | findstr SSID"
        output, err = self.getresult(command, True)
        if output == "":
            print(Fore.RED + 'Either you are not connected to any network or' +
                  ' the system doesn\'t find any network' +
                  Style.RESET_ALL)
        else:
            self.getpassword(output)

    def decoderesult(self, output, err, flag=False):
        try:
            if sys.version_info[0] == 3:
                output = output.decode()
                err = err.decode()
            if flag is True:
                output = output[0:output.find("\n")]
            output = output.strip('\r|\n')
            err = err.strip('\r|\n')
            if output != "":
                output = output.replace(" ", '')
                output = output[output.find(":") + 1:]
            output = output[output.find("=>") + 1:]
            return output, err
        except Exception as e:
            print(Fore.RED + str(e))
            sys.exit(2)


def main():
    '''A cross platform CLI tool to get connected wifi network\'s password.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('wifi_name', nargs='?',
                        help="Name of the WIFI Network", type=str)
    args = parser.parse_args()
    ob = WifiPassword()
    if args.wifi_name is not None:
        ob.getpassword(args.wifi_name)
    else:
        ob.getprofile()


if __name__ == '__main__':
    main()
