import unittest
import sys

try:
    from wifiPassword.wifiPassword import WifiPassword
except ImportError as e:
    # try to add relative path to enable unit tests without global installed wifiPassword 
    sys.path.append("../")
    from wifiPassword.wifiPassword import WifiPassword



class TestWifiPassword(unittest.TestCase):
    """docstring for TestWifiPassword"""

    def setUp(self):
        self.obj = WifiPassword()
         
        # legacy remove on issue #2 acceptance
        if hasattr(self.obj, "decoderesult"):
            self.decode_func = self.obj.decoderesult 
        else:
            from wifiPassword.wifiPassword import decoderesult 
            self.decode_func = decoderesult
        
        # legacy remove on issue #2 acceptance
        if hasattr(self.obj, "getresult"):
            self.getres = self.obj.getresult
        else:
            from wifiPassword.wifiPassword import getresult 
            self.getres = getresult

    def test_wifi_password(self):
        pas = self.obj.getprofile()
        self.assertTrue(len(pas) > 0)
        self.assertIsNotNone(pas)

    def test_get_essid(self):
        out = self.obj.getprofile()
        self.assertIsNotNone(out)
        self.assertTrue(len(out) > 0)
        self.assertTrue(isinstance(out, str))

    def test_decode_multiline_to_one(self):
        out = self.decode_func("foo\nbla".encode("utf-8"), True)
        self.assertEqual(out, "foo")

    def test_decode_split_on_equal_operator(self):
        out = self.decode_func("mykey=myvalue".encode("utf-8"))
        self.assertEqual(out, "myvalue")
       
    def test_decode_remove_whitespaces(self):
        out = self.decode_func("hello example".encode("utf-8"))
        self.assertEqual(out, "helloexample")

    def test_getresult(self):
        cmd = "dir" if sys.platform == "win32" else "ls"
        out = self.getres(cmd)
        self.assertIsNotNone(out)
        self.assertTrue(len(out) > 0)


if __name__ == '__main__':
    unittest.main()
