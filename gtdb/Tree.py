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
import dircache

from gtdb.Parameters import *
from gtdb.Util import *
_ = lang()


class TreePgm(wx.TreeCtrl):

    def __init__(
        self,
        parent,
        ID,
        mainFrame=0,
        ):
        wx.TreeCtrl.__init__(self, parent, -1)

        self.mainFrame = mainFrame
        self.firstNode = ''

    def loadDirInTree(self):

        # transfrom the game directory content into a tree

        dirGame = self.mainFrame.menu.getEnvDir()
        if dirGame:
            self.resetTree()

            path = os.path.basename(dirGame)
            root = self.AddRoot(path)
            self.firstNode = path

            self.addNodeToTree(dirGame, root)
            self.Expand(root)

            return True

        return False

    def resetTree(self):
        self.DeleteAllItems()

    def addNodeToTree(self, dirGame, root):

        # add nod eto the tree

        a = dircache.listdir(dirGame)

        for path in a:
            fic = os.path.join(dirGame, path)
            if os.path.isdir(fic):
                child = self.AppendItem(root, path)
                self.addNodeToTree(fic, child)
            else:
                if os.path.isfile(fic) and (path.endswith('.cs')
                        or path.endswith('.gui') or path.endswith('.mis'
                        )):
                    child = self.AppendItem(root, path)

        if self.GetChildrenCount(root, False) == 0:
            self.Delete(root)

    def getNodeTreePgm(self, event):

        # return the OS full path of the node selected into the tree
        # The relative path to the file is rebuild from the tree

        # identify the node in the tree

        fic = ''
        nodes = ''
        pt = event.GetPosition()
        (item, flags) = self.HitTest(pt)

        if item:
            node = self.GetItemText(item)

            # if a file has been selected

            if str(node).endswith('.cs') or str(node).endswith('.gui') \
                or str(node).endswith('.mis'):

                # search the parents and rebuild the relative path from hierarchy

                nodes = self.getParents(item, node)

                # build the full path

                if nodes:
                    dirGame = self.mainFrame.menu.getEnvDir()
                    if dirGame:
                        fic = os.path.join(os.path.dirname(dirGame),
                                self.firstNode)
                        fic = os.path.join(fic, nodes)

        # return the file selected and the full path of teh files

        return (fic, nodes)

    def getParents(self, item, node):

        # rebuild the relative path of the selected files
        # recursive function in order to navigate in the tree

        it = self.GetItemParent(item)

        # while parent is found the crecursive call is done

        if it:
            if self.GetItemText(it) != self.firstNode:

                # build the relative path

                no = os.path.join(self.GetItemText(it), node)

                # call recusively in order to get the previuos parent

                node = self.getParents(it, no)
        return node
