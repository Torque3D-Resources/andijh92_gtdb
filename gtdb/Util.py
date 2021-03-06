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
import locale
import gettext
import shutil
from gtdb.Config import *
from gtdb.Parameters import *
import App
import json

def lang():

    # by default the english language is selected

    #lang = wx.Locale(wx.LANGUAGE_DEFAULT).GetCanonicalName().split('_')

    # try:
    #     t = gettext.translation(APPLICATION, DATADIR, languages=[lang[0]])
    # except IOError:
    #     t = gettext.translation(APPLICATION, DATADIR, languages=['en'])

    t = gettext.translation(APPLICATION, DATADIR, languages=['en'])
    return t.lgettext


def initFileLexer(
    inp,
    out,
    style,
    lig,
    ):

    if not os.path.isfile(out):
        try:
            shutil.copyfile(inp, out)
        except IOError:
            pass
            return []

    try:
        f = open(out, 'r+')
    except IOError:
        pass
        print 'error open : ', out
        return []

    try:
        for l in f:
            l = l.replace('\n', '')
            lig[l] = style
    except IOError:
        pass
        print 'error read : ', out
        f.close()
        return []

    f.close()

    return lig


def getFicNameLocale(di, fi):

    fic = os.path.join(DATADIR, di)
    fic = os.path.join(fic, fi)

    return fic


def getFileIcon(image):

    # path tyo load the images

    icon = os.path.join(DATADIR, DIR_ICON)

    icon = os.path.join(icon, image)

    return icon


def MsgDlg(
    self,
    string,
    caption,
    style,
    ):

    # standard message dialog

    dlg = wx.MessageDialog(self, string, caption, style)
    result = dlg.ShowModal()
    dlg.Destroy()

    return result


def getAppliFileName(filec):

    # return the location where the debugger parameters are store ( file history for instance)
    # this parameter are managed by wxpython, reference wxpython doc for more information

    fic = getStandardPath('GetUserLocalDataDir')
    return os.path.join(fic, filec)


def getHomeUser():

    # what is the user home ?
    # this parameter are managed by wxpython, reference wxpython doc for more information

    fic = getStandardPath('GetUserConfigDir')
    return fic


def getStandardPath(lib):

    # this parameter are managed by wxpython, reference wxpython doc for more information

    sp = wx.StandardPaths.Get()
    func = getattr(sp, lib)
    return func()


def getValue(filec, val, sep):

    # get a value from the debugger parameters with a key

    try:
        if os.path.exists(filec):
            input = open(filec)
            for line in input.readlines():
                if line.startswith(val):
                    input.close()
                    tab = line.split(sep)
                    try:
                        return tab[1]
                    except IndexError:
                        return ''

            input.close()

            return ''
    except IOError:

        MsgDlg(self, 'There was an error during file open or read :\n'
               + fileC, 'Error!', wx.OK)


def image(image):

    # fromat the image for wxpython use, reference wxpython doc for more information

    return wx.Image(getFileIcon(image),
                    wx.BITMAP_TYPE_PNG).ConvertToBitmap()


def launchTorque(self):

    # launch torque from the debugger

    rc = True

    # go to the game directory

    current = os.getcwd()
    os.chdir(self.getParameter(GAME_DIRECTORY))

    # launch the game

    if self.getParameter(GAME_FILEBINARY):
        pgm = self.getParameter(GAME_FILEBINARY)
        command = os.path.join(self.getParameter(GAME_DIRECTORY), pgm)
        param = str(self.getParameter(GAME_UNIXPARA))

        if os.name == 'nt':
            os.system('START /b' + ' ' + command + ' ' + param)
        elif os.name == 'posix':
            os.system(command + ' ' + param + ' &')
        else:
            os.system(command + ' ' + param + ' &')
    else:

        rc = False

    # retore the current directory

    os.chdir(current)

    return rc


def sendCmdLn(cmd):

    cmd = cmd.replace('\\', '/')  # for windows
    App.app.frame.host.write(cmd + '\r\n')


def rcFile():

    rcfile = os.path.expanduser('~/.gtdbrc')
    if os.name == 'nt':
        rcfile = rcfile.replace('/', '\\')
    return rcfile

def loadSettings():

    if os.path.isfile(rcFile()):
        with open(rcFile()) as f:
            App.settings = json.load(f)
    else:
        App.settings = {'hideSecWarnDlg': 'n'}


def dumpSettings():

    with open(rcFile(), 'w+') as rc_file:
        json.dump(App.settings, rc_file)
