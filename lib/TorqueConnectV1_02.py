#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Debugger for Torque , more information http://www.garagegames.com/products/torque/tge/.
Copyright (C) 2007  philippe.cain@orange.fr, more information http://eviwo.free.fr/torque/Debugger-documentation.html

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import wx
import os.path
import os

from TorqueParametersV02 import *
from TorqueUtilV03_01 import *
_ = lang()


class ConnectPanel(wx.Dialog):

    def __init__(
        self,
        parent,
        ID,
        title,
        size=wx.DefaultSize,
        pos=wx.DefaultPosition,
        style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
        mainFrame=0,
        ):
        wx.Dialog.__init__(
            self,
            parent,
            -1,
            title,
            pos,
            size,
            style,
            )

        self.mainFrame = mainFrame

        large = 200
        height = 30

        # directory game

        l1 = wx.StaticText(self, -1, _('_dir_game-lib'))
        self.t1 = wx.TextCtrl(self, -1, '', size=(large, height))
        b1 = wx.Button(self, -1, _('_browse'), size=(-1, height))
        self.Bind(wx.EVT_BUTTON, self.browseGameDir, b1)

        # torque script main file

        l2 = wx.StaticText(self, -1, _('_file_script-lib'))
        self.t2 = wx.TextCtrl(self, -1, '', size=(large, height))
        b2 = wx.Button(self, -1, _('_browse'), size=(-1, height))
        self.Bind(wx.EVT_BUTTON, self.browseTorqueScript, b2)

        # exe or bianry file of the game

        l3 = wx.StaticText(self, -1, _('_file_binary-lib'))
        self.t3 = wx.TextCtrl(self, -1, '', size=(large, height))
        b3 = wx.Button(self, -1, _('_browse'), size=(-1, height))
        self.Bind(wx.EVT_BUTTON, self.browseBinary, b3)

        # parameter to use by the binary or exe file

        l5 = wx.StaticText(self, -1, _('_unix_para-lib'))
        self.t5 = wx.TextCtrl(self, -1, '', size=(large, height))

        # port to connect

        l6 = wx.StaticText(self, -1, _('_port-lib'))
        self.t6 = wx.TextCtrl(self, -1, '', size=(large, height))

        # password

        l7 = wx.StaticText(self, -1, _('_pwd-lib'))
        self.t7 = wx.TextCtrl(self, -1, '', size=(large, height))

        # host ip address

        l8 = wx.StaticText(self, -1, _('_host-lib'))
        self.t8 = wx.TextCtrl(self, -1, '', size=(large, height))

        # directory engine lib

        l9 = wx.StaticText(self, -1, _('_dir_engine-lib'))
        self.t9 = wx.TextCtrl(self, -1, '', size=(large, height))
        b9 = wx.Button(self, -1, _('_browse'), size=(-1, height))
        self.Bind(wx.EVT_BUTTON, self.browseEngineDir, b9)

        ok = wx.Button(self, wx.ID_OK, _('_ok-lib'), size=(-1, height))
        self.Bind(wx.EVT_BUTTON, self.okMenu, ok)

        cancel = wx.Button(self, wx.ID_CANCEL, _('_cancel-lib'),
                           size=(-1, height))
        self.Bind(wx.EVT_BUTTON, self.cancelMenu, cancel)

        # gui arrangement

        sizer = wx.FlexGridSizer(cols=3, hgap=0, vgap=0)
        sizer.AddMany([
            l1,
            self.t1,
            b1,
            l2,
            self.t2,
            b2,
            l3,
            self.t3,
            b3,
            l5,
            self.t5,
            (0, 0),
            l8,
            self.t8,
            (0, 0),
            l6,
            self.t6,
            (0, 0),
            l7,
            self.t7,
            (0, 0),
            l9,
            self.t9,
            b9,
            (20, 20),
            (20, 20),
            (20, 20),
            cancel,
            (0, 0),
            ok,
            ])
        border = wx.BoxSizer(wx.BOTH)
        border.Add(sizer, 0, wx.ALL, 25)
        self.SetSizer(border)
        self.SetAutoLayout(True)

        # initialisation of the GUI fileds

        self.t1.SetValue(self.mainFrame.menu.getParameter(GAME_DIRECTORY))

        if self.mainFrame.menu.getParameter(GAME_DIRECTORY):

            # if a debugger parameters file has been loaded previously display what is loaded

            self.t2.SetValue(self.mainFrame.menu.getParameter(GAME_FILESCRIPT))
            self.t3.SetValue(self.mainFrame.menu.getParameter(GAME_FILEBINARY))
            self.t5.SetValue(self.mainFrame.menu.getParameter(GAME_UNIXPARA))
            self.t6.SetValue(self.mainFrame.menu.getParameter(GAME_PORT))
            self.t7.SetValue(self.mainFrame.menu.getParameter(GAME_PWD))
            self.t8.SetValue(self.mainFrame.menu.getParameter(GAME_LOCALHOST))
            self.t9.SetValue(self.mainFrame.menu.getParameter(DIR_ENGINE))
        else:

            # if nothing has been loaded previously : display default parameters

            self.t2.SetValue(self.mainFrame.menu.getParameter(GAME_FILESCRIPT,
                             CONNECT_MAIN))
            self.t3.SetValue(self.mainFrame.menu.getParameter(GAME_FILEBINARY,
                             CONNECT_BINARY))
            self.t5.SetValue(self.mainFrame.menu.getParameter(GAME_UNIXPARA,
                             CONNECT_PARA))
            self.t6.SetValue(self.mainFrame.menu.getParameter(GAME_PORT,
                             CONNECT_PORT))
            self.t7.SetValue(self.mainFrame.menu.getParameter(GAME_PWD,
                             CONNECT_PWD))
            self.t8.SetValue(self.mainFrame.menu.getParameter(GAME_LOCALHOST,
                             CONNECT_LOCALH))
            self.t9.SetValue(self.mainFrame.menu.getParameter(DIR_ENGINE,
                             ''))

        self.GetBestSize()
        self.Show()

    def browseGameDir(self, event):

        # selection of the directory

        dlg = wx.DirDialog(self, _('_choose_dir-lib'),
                           style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.t1.SetValue(dlg.GetPath())

        dlg.Destroy()

    def browseEngineDir(self, event):

        # selection of the directory

        dlg = wx.DirDialog(self, _('_choose_dir-lib'),
                           style=wx.DD_DEFAULT_STYLE)

        if dlg.ShowModal() == wx.ID_OK:
            self.t9.SetValue(dlg.GetPath())

        dlg.Destroy()

    def browseGameFile(self):

        # selection of the file

        val = ''
        dlg = wx.FileDialog(self, _('_choose_file-lib'),
                            style=wx.DD_DEFAULT_STYLE,
                            defaultDir=self.t1.GetValue())

        if dlg.ShowModal() == wx.ID_OK:
            val = os.path.basename(dlg.GetPath())

        dlg.Destroy()

        return val

    def browseGameDirFile(self):

        # selection of the file

        val = ''
        dlg = wx.FileDialog(self, _('_choose_file-lib'),
                            style=wx.DD_DEFAULT_STYLE,
                            defaultDir=self.t1.GetValue())

        if dlg.ShowModal() == wx.ID_OK:
            val = dlg.GetPath()

        dlg.Destroy()

        return val

    def browseTorqueScript(self, event):

        # selection of torque script

        self.t2.SetValue(self.browseGameFile())

    def browseMission(self, event):

        # selection of mission

        self.t5_1.SetValue(self.browseGameDirFile())

    def browseBinary(self, event):

        # selection of the binary game

        self.t3.SetValue(self.browseGameFile())

    def cancelMenu(self, event):
        self.Destroy()

    def okMenu(self, event):

        # control the information fullfil in the GUI

        error = ''

        # directory is mandatory

        fil = self.t1.GetValue()
        if os.path.isdir(fil):
            self.mainFrame.menu.setParameter(GAME_DIRECTORY, fil)
        else:
            error = error + _('_dir_game-lib') + ' : ' + _('_Mandatory'
                    ) + '\n'

        # torque script is mandatory

        x = self.t2.GetValue()
        if os.path.isfile(os.path.join(self.t1.GetValue(), x)):
            self.mainFrame.menu.setParameter(GAME_FILESCRIPT, x)
        else:
            error = error + _('_file_script-lib') + ' : ' \
                + _('_Mandatory') + '\n'

        # binary or exe file is mandatory

        x = self.t3.GetValue()
        if os.path.isfile(os.path.join(self.t1.GetValue(), x)):
            self.mainFrame.menu.setParameter(GAME_FILEBINARY, x)
        else:
            error = error + _('_file_binary-lib') + ' : ' \
                + _('_Mandatory') + '\n'

        # parameter for exe of binary file not mandatory

        x = self.t5.GetValue()
        if x:
            if x.find('-nohomedir') > -1 or x.find('-dedicated') > -1:
                self.mainFrame.menu.setParameter(GAME_UNIXPARA,
                        self.t5.GetValue())
            else:
                error = error + _('_unix_para-lib') + ' : ' \
                    + _('_debugWrong') + '\n'
        else:
            self.mainFrame.menu.setParameter(GAME_UNIXPARA, '')

        # address IP  is mandatory

        x = self.t8.GetValue()
        if x:
            self.mainFrame.menu.setParameter(GAME_LOCALHOST, x)
        else:
            error = error + _('_host-lib') + ' : ' + _('_Mandatory') \
                + '\n'

        # address port  is mandatory

        x = self.t6.GetValue()
        if x:
            self.mainFrame.menu.setParameter(GAME_PORT, x)
        else:
            error = error + _('_port-lib') + ' : ' + _('_Mandatory') \
                + '\n'

        # password is mandatory

        x = self.t7.GetValue()
        if x:
            self.mainFrame.menu.setParameter(GAME_PWD, x)
        else:
            error = error + _('_pwd-lib') + ' : ' + _('_Mandatory') \
                + '\n'

        # directory is mandatory

        fileng = self.t9.GetValue()
        if fileng:
            if os.path.isdir(fileng):
                self.mainFrame.menu.setParameter(DIR_ENGINE, fileng)
            else:
                error = error + _('_dir_engine-lib') + ' : ' \
                    + _('_unknown') + '\n'

        # dsiplay all the errors messages

        if error:
            MsgDlg(self, error, _('_error_connect-lib'), wx.ICON_HAND)
        else:
            pgm = str(self.mainFrame.menu.getParameter(GAME_FILEBINARY))
            tab = pgm.split('.')
            fil = os.path.join(fil, os.path.basename(fil) + '-'
                               + tab[0] + EXT_DEBUG)
            self.mainFrame.menu.setEnv(fil)
            self.mainFrame.menu.saveEnv()
            self.mainFrame.OnMenu_OpenLaunch(fil)

            self.Destroy()
