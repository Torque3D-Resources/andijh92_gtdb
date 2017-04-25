import unittest
import wx
from gtdb.Config import *
# I cannot use 'import *' here. Otherwise I get an error in gtdb/Util.py .
import gtdb.App


class TestMyApp(unittest.TestCase):

    def setUp(self):

        gtdb.App.app = gtdb.App.MainApp(0)

    def tearDown(self):

        wx.CallAfter(gtdb.App.app.Exit)
        gtdb.App.app.MainLoop()

    def testConnectMenu(self):

        gtdb.App.app.frame.OnMenu_OpenLaunch(TESTSDIR+'/data/testing.gtdb')
        gtdb.App.app.frame.OnMenu_Start(True)
        assert gtdb.App.app.frame.host

if __name__ == '__main__':
    unittest.main()
