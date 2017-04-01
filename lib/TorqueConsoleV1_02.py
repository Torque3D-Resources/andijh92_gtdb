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

import os
import re

from TorqueParametersV02 import *
from TorqueUtilV03_01 import *
_ = lang()


class ExtractEngine:

    def __init__(self, path):

        self.path = ''
        self.implement = {}
        self.attribute = {}
        self.attr_detail = {}
        self.method = {}
        self.meth_detail = {}
        self.function = {}
        self.func_detail = {}

        self.datablock_h = ''
        self.beforeField_h = ''
        self.addfield_h = ''
        self.beforeMethod_h = ''
        self.method_h = ''
        self.funcTitleBefore_h = ''
        self.funcTitle_h = ''
        self.functionBefore_h = ''
        self.function_h = ''
        self.reportEnd_h = ''

        if os.path.isdir(path):
            self.path = path

        self.key2 = getAppliFileName(KEY2)
        self.key3 = getAppliFileName(KEY3)
        self.key4 = getAppliFileName(KEY4)
        self.key5 = getAppliFileName(KEY5)

    def getReportUrl(self):

        if not self.path:
            return ''

        rc = self.initFileTable()

        if rc == 'OK':
            rc = self.computeReport()

        return rc

    def initFileTable(self):

        groupFunc = NOGROUP
        groupTitle = NOGROUP_TITLE
        key1 = self.formatKey(groupFunc)
        self.implement['2|' + key1 + '|1|function'] = []
        self.function['2|' + key1 + '|1|functionTitle'] = groupTitle

        tmpLine = ''
        cou = 0

        try:
            fkey2 = open(self.key2, 'w+')
            fkey3 = open(self.key3, 'w+')
            fkey4 = open(self.key4, 'w+')
            fkey5 = open(self.key5, 'w+')
        except IOError:
            pass
            print 'error open : ', fkey2, fkey3, fkey4, fkey5
            return ''

        for (root, dirs, files) in os.walk(self.path):

            # print 'root',root

            for fil in files:
                if fil.endswith('cc') or fil.endswith('cpp'):
                    filec = os.path.join(root, fil)

                    ficinput = open(filec)
                    tmpLine = ''
                    for line in ficinput:
                        line = line.replace('\n', '')
                        line = line.replace('\r', '')
                        line = line.replace('\t', '')
                        l = line
                        line = line.lstrip()
                        line = line.lower()

                        if line.startswith('implement_co_') \
                            or line.startswith('implement_conobject') \
                            or line.startswith('addfield') \
                            or line.startswith('consolemethod') \
                            or line.startswith('consolefunction'):
                            tmpLine = l

                        if tmpLine or cou == 0:
                            if line.startswith('consolefunctiongroupbegin'
                                    ) \
                                or line.startswith('consolefunctiongroupend'
                                    ):
                                cou = 1
                                tmpLine = l
                            else:
                                cou = line.count('{') + line.count(';')

                            if cou == 0:
                                if tmpLine != l:
                                    tmpLine = tmpLine + ' ' + l.lstrip()

                                # print "tmpLine",cou,tmpLine,'\n'

                                continue

                            if tmpLine:
                                l = tmpLine
                                line = tmpLine
                                line = line.lstrip()
                                line = line.lower()
                                tmpLine = ''
                                cou = 0
                        else:
                            continue

                        if line.startswith('implement_co_datablock_v1') \
                            or line.startswith('implement_co_netobject_v1'
                                ) \
                            or line.startswith('implement_conobject'):

                            self.getReportUrlWrite(l, '[()]', fkey2)

                            # -The list of implemented object....accessible
                            # -from script is build with datablock and
                            # -netobject

                            # -Example of line read in the file :
                            # implement_co_datablock_v1--
                            # implement_co_datablock_v1(tsshapeconstructor);
                            # print 'implement--',line

                            tab = re.split('[()]', l)
                            key = self.formatKey(tab[1])

                            self.implement['1|' + key + '|0|implem'] = \
                                tab[1] + '|' + filec.replace(self.path,
                                    '')
                        elif line.startswith('addfield'):

                            self.getReportUrlWrite(l, '"', fkey3)

                            # -The attributes list of implemented object are
                            # build and in case of duplicate attributes in
                            # different implemented objects the list of
                            # attributes used in implemented object is build
                            # -The detail of attributes id stored for each
                            # "implemented object / attribute" in order to
                            # avoid to lost detail attribute information coming
                            # from different implemented objects

                            # - Example of line read in the file :
                            # addfield("audioenvironment",typeaudioenvironmentptr,offset(maudioenvironment,waterblock));............................
                            # print 'addfield--',line

                            l = l.replace('"', '')
                            l = l.replace(' ', '')
                            tab = re.split('[(),"]', l)

                            try:
                                key1 = self.formatKey(tab[1])
                                key5 = self.formatKey(tab[5])
                                try:
                                    self.implement['1|' + key5
        + '|1|field'].append(key1)
                                except KeyError:
                                    self.implement['1|' + key5
        + '|1|field'] = []
                                    self.implement['1|' + key5
        + '|1|field'].append(key1)
                            except KeyError, IndexError:
                                pass
                            else:
                                try:
                                    self.attribute[key1].append(key5)
                                except KeyError:
                                    self.attribute[key1] = []
                                    self.attribute[key1].append(key5)
                                    pass

                                self.attr_detail[key5 + '|' + key1] = \
                                    tab
                        elif line.startswith('consolemethod'):

                            self.getReportUrlWrite(l, ',', fkey4)

                            # -The methods list of implemented object are build
                            # and in case of duplicate methods in different
                            # implemented objects the list of methods used in
                            # implemented object is build -The detail of
                            # methods id stored for each "implemented object /
                            # method" in order to avoid to lost detail method
                            # information coming from different implemented
                            # objects

                            # - Example of line read in the file :
                            # consolemethod--
                            # consolemethod(sky,realfog,void,6,6,"(boolshow,floatmax,floatmin,floatspeed)")
                            # print 'consolemethod--',line

                            tab = re.split('[(),"]', l)

                            try:
                                key1 = self.formatKey(tab[1])
                                key2 = self.formatKey(tab[2])
                                try:
                                    self.implement['1|' + key1
        + '|2|method'].append(key2)
                                except KeyError:
                                    self.implement['1|' + key1
        + '|2|method'] = []
                                    self.implement['1|' + key1
        + '|2|method'].append(key2)
                            except KeyError, IndexError:

                                pass
                            else:
                                try:
                                    self.method[key2].append(key1)
                                except KeyError:
                                    self.method[key2] = []
                                    self.method[key2].append(key1)
                                    pass

                                tab[1] = tab[1].replace(' ', '')
                                tab[2] = tab[2].replace(' ', '')
                                tab[3] = tab[3].replace(' ', '')
                                tab[4] = tab[4].replace(' ', '')
                                tab[5] = tab[5].replace(' ', '')
                                tab[6] = tab[6].replace(' ', '')
                                tab[7] = tab[7].replace(' ', '')
                                self.meth_detail[key1 + '|' + key2] = \
                                    tab
                        elif line.startswith('consolefunctiongroupbegin'
                                ):

                            # -The function groups list of implemented object
                            # are build consolefunctiongroupbegin(netinterface,
                            # "global control functions for the
                            # netinterfaces."); print
                            # 'consolefunctiongroupbegin--',line

                            tab = re.split('[(),"]', l, 2)
                            groupFunc = self.formatKey(tab[1])
                            groupTitle = self.formatTitle(tab[2])

                            self.implement['2|' + groupFunc
                                    + '|1|function'] = []
                            self.function['2|' + groupFunc
                                    + '|1|functionTitle'] = groupTitle
                        elif line.startswith('consolefunctiongroupend'):

                            # -There is some function without group also value
                            # by default are set in order to group all these
                            # functions -Example of line read in the file :
                            # consolefunctiongroupend(netinterface); print
                            # 'ConsoleFunctionGroupEnd--',line

                            groupFunc = NOGROUP
                            groupTitle = NOGROUP_TITLE
                        elif line.startswith('consolefunction'):

                            tab = re.split('"', l)
                            self.getReportUrlWrite(l, '[(,]', fkey5)

                            # -The functions list are build and in case of
                            # duplicate functions in different implemented
                            # group function the list of functions used in
                            # group function is build -The detail of functions
                            # id stored for each "group function / function" in
                            # order to avoid to lost detail function
                            # information coming from different group functions
                            # - Example of line read in the file :
                            # consolefunction(getterrainheight, f32, 2, 2,
                            # "(point2i pos) - gets the terrain height at the
                            # specified position.") print
                            # 'consolefunction--',line

                            l = l.replace('"', '')
                            tab = re.split('[(),]', l, 5)

                            try:
                                key1 = self.formatKey(groupFunc)
                                key2 = self.formatKey(tab[1]) + '|' \
                                    + filec.replace(self.path, '')
                                self.implement['2|' + key1
                                        + '|1|function'].append(key2)
                            except KeyError, IndexError:
                                pass
                            else:
                                try:
                                    self.function[key2].append(key1)
                                except KeyError:
                                    self.function[key2] = []
                                    self.function[key2].append(key1)
                                    pass

                                tab[1] = tab[1].replace(' ', '')
                                tab[2] = tab[2].replace(' ', '')
                                tab[3] = tab[3].replace(' ', '')
                                tab[4] = tab[4].replace(' ', '')

                                self.func_detail[key1 + '|' + key2] = \
                                    tab

                    ficinput.close()

        fkey2.close()
        fkey3.close()
        fkey4.close()
        fkey5.close()

        return 'OK'

    def computeReport(self):

        # prepare the template to read

        ficin = getFicNameLocale(REPORT_DIR, REPORT_IN)
        ficout = getAppliFileName(REPORT_OUT)

        finput = open(ficin, 'r+')
        output = open(ficout, 'w+')

        self.initReport(finput, output)
        tab = []
        tabtmp = []
        lisimp = []
        lisimp = self.implement.keys()
        lisimp.sort()
        endDataBlock = False
        datablockName = ''

        for key in lisimp:

            tab = key.split('|')

            # print 'tab1=',tab

            try:
                self.implement[key].sort()
            except AttributeError:
                pass

            # print 'key',self.implement[key]

            key1 = tab[1]
            if tab[0] == '1':
                try:
                    if tab[3] == 'field' and datablockName:
                        output.write(self.beforeField_h)

                        # print 'field1',key, self.implement[key]

                        for key2 in self.implement[key]:

                            # print 'field2',key2,self.attr_detail[key1 +'|'+ key2]

                            tabtmp = self.attr_detail[key1 + '|' + key2]

                            # print 'tabtmp field',tabtmp

                            line = \
                                self.addfield_h.replace('#implement_co_datablock_v1#'
                                    , datablockName)
                            line = line.replace('#addField#', tabtmp[1])
                            line = line.replace('#1#', tabtmp[2])
                            line = line.replace('#offset#', tabtmp[4])
                            output.write(line)
                    elif tab[3] == 'method' and datablockName:

                        output.write(self.beforeMethod_h)

                        # print 'method1',key, self.implement[key]

                        for key2 in self.implement[key]:

                            # print 'method2',self.meth_detail[key1 +'|'+ key2]

                            tabtmp = self.meth_detail[key1 + '|' + key2]
                            line = \
                                self.method_h.replace('#implement_co_datablock_v1#'
                                    , datablockName)
                            line = line.replace('#consolemethod#',
                                    tabtmp[2])
                            line = line.replace('#1#', tabtmp[3])
                            tot = 8 + int(tabtmp[4]) - 2
                            tmp = ''
                            for i in range(8, tot):
                                if tabtmp[i]:
                                    tmp = tmp + tabtmp[i] + ','
                            if not tmp:
                                tmp = ' '
                            tmp = tmp.rstrip(',')
                            line = line.replace('#2#', tmp)
                            try:
                                tabtmp[tot + 3] = tabtmp[tot
                                        + 3].replace('{', '')
                                tabtmp[tot + 3] = tabtmp[tot
                                        + 3].replace('\\n', '')
                                line = line.replace('#3#', tabtmp[tot
                                        + 3])
                            except IndexError:
                                line = line.replace('#3#', ' ')
                                pass
                            output.write(line)
                    elif tab[3] == 'implem':

                        # print 'implem',key, self.implement[key]

                        tabtmp = self.implement[key].split('|')
                        datablockName = tabtmp[0]
                        self.computeReportDataBlock(tabtmp[0],
                                tabtmp[1], output)
                    else:
                        print 'unknown1=', key, self.implement[key]
                except IndexError:
                    print 'unknown2=', key, self.implement[key]
                    pass
            elif tab[0] == '2':

                if not endDataBlock:
                    endDataBlock = True
                    output.write(self.funcTitleBefore_h)
                try:
                    if tab[3] == 'function':

                        # print 'function1=',key,self.implement[key]
                        # print 'function2=',self.function[key+'Title']

                        line = \
                            self.funcTitle_h.replace('#consolefunctionbegin#'
                                , self.function[key + 'Title'])
                        fil = tabtmp[1]
                        output.write(line)
                        output.write(self.functionBefore_h)

                        for key2 in self.implement[key]:

                            # print 'function3',key2,self.func_detail[key1 +'|'+ key2]

                            tabtmp = self.func_detail[key1 + '|' + key2]
                            line = \
                                self.function_h.replace('#consolefunction#'
                                    , tabtmp[1])
                            line = line.replace('#1#', tabtmp[2])
                            tabtmp[5] = tabtmp[5].replace('\\n', '<br>')
                            if tabtmp[5].count(')') \
                                != tabtmp[5].count('('):
                                tabtmp[5] = tabtmp[5].rstrip(')')
                                if tabtmp[5].count(')') \
                                    != tabtmp[5].count('('):
                                    tabtmp[5] = tabtmp[5] + ')'

                            line = line.replace('#2#', tabtmp[5])

                            tabtmp = key2.split('|')
                            line = line.replace('#file#', tabtmp[1])
                            output.write(line)
                    else:
                        print 'unknown3=', key, self.implement[key]
                except IndexError:
                    print 'unknown4=', key, self.implement[key]
                    pass

        output.write(self.reportEnd_h)

        finput.close()
        output.close()

        self.datablock_h = ''
        self.beforeField_h = ''
        self.addfield_h = ''
        self.beforeMethod_h = ''
        self.method_h = ''
        self.funcTitleBefore_h = ''
        self.funcTitle_h = ''
        self.functionBefore_h = ''
        self.function_h = ''
        self.reportEnd_h = ''

        self.implement = {}
        self.attribute = {}
        self.attr_detail = {}
        self.method = {}
        self.meth_detail = {}
        self.function = {}
        self.func_detail = {}

        return ficout

    def computeReportDataBlock(
        self,
        tabtmp0,
        tabtmp1,
        output,
        ):
        line = self.datablock_h.replace('#implement_co_datablock_v1#',
                tabtmp0)
        line = line.replace('#file#', tabtmp1)
        output.write(line)

    def initReport(self, finput, output):

        # DATABLOCK

        line = ''
        for line in finput:
            if line.startswith('<!-- datablock title -->'):
                break
            output.write(line)

        self.datablock_h = ''
        for line in finput:
            if line.startswith('<!-- datablock title -->'):
                break
            self.datablock_h = self.datablock_h + line

        # DATABLOCK REPEAT

        self.beforeField_h = ''
        for line in finput:
            if line.startswith('<!-- addfield repeat -->'):
                break
            self.beforeField_h = self.beforeField_h + line

        self.datablockr = ''
        for line in finput:
            if line.startswith('<!-- addfield repeat -->'):
                break
            self.addfield_h = self.addfield_h + line

        # METHOD REPEAT

        self.beforeMethod_h = ''
        for line in finput:
            if line.startswith('<!-- method repeat -->'):
                break
            self.beforeMethod_h = self.beforeMethod_h + line

        self.method = ''
        for line in finput:
            if line.startswith('<!-- method repeat -->'):
                break
            self.method_h = self.method_h + line

        # Console functon tittle

        self.funcTitleBefore_h = ''
        for line in finput:
            if line.startswith('<!-- consolefunction title -->'):
                break
            self.funcTitleBefore_h = self.funcTitleBefore_h + line

        self.funcTitle_h = ''
        for line in finput:
            if line.startswith('<!-- consolefunction title -->'):
                break
            self.funcTitle_h = self.funcTitle_h + line

        # Console functon repeat

        self.functionBefore_h = ''
        for line in finput:
            if line.startswith('<!-- consolefunction repeat -->'):
                break
            self.functionBefore_h = self.functionBefore_h + line

        self.function_h = ''
        for line in finput:
            if line.startswith('<!-- consolefunction repeat -->'):
                break
            self.function_h = self.function_h + line

        self.reportEnd_h = ''
        for line in finput:
            self.reportEnd_h = self.reportEnd_h + line

    def formatKey(self, tex):
        tex = tex.lower()
        tex = tex.replace(' ', '')

        return tex

    def formatTitle(self, tex):

        tex = tex.replace('\\n', '')
        tex = tex.replace('\\', '')
        tex = tex.replace('"', '')
        tex = tex.replace('.);', '')
        tex = tex.replace(');', '')
        tex = tex.replace('.)', '')
        tex = tex.replace('. )', '')

        return tex

    def getReportUrlWrite(
        self,
        l,
        sep,
        fkey,
        ):
        tab = re.split(sep, l)

        try:
            tab[1] = tab[1].lstrip()
            tab[1] = tab[1].rstrip()
        except IndexError:
            pass
        else:
            fkey.write(tab[1] + '\n')
