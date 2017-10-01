import argparse
import subprocess
import sys
import os
from colorama import Fore, Style, init
init()

'''
    Author: Ankit Jain
    Email: ankitjain28may77@gmail.com
'''

def decoderesult(output, flag=False):
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

def getresult(command, flag=False):
    output, _ = subprocess.Popen(
        command, stdout=subprocess.PIPE,
        stderr=None,
        shell=True
    ).communicate()
    output = decoderesult(output, flag)
    return output



class BaseExtractor:
    cmd_tmpl = None 
    def _handle_result(self, res):
        try:
            return getresult(res)
        except Exception as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
            sys.exit(2)

    @classmethod
    def is_applicable(cls):
        raise NotImplementedError()

    def get_password(self, wifi_name):
        out = self.cmd_tmpl.format(essid=wifi_name)
        return self._handle_result(out)

class LinuxNetworkManagerExtractor(BaseExtractor):
    netman_path = "/etc/NetworkManager/system-connections/"
    cmd_tmpl = "sudo cat " + netman_path + "{essid} | grep psk="

    @classmethod
    def is_applicable(cls):
        return sys.platform in ["linux", "linux2"] and os.path.exists(cls.netman_path)

class LinuxNetctlExtractor(BaseExtractor):
    netctl_path = "/etc/netctl/"
    cmd_tmpl = "sudo cat " + netctl_path + "*{essid}* | grep Key | cut -f 2 -d \"=\""

    @classmethod 
    def is_applicable(cls):
        return sys.platform in ["linux", "linux2"] and os.path.exists(cls.netctl_path)

class MacExtractor(BaseExtractor):
    cmd_tmpl = "security find-generic-password -D\"AirPort network password\" -a {essid} -g"

    @classmethod
    def is_applicable(cls):
        return sys.platform == "darwin"

class WindowsExtractor(BaseExtractor):
    cmd_tmpl = "netsh wlan show profile name={essid} key=clear | findstr Key"

    @classmethod
    def is_applicable(cls):
        return sys.platform == "win32"

class WifiPassword:
    avail_extractors = [
        MacExtractor, WindowsExtractor, 
        LinuxNetctlExtractor, LinuxNetworkManagerExtractor
    ]

    def __init__(self):
        self.system = sys.platform
        self.wifiName = None 
 
        self.extractor = None
        for ext in self.avail_extractors:
            if ext.is_applicable():
                self.extractor = ext()
                break

    def usage(self):
        usage = """
usage: wifiPassword.py [-h] [wifi_name]

positional arguments:
    wifi_name   Name of the WIFI Network

optional arguments:
    -h, --help  show this help message and exit
            """
        print(usage)

    def getpassword(self, name):
        self.wifiName = name
        return self.extractor.get_password(self.wifiName)
       
    def getprofile(self):
        if self.system == "linux" or self.system == "linux2":
            command = "iwgetid -r"
        elif self.system == "darwin":
            command = ""
        elif self.system == "win32":
            command = "netsh wlan show interfaces | findstr SSID"
        output = getresult(command, True)
        return output

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
