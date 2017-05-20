import wx
import gtdb.App
import gtdb.Util

class SecWarningDlg(wx.Dialog):

    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.SetTitle("Security Warning")
        mainVBox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        msg = """Attention: Starting a game with gtdb using an untrusted *.gtdb file can lead to the execution of malicious code!"""
        stext = wx.StaticText(self, -1, msg)
        self.cbox = wx.CheckBox(self, -1, "Remember and don't show this warning again.")
        btOk = wx.Button(self, wx.ID_OK, "OK")
        btCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        mainVBox.Add(stext, 1, wx.EXPAND | wx.ALL, border=5)
        mainVBox.Add(self.cbox, 0, wx.LEFT, border=5)
        mainVBox.Add(hbox, 0, wx.ALL | wx.ALIGN_RIGHT, border=5)

        hbox.Add(btCancel, 0, wx.ALL, border=5)
        hbox.Add(btOk, 0, wx.ALL, border=5)

        self.SetSizer(mainVBox)

        self.Bind(wx.EVT_BUTTON, self.onOK, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

    def onOK(self, evt):

        if self.cbox.IsChecked():
            gtdb.App.settings['hideSecWarnDlg'] = 'y'
            gtdb.Util.dumpSettings()
        self.Destroy()

    def onCancel(self, evt):

        self.Destroy()

if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    dlg = SecWarningDlg(None, -1)
    app.SetTopWindow(dlg)
    dlg.Show()
    app.MainLoop()
