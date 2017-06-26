import unittest
from wifiPassword.wifiPassword import WifiPassword


class TestWifiPassword(unittest.TestCase):
    """docstring for TestWifiPassword"""

    def test_wifi_password(self):
        ob = WifiPassword()
        pas = ob.getpassword("ankit")
        self.assertEqual(pas, "Password for the network ankit: jain1234")

if __name__ == '__main__':
    unittest.main()
