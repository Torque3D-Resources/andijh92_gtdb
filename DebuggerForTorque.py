#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Debugger for Torque , more information http://www.garagegames.com/products/torque/tge/.
Copyright (C) 2007....philippe.cain@orange.fr, more information http://eviwo.free.fr/torque/Debugger-documentation.html

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.....See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA.... 02110-1301, USA.
"""

import wx
import sys
import os
import os.path
import threading
import time
import telnetlib
import socket
import wx.lib.hyperlink

# init of the libray path

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'lib'))

from TorqueConnectV1_02 import *
from TorqueConsoleV1_02 import *
from TorqueEditorV1_03 import *

# from TorqueMapV01................................import *

from TorqueNotebookV1_02 import *
from TorqueMenuV1_03 import *
from TorqueSplashV01 import *
from TorqueToolBarV1_02 import *
from TorqueTreeV05 import *

from TorqueParametersV02 import *
from TorqueUtilV03_01 import *

_ = lang()

EVT_TORQUE_TELNET_ID = wx.NewId()


def EVT_TORQUE_TELNET(win, func):
    win.Connect(-1, -1, EVT_TORQUE_TELNET_ID, func)


class MainFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, -1, title=_('torqueDebug'),
                          size=(800, 600))

# ----------- COMMON VARIABLES ----------------------------------------------

        self.fileLoad = ''  # full name of the file loaded into the editor
        self.fileTorque = ''  # full name of the file loaded into the editor
        self.parameters = {}  # contains all the users environment
        self.projectSave = True  # manage the environment save
        self.worker = None  # thread
        self.host = None  # Telnet application
        self.server = CONNECT_LOCALH  # Telnet default parameters
        self.port = CONNECT_PORT
        self.password = CONNECT_PWD
        self.timerInterval = 0.5  # the thread to read the port is launched every timeInterval
        self.fickey = {}  # list of keyword for lexer

# -------------------------------------------------------------------------------
# ........ MENU & GUI DECALARATION AND EVENTS
# -------------------------------------------------------------------------------

        # ----------- WINDOW --------------------------------------------------------

        self.Bind(wx.EVT_CLOSE, self.OnMenu_Exit)

        # ----------- Torque telnet -------------------------------------------------....

        EVT_TORQUE_TELNET(self, self.OnResult)

        # ----------- MENU ----------------------------------------------------------

        self.menu = Menu(mainFrame=self)
        self.SetMenuBar(self.menu)

        self.Bind(wx.EVT_MENU, self.OnMenu_Open, self.menu.Menu_Open)
        self.Bind(wx.EVT_MENU, self.OnMenu_Connect,
                  self.menu.Menu_Connect)
        self.Bind(wx.EVT_MENU, self.OnMenu_Save, self.menu.Menu_Save)
        self.Bind(wx.EVT_MENU, self.OnMenu_Close, self.menu.Menu_Close)
        self.Bind(wx.EVT_MENU, self.OnMenu_SaveText,
                  self.menu.Menu_SaveText)
        self.Bind(wx.EVT_MENU, self.OnMenu_Exit, self.menu.Menu_Exit)

        self.Bind(wx.EVT_MENU, self.OnMenu_Break, self.menu.Menu_Break)
        self.Bind(wx.EVT_MENU, self.OnMenu_RemAllBreak,
                  self.menu.Menu_RemAllBreak)
        self.Bind(wx.EVT_MENU, self.OnMenu_ListeEngine,
                  self.menu.Menu_ListeEngine)

# ........self.Bind(wx.EVT_MENU, self.OnMenu_Preference........, self.menu.Menu_Preference)

        self.Bind(wx.EVT_MENU, self.OnMenu_Help, self.menu.Menu_Help)
        self.Bind(wx.EVT_MENU, self.OnMenu_Credits,
                  self.menu.Menu_Credits)

        self.Bind(wx.EVT_MENU_RANGE, self.OnFileHistory,
                  id=wx.ID_FILE1, id2=wx.ID_FILE9)

        # ----------- TOOL BAR ------------------------------------------------------

        self.toolBar = Tool(self, -1, mainFrame=self)
        self.SetToolBar(self.toolBar)

        self.Bind(wx.EVT_TOOL, self.OnMenu_Start,
                  self.toolBar.Tool_Start)
        self.Bind(wx.EVT_TOOL, self.OnMenu_Stop, self.toolBar.Tool_Stop)
        self.Bind(wx.EVT_TOOL, self.OnMenu_Pause,
                  self.toolBar.Tool_Pause)
        self.Bind(wx.EVT_TOOL, self.OnMenu_StepIn,
                  self.toolBar.Tool_StepIn)
        self.Bind(wx.EVT_TOOL, self.OnMenu_RunCurs,
                  self.toolBar.Tool_RunCurs)
        self.Bind(wx.EVT_TOOL, self.OnMenu_StepOver,
                  self.toolBar.Tool_StepOver)
        self.Bind(wx.EVT_TOOL, self.OnMenu_StepOut,
                  self.toolBar.Tool_StepOut)
        self.Bind(wx.EVT_TOOL, self.OnMenu_SaveText,
                  self.toolBar.Tool_SaveText)
        self.Bind(wx.EVT_TOOL, self.OnMenu_Dump, self.toolBar.Tool_Dump)

        # ----------- SPLIT AREA ----------------------------------------------------

        splitterv = wx.SplitterWindow(self, wx.SP_3D | wx.SP_BORDER)
        splitterh = wx.SplitterWindow(splitterv, wx.SP_3D
                | wx.SP_BORDER)

        # editor

        self.editor = PythonSTC(splitterh, -1, mainFrame=self)
        self.Bind(wx.stc.EVT_STC_MARGINCLICK, self.OnMarginClick)

        # notebook

        self.nboo = NoteList(splitterv, -1, mainFrame=self)
        self.nboo.list_breakPoint.Bind(wx.EVT_LIST_ITEM_SELECTED,
                self.OnItemSelected_breakPoint)
        self.nboo.list_callStack.Bind(wx.EVT_LIST_ITEM_SELECTED,
                self.OnItemSelected_callStack)
        self.nboo.list_logCompile.Bind(wx.EVT_LIST_ITEM_SELECTED,
                self.OnItemSelected_logCompile)
        self.nboo.list_watchValue.Bind(wx.EVT_LIST_ITEM_SELECTED,
                self.OnItemSelected_watchValue)

        # tree

        self.tree = TreePgm(splitterh, -1, mainFrame=self)
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClickTree)

        # repartition screen

        splitterh.SplitVertically(self.editor, self.tree)
        splitterv.SplitHorizontally(splitterh, self.nboo)

        # adjustement of the different screen

        def SplitterOnSizeV(evt):
            splitter = evt.GetEventObject()
            sz = splitter.GetSize()
            splitter.SetSashPosition(sz.height - 200, False)
            evt.Skip()

        def SplitterOnSizeH(evt):
            splitter = evt.GetEventObject()
            sz = splitter.GetSize()
            splitter.SetSashPosition(sz.width - 250, False)
            evt.Skip()

        splitterh.Bind(wx.EVT_SIZE, SplitterOnSizeH)
        splitterv.Bind(wx.EVT_SIZE, SplitterOnSizeV)

        # ----------- STATUS BAR ----------------------------------------------------

        self.CreateStatusBar()
        self.SetStatusText(_('_welcome'))

        # ----------- INITIALISATION ------------------------------------------------

        self.menu.fileHistoryLoad()
        self.menu.initLexer()

        # ----------- Spash screen --------------------------------------------------

        splash = MySplashScreen()
        splash.Show()

        # ----------- DISPLAY -------------------------------------------------------

        self.CenterOnScreen()
        self.GetBestSize()
        self.Show()

        # test
        # MyTorqueMap().load('/home/philippe/Projects/boomboom152/game/data/missions/Map1.mis')

# -------------------------------------------------------------------------------
# ........ FUNCTIONS LAUNCHED BY EVENTS WHICH COME FROM MENU
# -------------------------------------------------------------------------------........

    def OnFileHistory(self, evt):

        # get the file based on the menu ID and load the debugger environment

        fileNum = evt.GetId() - wx.ID_FILE1
        path = self.menu.filehistory.GetHistoryFile(fileNum)
        self.OnMenu_OpenLaunch(path)

    def OnItemSelected(self, fil, lig):

        # display in the tewt windows the file and lign correponding to the selection

        self.SetStatusText('')
        if fil:
            fic = os.path.join(self.menu.getEnvDir(), fil)
            self.fileLoad = fic
            self.fileTorque = fil
            self.editor.load(fic, fil, lig)
        else:
            self.SetStatusText(_('_no-file-lign'))

        self.SetStatusText(_('_current-file') + ' '
                           + str(self.fileTorque))

    def OnItemSelected_breakPoint(self, event):

        # manage the break point selection

        (fil, lig, col3, col4) = \
            self.nboo.list_breakPoint.GetFileLign(event.m_itemIndex)
        self.OnItemSelected(fil, lig)

    def OnItemSelected_callStack(self, event):

        # manage the call stack selection

        (fil, lig, col3, col4) = \
            self.nboo.list_callStack.GetFileLign(event.m_itemIndex)
        self.OnItemSelected(fil, lig)

    def OnItemSelected_logCompile(self, event):

        # manage the errors compilation selection

        (fil, lig, col3, col4) = \
            self.nboo.list_logCompile.GetFileLign(event.m_itemIndex)
        self.OnItemSelected(fil, lig)

    def OnItemSelected_watchValue(self, event):

        # manage the value selection

        (fil, lig, col3, col4) = \
            self.nboo.list_watchValue.GetFileLign(event.m_itemIndex)
        self.OnItemSelected(fil, lig)

    def OnLeftDClickTree(self, event):

        # manage the file selection in the tree

        (fil, node) = self.tree.getNodeTreePgm(event)
        self.fileLoad = ''
        self.fileTorque = ''
        if fil:
            self.fileLoad = fil
            self.fileTorque = node
            if node.endswith('.mis'):
                torqueMap = MyTorqueMap()
                torqueMap.load(fil)
            else:
                self.editor.load(fil, node)

    def OnMarginClick(self, event):

        # Manage the clicj in the margin of the text. The margin is between the number and the text

        self.SetStatusText('')
        message = self.editor.OnMarginClickEditor(event)
        self.projectSave = False
        self.SetStatusText(message)

    def OnMenu_Break(self, event):

        # display a information screen : how to do a break point

        MsgDlg(self, _('_message-break-lib'), _('_message-break'),
               wx.OK | wx.ICON_INFORMATION)

    def OnMenu_Close(self, event):

        # manage the close menu operation

        self.save()
        self.OnMenu_CloseLaunch()

    def OnMenu_Connect(self, event):

        # manage the concetion GUI

        dlg = ConnectPanel(
            self,
            -1,
            _('_connect-dialog'),
            size=(530, 330),
            style=wx.DEFAULT_DIALOG_STYLE,
            mainFrame=self,
            )
        dlg.CenterOnScreen()
        self.projectSave = False

    def OnMenu_Dump(self, event):
        val = self.nboo.list_watchValue.GetFocusedItem()
        (fil, lig, col3, col4) = \
            self.nboo.list_watchValue.GetFileLign(val)
        identifier = fil + '|' + lig + '|' + col3

# ........lig = self.editor.GetSelectedText()

        if col4:

            # self.Continue()
            # lig = str("CEVAL commandToServer('DebugDump'," + col4 + ");\n")

            self.nboo.list_logDump.reset()
            self.nboo.list_logDisplay.dump = True
            lig = str('EVAL STARTDUMP|' + identifier + ' 0 ' + col4
                      + '.dump()' + '\r\n')
            self.host.write(lig)
            lig = str('EVAL ENDDUMP' + ' 0 ' + col3 + '\r\n')
            self.host.write(lig)

    def OnMenu_Exit(self, event):

        # manage the window close or exit menu

        self.save()
        self.OnMenu_CloseLaunch()
        self.menu.fileHistorySave()
        self.Destroy()

    def OnMenu_Open(self, event):

        # manage the open of a debugger parameters file

        dlg = wx.FileDialog(
            self,
            message=_('_ChooseFile'),
            defaultDir=getHomeUser(),
            defaultFile='',
            wildcard=_('_Debug-Environment') + ' *.TDebug |*.TDebug',
            style=wx.OPEN | wx.CHANGE_DIR,
            )

        if dlg.ShowModal() == wx.ID_OK:

                # This returns a Python list of files that were selected.

            path = dlg.GetPath()
            self.OnMenu_OpenLaunch(path)

        dlg.Destroy()

    def OnMenu_ListeEngine(self, event):
        path = self.menu.getParameter(DIR_ENGINE)
        if os.path.isdir(path):
            self.consoleURL = ExtractEngine(path).getReportUrl()
            if self.consoleURL:
                self.consoleLink = wx.lib.hyperlink.HyperLinkCtrl(self,
                        wx.ID_ANY, '', URL=self.consoleURL)
                self.consoleLink.GotoURL(self.consoleURL, True, True)
                self.SetStatusText(_('_consoleUrl-OK'))
            else:
                self.SetStatusText(_('_consoleUrl-KO'))
        else:
            self.SetStatusText(_('_dirEngine-KO'))

# ....def OnMenu_Preference(self,event):

# ........dlg = Preference(self, -1, _("_Preference-dialog"), size=(500,330),
# ........................................ style = wx.DEFAULT_DIALOG_STYLE,
# ........................................ mainFrame=self)
# ........dlg.CenterOnScreen()
# ........self.PreferenceSave = False

    def OnMenu_Help(self, event):

        # Manage the display of the help menu in an internet browser

        link = wx.lib.hyperlink.HyperLinkCtrl(self, wx.ID_ANY, '',
                URL=URL)
        link.GotoURL(URL, True, True)
        link.Destroy()
        MsgDlg(self, _('_message-consultSite-lib'),
               _('_message-consultSite'), wx.OK | wx.ICON_INFORMATION)

    def OnMenu_Credits(self, event):

        # manage the display of the credits

        splash = MySplashScreen()
        splash.Show()

    def OnMenu_Save(self, event):

        # manage the save of the debugger parameters file

        self.menu.saveEnv()
        self.projectSave = True

    def OnResult(self, event):

        # manage the information received form Torque inorder to debug
        # and relaunch the thread every 'seconds'

        if event.data is None:

                # Thread aborted (using our convention of None return)

            self.SetStatusText(_('_thread-Aborted'))
            self.OnMenu_Stop(-1)
        else:

                # Process results here

            if event.data:
                self.nboo.list_logDisplay.append(event.data)

        if self.host:
            self.worker = Timer(self, self.timerInterval, self.host)
            self.worker.start()

# -------------------------------------------------------------------------------
# ........ FUNCTIONS LAUNCHED BY EVENTS WHICH COME FROM TOOLBAR
# -------------------------------------------------------------------------------........

    def OnMenu_Pause(self, event):

        # manage the pause action to launch during debugging activity

        self.host.write('BRKNEXT\r\n')

    def OnMenu_SaveText(self, event):
        self.editor.saveText(False)

    def OnMenu_Start(self, event):

        # manage the start debugging action in order to launch the debugger

        self.nboo.resetNoteDebug()
        if launchTorque(self.menu):
            error = 'go'
            xx_time = int(time.time() + 10)
            while error:
                if time.time() > xx_time:
                    error = _('_errorLaunchTorque')
                    break
                error = self.Start()

            if error:
                MsgDlg(self, error, _('_errorTelnet-lib'), wx.ICON_HAND)
            else:
                self.SetStatusText(_('_telnetOK'))
                self.toolBar.enable(True)
                self.toolBar.enableStart(False)
                self.menu.enableToolMenu(True)
                self.menu.enableToolMenuStart(True)
        else:
            MsgDlg(self, error, _('_errorconnect-lib'), wx.ICON_HAND)

    def OnMenu_StepIn(self, event):

        # manage the set in action to launch during debugging activity

        self.host.write('STEPIN\r\n')

    def OnMenu_Stop(self, event):

        # manage the stop action to stop the debugger and torque

        self.Stop()
        self.toolBar.enable(False)
        self.toolBar.enableStart(True)
        self.menu.enableToolMenuStart(False)

    def OnMenu_RunCurs(self, event):

        # manage the continue action to launch during debugging activity

        self.Continue()
        self.nboo.list_logDisplay.firstTime = True

    def OnMenu_StepOver(self, event):

        # manage the step over action to launch during debugging activity

        self.host.write('STEPOVER\r\n')

    def OnMenu_StepOut(self, event):

        # manage the step out action to launch during debugging activity

        self.host.write('STEPOUT\r\n')

    def OnMenu_RemAllBreak(self, event):

        # manage the remove of all the break points

        self.Continue()
        self.host.write('BRKCLRALL\r\n')
        self.nboo.list_breakPoint.reset()

# -------------------------------------------------------------------------------
# ........ COMMON FUNCTIONS
# -------------------------------------------------------------------------------

    def OnMenu_CloseLaunch(self):

        # manage all the actions to perform when a close action of the debugger parameters file is requested

        self.Stop()
        self.editor.reset()
        self.tree.resetTree()
        self.nboo.resetNoteList()
        self.menu.resetDebug()
        self.toolBar.enable(False)
        self.menu.enableMenu(False)
        self.menu.enableToolMenuStart(False)
        self.toolBar.enableSave(False)  # V2.4 because of trigger OnModified
        self.menu.enableMenuSaveText(False)
        self.SetTitle(_(APPLICATION))

    def OnMenu_OpenLaunch(self, path):

        # manage all the actions to perform when an open action of debugger parameters file is requested

        if os.path.isfile(path):
            self.OnMenu_CloseLaunch()
            if not self.menu.initEnv(path):
                MsgDlg(self, _('_error-load-env') + '\n'
                       + dlg.GetPath(), _('_error-lib'), wx.ICON_HAND)
            else:
                self.toolBar.enableStart(True)
                self.menu.enableInit(True)
                self.nboo.list_breakPoint.init('break')
                self.menu.filehistory.AddFileToHistory(path)
                self.tree.loadDirInTree()
                fil = str(self.fileLoad)
                self.fileTorque = fil[len(self.menu.getEnvDir()) + 1:]
                self.menu.setDebug()
                self.editor.load(self.fileLoad, self.fileTorque)
                self.menu.enableInit(True)
                self.menu.enableToolMenu(True)
                self.menu.enableToolMenuStart(False)

    def Continue(self):
        self.toolBar.enableDebug(False)
        self.editor.MarkerDelete(self.nboo.list_logDisplay.marker, 2)
        self.host.write('CONTINUE\r\n')

    def Start(self):

        # manage the start of the debugger thread

        self.nboo.list_logDisplay.reset()

        if not self.host:
            try:
                self.host = telnetlib.Telnet(self.server, self.port)
                self.host.write(self.password + '\n')
            except socket.error, msg:
                pass
                return _('_errorSocket') + '\n' \
                    + 'telnetTorque.Start\n' + str(msg)

            try:
                self.worker = Timer(self, self.timerInterval, self.host)
                self.worker.start()
            except error, msg:
                return _('_errorThread') + '\n' \
                    + 'telnetTorque.Start\n' + str(msg)

            return None

        return _('_alwaysConnected')

    def Stop(self):

        # manage the stop oh the debugger thread and game

        if self.host:
            try:
                self.Continue()
                self.host.write('CEVAL quit();\n')
                time.sleep(2)
                self.nboo.list_logDisplay.firstTime = True
            except socket.error:
                pass
            else:
                self.host.close()
            self.host = None

        self.editor.MarkerDelete(self.nboo.list_logDisplay.marker, 2)

    def save(self):

        # manage the save of the debugger parameters file

        if not self.projectSave:
            self.projectSave = True
            result = MsgDlg(self, _('_projectChanged'), _('_warning'),
                            wx.YES_NO)
            if result == wx.ID_YES:
                self.menu.saveEnv()


class Timer(threading.Thread):

        # thread declaration

    def __init__(
        self,
        window,
        seconds,
        host,
        ):
        self.window = window
        self.host = host
        self.runTime = seconds
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(self.runTime)
        lign = None
        if self.host:
            try:
                lign = self.host.read_very_eager()
            except:
                pass
        try:
            wx.PostEvent(self.window, ResultEvent(lign))
        except:
            pass


class ResultEvent(wx.PyEvent):

    # event launched by the Thread....

    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_TORQUE_TELNET_ID)
        self.data = data


class MainApp(wx.App):

    def OnInit(self):

        self.frame = MainFrame(None, -1)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True


if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()
