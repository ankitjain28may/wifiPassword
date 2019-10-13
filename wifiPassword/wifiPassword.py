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
            output, _ = subprocess.Popen(
                command, stdout=subprocess.PIPE,
                stderr=None,
                shell=True
            ).communicate()
            output = self.decoderesult(output, flag)
            return output
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
            command = "sudo security find-generic-password -l" + \
                self.wifiName + " -D 'AirPort network password' -w"
        elif self.system == "win32":
            command = "netsh wlan show profile name=" + \
                self.wifiName + " key=clear | findstr Key"
        output = self.getresult(command)
        return output

    def getprofile(self):
        if self.system == "linux" or self.system == "linux2":
            command = "iwgetid -r"
        elif self.system == "darwin":
            command = "/System/Library/PrivateFrameworks/" + \
                "Apple80211.framework/Versions/Current/Resources/" + \
                "airport -I | sed -n 's/^ *SSID: //p'"
        elif self.system == "win32":
            command = "netsh wlan show interfaces | findstr SSID"
        output = self.getresult(command, True)
        return output

    def decoderesult(self, output, flag=False):
        try:
            if sys.version_info[0] == 3:
                output = output.decode()
            if flag is True:
                output = output[0:output.find("\n")]
            output = output.strip('\r|\n')
            if output != "":
                output = output.replace(" ", '')
                output = output[output.find(":") + 1:]
            output = output[output.find("=") + 1:]
            return output
        except Exception as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
            sys.exit(2)


def main():
    '''A cross platform CLI tool to get connected wifi network\'s password.'''
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('wifi_name', nargs='?',
                            help="Name of the WIFI Network", type=str)
        args = parser.parse_args()
        ob = WifiPassword()
        wifiName = args.wifi_name
        output = ""
        if wifiName is not None:
            output = ob.getpassword(wifiName)
        else:
            wifiName = ob.getprofile()
            if wifiName == "":
                print(Fore.RED + 'Either you are not connected to any network or' +
                      ' the system doesn\'t find any network' +
                      Style.RESET_ALL)
            else:
                output = ob.getpassword(wifiName)

        if output == "":
            print(Fore.RED + 'Profile "' + wifiName +
                  '" is not found on the system.' + Style.RESET_ALL)
        else:
            print(Fore.GREEN + 'Password for the network ' + Fore.YELLOW +
                  wifiName + ': ' + output + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + str(e) + Style.RESET_ALL)
        parser.print_help()
        sys.exit(2)


if __name__ == '__main__':
    main()
