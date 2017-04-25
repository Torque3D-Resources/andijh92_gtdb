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
import json

from gtdb.Parameters import *
from gtdb.Util import *
from gtdb.Config import *

_ = lang()


class Menu(wx.MenuBar):

    def __init__(self, mainFrame=0):
        wx.MenuBar.__init__(self)

        # init name application use to save parameters of torque debugger

        wx.GetApp().SetAppName(APPLICATION)

# -------------------------------------------------------------------------------
# menu management
# -------------------------------------------------------------------------------

        self.mainFrame = mainFrame

        # Menu file

        Menu = wx.Menu()
        self.MenuFile = Menu

        self.Menu_Connect = Menu.Append(120, _('&_Connect'),
                _('_Connect-lib'))
        self.Menu_Open = Menu.Append(121, _('&_Open'), _('_Open-lib'))
        self.Menu_Save = Menu.Append(101, _('&_Save'), _('_Save-lib'))
        self.Menu_Close = Menu.Append(102, _('&_Close'), _('_Close-lib'
                ))

        Menu.AppendSeparator()

        self.Menu_SaveText = Menu.Append(110, _('&_SaveText'),
                _('_saveText-lib'))

        Menu.AppendSeparator()

        self.Menu_Exit = Menu.Append(500, _('&_Exit'), _('_Exit-lib'))

        self.Append(Menu, _('&_File'))

        self.filehistory = wx.FileHistory()
        self.filehistory.UseMenu(Menu)

        # menu Edit
# ........Menu = wx.Menu()

# ........self.Menu_Preference........= Menu.Append(-1 , _("&_Preference")................, _("_Preference-lib"))

# ........self.Append(Menu............, _("&_Edit"))

        # Menu debugger

        Menu = wx.Menu()
        self.MenuDebug = Menu

        self.Menu_Break = Menu.Append(116, _('&_Break'), _('_Break-lib'
                ))

        Menu.AppendSeparator()

        self.Menu_RemAllBreak = Menu.Append(117, _('&_RemAllBreak'),
                _('_RemAllBreak-lib'))

        Menu.AppendSeparator()

        self.Menu_ListeEngine = Menu.Append(118, _('&_listEngine'),
                _('_listEngine-lib'))

        self.Append(Menu, _('&_Debug'))

        # menu help

        Menu = wx.Menu()

        self.Menu_Help = Menu.Append(200, _('&_Help'), _('_Help-manual'
                ))
        self.Menu_Credits = Menu.Append(201, _('&_Credits'),
                _('_Credits'))

        Menu.AppendSeparator()

        self.Menu_PyRepl = Menu.Append(202, "GTDB Python Repl")

        self.Append(Menu, _('&_Help'))

        self.fileEnv = ''
        self.dirEnv = ''

        self.enableMenu(False)

    def enableMenu(self, status):

        # enable all menus

        self.enableInit(status)
        self.enableToolMenu(status)
        self.enableToolMenuStart(status)
        self.enableMenuSaveText(status)

    def enableInit(self, status):

        # enable the menu save and close and list engine

        self.MenuFile.Enable(101, status)
        self.MenuFile.Enable(102, status)
        self.MenuDebug.Enable(118, status)

    def enableToolMenu(self, status):

        # enable the menu add & delete break

        self.MenuDebug.Enable(116, status)

    def enableToolMenuStart(self, status):

        # enable the menu remove all break

        self.MenuDebug.Enable(117, status)

    def enableMenuSaveText(self, status):
        self.MenuFile.Enable(110, status)

# -------------------------------------------------------------------------------
# environement management
# -------------------------------------------------------------------------------

    def initEnv(self, fil):

        # intialise the debugger environement

        self.mainFrame.parameters = {}

        # put in memory the debugger parameters file choosen

        self.setEnv(fil)

        # laod all the parameters from this file

        if self.getEnvFile():
            inp = open(self.getEnvFile())
            try:
                self.mainFrame.parameters = json.load(inp)
            except:
                pass
                inp.close()
                self.mainFrame.parameters = {}
                self.mainFrame.SetStatusText(_('_errorReadEnv'))
                return False

            self.mainFrame.SetStatusText(_('_OKReadEnv'))
            inp.close()

        return True

    def initLexer(self):
        dire = os.path.join(DATADIR, DIR_LEXER)

        self.mainFrame.fickey = initFileLexer(os.path.join(dire, KEY1),
                getAppliFileName(KEY1), 1, self.mainFrame.fickey)
        self.mainFrame.fickey = initFileLexer(os.path.join(dire, KEY2),
                getAppliFileName(KEY2), 2, self.mainFrame.fickey)
        self.mainFrame.fickey = initFileLexer(os.path.join(dire, KEY3),
                getAppliFileName(KEY3), 3, self.mainFrame.fickey)
        self.mainFrame.fickey = initFileLexer(os.path.join(dire, KEY4),
                getAppliFileName(KEY4), 4, self.mainFrame.fickey)
        self.mainFrame.fickey = initFileLexer(os.path.join(dire, KEY5),
                getAppliFileName(KEY5), 5, self.mainFrame.fickey)

        inp = os.path.join(dire, STYLE)
        out = getAppliFileName(STYLE)

        if not os.path.isfile(out):
            try:
                shutil.copyfile(inp, out)
            except IOError:
                pass

    def getEnvFile(self):

        # return the debugger parameter file name

        return self.fileEnv

    def getEnvDir(self):

        # return the game directory

        return self.dirEnv

    def setEnv(self, fil):

        # save the game directory and the debugger parameter file name

        if fil:
            self.fileEnv = fil
            fil = os.path.dirname(fil)
            if fil:
                self.dirEnv = fil
                return True

        return False

    def saveEnv(self):

        # save the debugger environement : connection parameters in the game directory

        fil = self.getEnvFile()
        if fil:
            if os.path.exists(fil):
                os.unlink(fil)

            try:
                output = open(fil, 'w+')
                json.dump(self.mainFrame.parameters, output)
            except:
                output.close()
                self.mainFrame.parameters = {}
                self.mainFrame.SetStatusText(_('_errorSaveEnv'))
                return False

            self.mainFrame.SetStatusText(_('_OKSaveEnv'))
            output.close()
            return True

        return False

# -------------------------------------------------------------------------------
# debugger management : preparation torque scripts
# -------------------------------------------------------------------------------

    def setDebug(self):

        # intilise the torque main script file with the parameter needed by the debugger

        # get the torque main script file name

        dire = self.mainFrame.menu.getParameter(GAME_DIRECTORY)
        fil = self.mainFrame.menu.getParameter(GAME_FILESCRIPT)
        filec = os.path.join(dire, fil)
        filectmp = filec + '-tmp'

        # open , read and write the updated torque main script file

        nodebug = True
        try:
            if os.path.exists(filec):

                # all the lines with dbgsetparameters are put in comment ( several lines could block the debugger)

                inpute = open(filec)
                output = open(filectmp, 'w+')
                for line in inpute.readlines():
                    li = line
                    li = li.lower()
                    if li.find('dbgsetparameters') > -1:
                        output.write('//' + line)
                    else:
                        output.write(line)

                inpute.close()
                output.close()

                # the 2 first lines are automatically put by the debugger in order to set correctly the debugger

                inpute = open(filectmp)
                output = open(filec, 'w+')
                port = self.mainFrame.menu.getParameter(GAME_PORT)
                if not port:
                    port = CONNECT_PORT

                pwd = self.mainFrame.menu.getParameter(GAME_PWD)
                if not pwd:
                    pwd = CONNECT_PWD

                # torque wait until the connection is done by the debugger

                val = 'dbgSetParameters(' + port + ',"' + pwd \
                    + '",true);\n'

                # avoid that the mouse stay in the window

                val = val + 'lockMouse(false); //dbgSetParameters\n'
                output.write(val)

                for line in inpute.readlines():
                    output.write(line)

                inpute.close()
                output.close()
        except IOError:

            MsgDlg(self,
                   'There was an error during file open or write :\n'
                   + fileC, 'Error!', wx.OK)

    def resetDebug(self):

        # when the debugging is finished : closed or exit menu action
        # the torque main script are reset to the original value

        # get the torque main script file name

        dire = self.mainFrame.menu.getParameter(GAME_DIRECTORY)
        fil = self.mainFrame.menu.getParameter(GAME_FILESCRIPT)
        filec = os.path.join(dire, fil)

        # tmp file contains the original scripts

        filectmp = filec + '-tmp'

        # remove line with 'dbgsetparameters'

        try:
            if os.path.exists(filectmp):
                inpute = open(filectmp)
                output = open(filec, 'w+')
                for line in inpute.readlines():
                    li = line.lower()
                    if li.find('dbgsetparameters') <= -1:
                        output.write(line)

                inpute.close()
                output.close()
        except IOError:

            MsgDlg(self,
                   'There was an error during file open or write :\n'
                   + fileC, 'Error!', wx.OK)

        if os.path.exists(filectmp):
            os.unlink(filectmp)

# -------------------------------------------------------------------------------
# file history management
# -------------------------------------------------------------------------------

    def fileHistoryLoad(self):

        # load the file history from the home user

        fic = getAppliFileName(SAVE_APPLIC)

        if os.path.isfile(fic):
            self.mainFrame.fileLoad = getValue(fic, 'fileLoad', ';')
            for i in range(7, -1, -1):
                x = getValue(fic, 'history' + str(i), ';')
                if x:
                    if os.path.isfile(x):
                        self.filehistory.AddFileToHistory(x)

    def fileHistorySave(self):

        # save the file history into the home user

        fic = self.fileHistoryInit()
        if fic and (self.filehistory.GetCount() > 0):
            out = open(fic, 'w+')
            out.write('fileLoad' + ';' + self.mainFrame.fileLoad + ';\n'
                      )
            for i in range(0, 6):
                try:
                    if self.filehistory.GetHistoryFile(i):
                        out.write('history' + str(i) + ';'
                                  + self.filehistory.GetHistoryFile(i)
                                  + ';\n')
                    else:
                        break
                except wx._core.PyAssertionError:
                    pass

            out.close()

    def fileHistoryInit(self):

        # initialise the home user envrionement

        fic = getAppliFileName(SAVE_APPLIC)

        dire = os.path.dirname(fic)

        # create the directory APPLICATION into the home if it does not exist

        try:
            if not os.path.exists(dire):
                os.mkdir(dire)
        except IOError:
            MsgDlg(self, _('_error-create-dir:') + '\n' + dire,
                   _('_lib-Error!'), wx.OK)

        # delete the file in order to create e new one

        try:
            if os.path.isfile(fic):
                os.unlink(fic)
        except IOError:
            MsgDlg(self, _('_error-create-file:') + '\n' + fic,
                   _('_lib-Error!'), wx.OK)

        return fic

# -------------------------------------------------------------------------------
# parameter management in memory
# -------------------------------------------------------------------------------

    def setParameter(self, key, value):

        # manage the list of parameters : set a value

        self.mainFrame.parameters[key] = value

    def delParameter(self, key):

        # manage the list of parameters : delete a value

        try:
            del self.mainFrame.parameters[key]
        except:
            pass
            return False

        return True

    def getParameter(self, key, default=''):

        # manage the list of parameters : get a value

        x = ''
        try:
            x = self.mainFrame.parameters[key]
        except:
            x = default
            self.mainFrame.parameters[key] = default
            pass

        return x
