import unittest
from wifiPassword.wifiPassword import WifiPassword


class TestWifiPassword(unittest.TestCase):
    """docstring for TestWifiPassword"""

    def test_wifi_password(self):
        ob = WifiPassword()
        system = ob.system
        self.assertEqual(system, "linux")

if __name__ == '__main__':
    unittest.main()
