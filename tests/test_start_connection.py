import unittest
import wx
from gtdb.Config import *
from gtdb.App import *


class TestMyApp(unittest.TestCase):

    def setUp(self):

        self.app = MainApp(0)

    def tearDown(self):

        wx.CallAfter(self.app.Exit)
        self.app.MainLoop()

    def testConnectMenu(self):

        self.app.frame.OnMenu_OpenLaunch(TESTSDIR+"/data/testing.TDebug")

        self.app.frame.OnMenu_Start(True)

        assert self.app.frame.host

if __name__ == '__main__':
    unittest.main()
