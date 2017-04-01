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
import wx.stc
import re

from TorqueParametersV02 import *
from TorqueUtilV03_01 import *
_ = lang()

if wx.Platform == '__WXMSW__':
    font1 = 'Arial'
    font2 = 'Times New Roman'
    font3 = 'Courier New'
    fontSize = 10
else:
    font1 = 'Helvetica'
    font2 = 'Times'
    font3 = 'Courier'
    fontSize = 10


class PythonSTC(wx.stc.StyledTextCtrl):

    fold_symbols = 2

    def __init__(
        self,
        parent,
        ID,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=0,
        mainFrame=0,
        ):
        wx.stc.StyledTextCtrl.__init__(
            self,
            parent,
            ID,
            pos,
            size,
            style,
            )

        self.mainFrame = mainFrame

            # style identifier

        self.key1 = 1
        self.key2 = 2
        self.key3 = 3
        self.key4 = 4
        self.key5 = 5
        self.comment = 6
        self.brace = 7
        self.varp = 8
        self.vard = 9

        self.tab = ''

        self.Bind(wx.stc.EVT_STC_MODIFIED, self.OnModified)  # V2.4
        self.FileModified = False  # V2.4

        self.tagComment = False

        self.EmptyUndoBuffer()

            # no lexer defined , the standard one is taken into account

        self.SetLexer(wx.stc.STC_LEX_CONTAINER)
        wx.stc.EVT_STC_STYLENEEDED(self, -1, self.OnStyleNeeded)

        self.SetMargins(0, 0)

            # Setup a margin to hold fold markers

        self.SetMarginType(0, wx.stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(0, 25)

            # define the margin name to use

        self.SetMarginSensitive(1, True)
        self.SetMarginType(1, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginWidth(1, 20)

            # define the markers

        self.MarkerDefine(0, wx.stc.STC_MARK_ROUNDRECT, '#CCFF00', 'RED'
                          )  # red circle
        self.MarkerDefine(2, wx.stc.STC_MARK_SHORTARROW, 'blue', 'blue')  # blue arrow

            # used to avoid to relaod systematically the text at each call

        self.OldFile = ''

    def OnMarginClickEditor(self, evt):

            # function lauched by the main menu when a click is done in the margin of the text file

        self.mainFrame.SetStatusText('')

            # if a click is done in the expected margin

        if evt.GetMargin() == 1:

                # get the line number and the line content

            lineClicked = self.LineFromPosition(evt.GetPosition())
            line = self.GetLine(lineClicked).lstrip()
            li = str(lineClicked + 1)

                # prepare the data to display in the bottom ofthe screen

            title = self.mainFrame.fileTorque
            data = title + ':' + li

            if self.isLignValid(line):

                    # if the marker does not exxist on the line

                if self.MarkerGet(lineClicked) == 0:

                        # add the red marker

                    self.MarkerAdd(lineClicked, 0)

                        # populate the tab for break point

                    self.mainFrame.nboo.list_breakPoint.Populate(data,
                            '', '')

                        # and send the break order to add the break point into.... the torque debugger

                    if self.mainFrame.host:
                        x = 'BRKSET' + ' ' + title + ' ' + li \
                            + ' 0 0 1\r\n'
                        x = str(x)
                        try:
                            self.mainFrame.host.write(x)
                        except socket.error:
                            pass
                            return _('_error-host-add')

                        return _('_ok-host-add')

                    return _('_ok-list-add')
                else:

                    # if a marker exist in the line
                        # remove the 2 possible marker

                    self.MarkerDelete(lineClicked, 0)
                    self.MarkerDelete(lineClicked, 2)

                        # delete the line in the tab for break point

                    self.mainFrame.nboo.list_breakPoint.Delete(data)

                        # and send the break order to remove the break point into the torque debugger

                    if self.mainFrame.host:
                        x = 'BRKCLR' + ' ' + title + ' ' + li
                        x = str(x)
                        try:
                            self.mainFrame.host.write(x)
                        except socket.error:
                            pass
                            return _('_error-host-delete')

                        return _('_ok-host-delete')

                    return _('_ok-list-delete')
            else:

                # if the line selected is not valid
                # this could happen when lines are added to the torque script
                    # if a marker exist

                if self.MarkerGet(lineClicked) != 0:

                        # remove the marker

                    self.MarkerDelete(lineClicked, 0)

                        # delete the line in the tab for break point

                    self.mainFrame.nboo.list_breakPoint.Delete(data)

                        # and send the break order to remove the break point into the torque debugger

                    if self.mainFrame.host:
                        x = 'BRKCLR' + ' ' + title + ' ' + li
                        x = str(x)
                        try:
                            self.mainFrame.host.write(x)
                        except socket.error:
                            pass
                            return _('_error-host-delete')

                        return _('_ok-list-delete')

                return _('_noSelection')

    def isLignValid(self, line):

            # check if the lign is valid

        if line.startswith('//'):
            return False
        if line.startswith('function'):
            return False
        if line.startswith('}'):
            return False
        if line.startswith('{'):
            return False

        return True

    def OnStyleNeeded(self, evt):
        start = self.GetEndStyled()
        end = evt.GetPosition()
        text = self.GetTextRange(start, end)

        line = text.splitlines()
        startline = start
        for lin in line:
            l = lin.lstrip()

            if l.startswith('/*') or self.tagComment:
                self.tagComment = True
                self.SetStyleNeeded(lin, startline, 0, self.comment)
                if l.startswith('*/'):
                    self.tagComment = False
            else:
                li = re.split('[=!><)(;+-/|^~}{.,;\]\[?\t@: ]', lin)
                for x in li:
                    try:
                        if self.mainFrame.fickey[x]:
                            self.TestStyleNeeded(x, lin, startline,
                                    self.mainFrame.fickey[x])
                    except KeyError:
                        pass

                    if x.startswith('%'):
                        self.TestStyleNeeded(x, lin, startline,
                                self.varp)
                    elif x.startswith('$'):
                        self.TestStyleNeeded(x, lin, startline,
                                self.vard)

                self.TestStyleNeeded('@', lin, startline, self.key1)
                self.TestStyleNeeded('{', lin, startline, self.brace)
                self.TestStyleNeeded('}', lin, startline, self.brace)
                self.TestStyleNeeded('(', lin, startline, self.brace)
                self.TestStyleNeeded(')', lin, startline, self.brace)
                self.TestStyleNeeded('<', lin, startline, self.key1)
                self.TestStyleNeeded('>', lin, startline, self.key1)
                self.TestStyleNeeded('=', lin, startline, self.key1)
                self.TestStyleNeeded('!', lin, startline, self.key1)
                self.TestStyleNeeded('|', lin, startline, self.key1)
                self.TestStyleNeeded('+', lin, startline, self.key1)
                self.TestStyleNeeded('-', lin, startline, self.key1)
                self.TestStyleNeeded('[', lin, startline, self.brace)
                self.TestStyleNeeded(']', lin, startline, self.brace)
                self.TestStyleNeeded('^', lin, startline, self.key1)
                self.TestStyleNeeded('~', lin, startline, self.key1)

                pos = lin.find('//')
                if pos >= 0:
                    self.StartStyling(startline + pos, 0xff)
                    self.SetStyling(len(lin) - pos, self.comment)

            startline = startline + len(lin) + 1

    def TestStyleNeeded(
        self,
        l,
        lin,
        startline,
        style,
        ):
        pos = lin.find(l)
        while pos >= 0:
            self.SetStyleNeeded(l, startline, pos, style)
            pos = lin.find(l, pos + 1)

    def SetStyleNeeded(
        self,
        l,
        startline,
        pos,
        style,
        ):
        self.StartStyling(startline + pos, 0xff)
        self.SetStyling(len(l), style)

    def load(
        self,
        fil,
        lig,
        line=1,
        ):

        self.saveText(True)

            # load the text file into the text area

        if os.path.isfile(fil):

                # if the file to load is not the same that the previuos one

            if fil != self.OldFile:
                self.OldFile = fil
                self.FileModified = True
                self.SetStyle()
                self.SetReadOnly(0)
                self.SetText('')
                self.SetText(self.loadFormat(fil))

                    # self.SetReadOnly(1) V2.3

                self.SetReadOnly(0)  # V2.4
                self.mainFrame.SetTitle(_('torqueDebug') + ' : '
                        + str(lig))
                self.mainFrame.fileLoad = fil
                self.mainFrame.fileTorque = \
                    fil[len(self.mainFrame.menu.getEnvDir()) + 1:]

            if line:

                    # display the text from the requested line

                scroll = int(line)
                scroll = scroll - 2
                if scroll < 0:
                    scroll = 1

                    # at each time the text is moved or change the red circle
                    # should be displayed again

                if lig:

                        # the list of break point is read in order to retriev the lign with a red circle

                    liste = \
                        self.mainFrame.nboo.list_breakPoint.GetListLign(lig)
                    for l in liste:
                        if l:
                            i = int(l) - 1
                            self.MarkerAdd(i, 0)
                            if scroll <= 1 and i > 3:
                                scroll = i - 2

                    # move the text if the line is not currently displayed into the text area

                deb = self.GetFirstVisibleLine() + 1
                end = deb + self.LinesOnScreen()

                if deb >= scroll or scroll >= end:
                    scroll = scroll - deb
                    self.LineScroll(0, scroll)

        self.FileModified = False  # V2.4
        self.EmptyUndoBuffer()  # V2.4

    def loadFormat(self, fil):
        lig = ''
        f = []
        try:
            f = open(fil, 'r+')
        except IOError:
            pass
            print 'error open : ', fil
            return ''

        margin = ''
        cou = 0
        oldcou = 0
        c = 0
        try:
            for l in f:
                l = l.replace('\t', '')
                l = l.replace('\r', '')
                l = l.replace('\n', '')
                l = l.lstrip(' ')

                if not l.startswith('//'):
                    cou = cou + l.count('{') - l.count('}')

                if cou > oldcou:
                    oldcou = cou
                    c = cou - 1
                    if c < 0:
                        c = 0
                    margin = self.tab * c
                else:
                    oldcou = cou
                    margin = self.tab * cou

                lig = lig + margin + l + '\n'
        except IOError:

            pass
            print 'error read : ', out
            f.close()
            return []
        f.close()

        return lig

    def reset(self):
        self.saveText(True)
        self.SetReadOnly(0)
        self.SetText('')
        self.SetReadOnly(1)
        self.OldFile = ''

    def SetStyle(self):

        fic = getAppliFileName(STYLE)

        v = getValue(fic, 'tab', ';')
        v = int(v)
        self.tab = ''
        while v:
            self.tab = self.tab + ' '
            v = v - 1

        self.StyleClearAll()

        font = int(getValue(fic, 'default_fontsize', ';'))
        fontt = getValue(fic, 'default_fonttype', ';')
        face = getValue(fic, 'default_face', ';')
        fore = getValue(fic, 'default_fore', ';')
        back = getValue(fic, 'default_back', ';')
        self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        font = int(getValue(fic, 'comment_fontsize', ';'))
        fontt = getValue(fic, 'comment_fonttype', ';')
        face = getValue(fic, 'comment_face', ';')
        fore = getValue(fic, 'comment_fore', ';')
        b = getValue(fic, 'comment_back', ';')
        if not b:
            b = back
        self.StyleSetSpec(self.comment,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        font = int(getValue(fic, 'brace_fontsize', ';'))
        fontt = getValue(fic, 'brace_fonttype', ';')
        face = getValue(fic, 'brace_face', ';')
        fore = getValue(fic, 'brace_fore', ';')
        b = getValue(fic, 'brace_back', ';')
        if not b:
            b = back
        self.StyleSetSpec(self.brace,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        font = int(getValue(fic, 'varp_fontsize', ';'))
        fontt = getValue(fic, 'varp_fonttype', ';')
        face = getValue(fic, 'varp_face', ';')
        fore = getValue(fic, 'varp_fore', ';')
        b = getValue(fic, 'varp_back', ';')
        if not b:
            b = back
        self.StyleSetSpec(self.varp,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        font = int(getValue(fic, 'vard_fontsize', ';'))
        fontt = getValue(fic, 'vard_fonttype', ';')
        face = getValue(fic, 'vard_face', ';')
        fore = getValue(fic, 'vard_fore', ';')
        b = getValue(fic, 'vard_back', ';')
        if not b:
            b = back
        self.StyleSetSpec(self.vard,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        font = int(getValue(fic, 'key1_fontsize', ';'))
        fontt = getValue(fic, 'key1_fonttype', ';')
        face = getValue(fic, 'key1_face', ';')
        fore = getValue(fic, 'key1_fore', ';')
        b = getValue(fic, 'key1_back', ';')
        if not b:
            b = back
        self.StyleSetSpec(self.key1,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        font = int(getValue(fic, 'key2_fontsize', ';'))
        fontt = getValue(fic, 'key2_fonttype', ';')
        face = getValue(fic, 'key2_face', ';')
        fore = getValue(fic, 'key2_fore', ';')
        b = getValue(fic, 'key2_back', ';')
        if not b:
            b = back
        self.StyleSetSpec(self.key2,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        font = int(getValue(fic, 'key3_fontsize', ';'))
        fontt = getValue(fic, 'key3_fonttype', ';')
        face = getValue(fic, 'key3_face', ';')
        fore = getValue(fic, 'key3_fore', ';')
        b = getValue(fic, 'key3_back', ';')
        if not b:
            b = back
        self.StyleSetSpec(self.key3,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        font = int(getValue(fic, 'key4_fontsize', ';'))
        fontt = getValue(fic, 'key4_fonttype', ';')
        face = getValue(fic, 'key4_face', ';')
        fore = getValue(fic, 'key4_fore', ';')
        b = getValue(fic, 'key4_back', ';')
        if not b:
            b = back
        self.StyleSetSpec(self.key4,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        font = int(getValue(fic, 'key5_fontsize', ';'))
        fontt = getValue(fic, 'key5_fonttype', ';')
        face = getValue(fic, 'key5_face', ';')
        fore = getValue(fic, 'key5_fore', ';')
        b = getValue(fic, 'key5_back', ';')
        if not b:
            b = back
        self.StyleSetSpec(self.key5,
                          'size:%d,%s,face:%s,fore:%s,back:%s' % (font,
                          fontt, face, fore, back))

        # V2.4
        # this function test if the text has been modified when it is needed

    def OnModified(self, evt):
        if not self.FileModified:
            if evt.GetModificationType() & wx.stc.STC_MOD_BEFOREINSERT \
                or evt.GetModificationType() \
                & wx.stc.STC_MOD_BEFOREDELETE:
                self.FileModified = True

                    # add a star to the title => modified indicator

                self.mainFrame.SetTitle(self.mainFrame.GetTitle() + '*')
                self.mainFrame.toolBar.enableSave(True)

        # V2.4
        # This function save the text modified

    def saveText(self, confirm):

        saveok = False

        if confirm:

                # when the file is changed a confirmation is requested

            if self.FileModified and self.OldFile:
                result = MsgDlg(self, _('_fileChanged') + '''

'''
                                + self.OldFile + '''

'''
                                + _('_doYouSaveIt'), _('_warning'),
                                wx.YES_NO)
                if result == wx.ID_YES:
                    saveok = True
        else:

                # when save by menu or toolbar icon click

            saveok = True

        if saveok:
            self.SaveFile(self.OldFile)
            if self.OldFile.endswith('.cs'):
                dso = self.OldFile + '.dso'
                try:
                    os.unlink(dso)
                except OSError:
                    pass

        self.mainFrame.toolBar.enableSave(False)

            # remove the star to the title

        self.mainFrame.SetTitle(self.mainFrame.GetTitle().replace('*',
                                ''))

        self.FileModified = False
