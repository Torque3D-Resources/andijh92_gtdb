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

        assert self.app.frame.parameters["engine"] == ""
        assert self.app.frame.parameters["directoryGame"] == "/home/andijh92/src/Uebergame-andijh92/Uebergame"
        assert self.app.frame.parameters["unixPara"] == ""
        assert self.app.frame.parameters["fileScript"] == "main.cs"
        assert self.app.frame.parameters["break"] == []
        assert self.app.frame.parameters["pwd"] == "password"
        assert self.app.frame.parameters["port"] == "6000"
        assert self.app.frame.parameters["localhost"] == "127.0.0.1"
        assert self.app.frame.parameters["fileBinary"] == "Uebergame"

if __name__ == '__main__':
    unittest.main()
