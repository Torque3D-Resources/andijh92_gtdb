"""
Debugger for Torque , more information http://www.garagegames.com/products/torque/tge/.
Copyright (C) 2007	philippe.cain@orange.fr, more information http://eviwo.free.fr/torque/Debugger-documentation.html

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA	 02110-1301, USA.
"""

"""
This program manages all the lists visible at the bottom of the GUI in the tab window
These lists are done to inform the user of Torque and debugger internal information
From this list by a click the user can retrives the source code and the line listed 
"""

import wx
import re

from TorqueParametersV02	import *
from TorqueUtilV03_01					import *
_ = lang()


class NoteList(wx.Notebook):
	def __init__(self, parent, ID,mainFrame=0):
		wx.Notebook.__init__(self, parent, -1)
		
		self.mainFrame = mainFrame

#-------------------------------------------------------------------------------
# tab GUI definition
#-------------------------------------------------------------------------------
		
		watchValue	= wx.Panel(self)
		callStack		= wx.Panel(self)
		breakPoint	= wx.Panel(self)
		logDisplay	= wx.Panel(self)
		logCompile	= wx.Panel(self)
		logDump			= wx.Panel(self)

		self.AddPage(watchValue , _('_watchValue'))
		self.AddPage(callStack	, _('_callStack'))
		self.AddPage(breakPoint , _('_breakPoint'))
		self.AddPage(logCompile , _('_logCompile'))
		self.AddPage(logDisplay , _('_logDisplay'))
		self.AddPage(logDump 		, _('_logDump'))

		dialog_sizer = wx.BoxSizer(wx.VERTICAL)
		dialog_sizer.Add(self, 1, wx.EXPAND|wx.ALL)
		
		watchValue_sizer = wx.BoxSizer(wx.VERTICAL)
		self.list_watchValue = ListLignForEditor(watchValue, -1,_("_name-file"),_("_name-attribute"),_("_value"))
		watchValue_sizer.Add(self.list_watchValue, 1, wx.EXPAND|wx.ALL)
		watchValue.SetSizer(watchValue_sizer)
		
		callStack_sizer = wx.BoxSizer(wx.VERTICAL)
		self.list_callStack = ListLignForEditor(callStack, -1,_("_name-stack"),_("_func-stack"),"")
		callStack_sizer.Add(self.list_callStack, 1, wx.EXPAND|wx.ALL)
		callStack.SetSizer(callStack_sizer)

		breakPoint_sizer = wx.BoxSizer(wx.VERTICAL)
		self.list_breakPoint = ListLignForEditor(breakPoint, -1,_("_name-lib"),_("_condition-lib"),_("_hit-lib"))
		breakPoint_sizer.Add(self.list_breakPoint, 1, wx.EXPAND|wx.ALL)
		breakPoint.SetSizer(breakPoint_sizer)
		
		logDisplay_sizer = wx.BoxSizer(wx.VERTICAL)
		self.list_logDisplay = LogDisplay(logDisplay, -1)
		logDisplay_sizer.Add(self.list_logDisplay, 1, wx.EXPAND|wx.ALL)
		logDisplay.SetSizer(logDisplay_sizer)
		
		logCompile_sizer = wx.BoxSizer(wx.VERTICAL)
		self.list_logCompile = ListLignForEditor(logCompile, -1,_("_name-error"),_("_error-lib"),_("_compile-mess"))
		logCompile_sizer.Add(self.list_logCompile, 1, wx.EXPAND|wx.ALL)
		logCompile.SetSizer(logCompile_sizer)

		logDump_sizer = wx.BoxSizer(wx.VERTICAL)
		self.list_logDump = LogDisplay(logDump, -1)
		logDump_sizer.Add(self.list_logDump, 1, wx.EXPAND|wx.ALL)
		logDump.SetSizer(logDump_sizer)

		
	def resetNoteList(self):

		self.list_breakPoint.reset()
		self.resetNoteDebug()
	
	def resetNoteDebug(self):
		self.list_watchValue.reset()
		self.list_callStack.reset()
		self.list_logDisplay.reset()
		self.list_logCompile.reset()
		self.list_logDump.reset()
		
#-------------------------------------------------------------------------------
# tab GUI generic class definition
#-------------------------------------------------------------------------------

class ListLignForEditor(wx.ListCtrl):
	# this class managed the same kind of GUI : reference to the source code

	# define the column needed ( minimum 1, maximum = 3 )
	def __init__(self, parent, ID,col1,col2,col3, 
								pos=wx.DefaultPosition,
								size=wx.DefaultSize, 
								style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SORT_ASCENDING):
									
		wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
		self.parent = parent
		self.col1		= col1
		self.col2		= col2
		self.col3		= col3
		self.param	= ''
		
		self.InsertColumn(0, _(self.col1))
		self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
		self.col0width = self.GetColumnWidth(0)
		if self.col2:
			self.InsertColumn(1, _(self.col2))
			self.SetColumnWidth(1,wx.LIST_AUTOSIZE_USEHEADER)
			self.col1width = self.GetColumnWidth(1)
		if self.col3:
			self.InsertColumn(2, _(self.col3))
			self.SetColumnWidth(2,wx.LIST_AUTOSIZE_USEHEADER)
			self.col2width = self.GetColumnWidth(2)
		
	
	# id the information in this tab has been saved as game torque parameters, 
	# it is possible to reload it
	def init(self,param):
		li = []
		self.param = param
		if self.param:
			x = self.getparents().mainFrame.menu.getParameter(param)
			if x:
				li = x
				for l in li:
					self.Populate(str(l),'','',False)
	
	def getparents(self):
		return self.GetParent().GetParent()
	
	def Populate(self,col1,col2,col3,noInit=True):
		# populate the line with the information received
		
		# add the data into each column
		key		= listGetLastIndex(self)
		index = self.InsertStringItem(sys.maxint, str(key))
		
		self.SetStringItem(index, 0, col1)
		self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
		if self.GetColumnWidth(0) < self.col0width:
				self.SetColumnWidth(0,self.col0width)

		if self.col2:
			self.SetStringItem(index, 1, col2)
			self.SetColumnWidth(1,wx.LIST_AUTOSIZE)
			if self.GetColumnWidth(1) < self.col1width:
				self.SetColumnWidth(1,self.col1width)
		if self.col3:
			self.SetStringItem(index, 2, col3)
			self.SetColumnWidth(2,wx.LIST_AUTOSIZE)
			if self.GetColumnWidth(2) < self.col2width:
				self.SetColumnWidth(2,self.col2width)
				
		self.SetItemData(index, key)
		
		# if the data should be saved as game parameters : save it in memory
		if self.param:
			if noInit:
				li	= []
				x		= self.getparents().mainFrame.menu.getParameter(self.param)
				if x:
					li = x
					
				li.append(col1)
				self.getparents().mainFrame.menu.setParameter(self.param ,li)
	
	def Delete(self,line):
		# delete tle line into the GUI
		index = listGetLineIndex(self,line)
		if index != -1: 
			self.DeleteItem(index)
			li = []
			
			# if the data should be saved as game parameters : save it in memory
			if self.param:
				x = self.getparents().mainFrame.menu.getParameter(self.param)
			if x:
				li = x
				li.remove(line)
				if self.param:
					self.getparents().mainFrame.menu.setParameter(self.param ,li)
	
	def GetFileLign(self,index):
		# get the values of the first column of the line
		line = self.getColumnText(index,0)

		try:
			(col1,col2) = line.split(':')
		except ValueError:
			(col1,col2) = ('','')
		
		col3 = self.getColumnText(index,1)
		col4 = self.getColumnText(index,2)
				
		return (col1,col2,col3,col4)
		
	def getColumnText(self, index, col):
		item = self.GetItem(index, col)
		return item.GetText()
				
	def GetListLign(self,fil):
		# thsi function return the complete list of lign displayed in the GUI
		found			= 1
		lastFound = -1
		liste			= ''
		
		while found:
			
			index = self.GetNextItem(lastFound,wx.LIST_NEXT_ALL)
		
			if index == -1:
				break
			else:
				lastFound = index
			
			l = self.GetItemText(index)
			if l.startswith(fil):
				col		= l.split(':')
				liste = liste + col[1] + ':'
				
		return liste.split(':')
	
	def reset(self):
		self.DeleteAllItems()
		try:
			self.SetColumnWidth(0,self.col0width)
			self.SetColumnWidth(1,self.col1width)
			self.SetColumnWidth(2,self.col2width)
		except AttributeError:
			pass
			
#-------------------------------------------------------------------------------
# tab GUI specific class to manage debuger display and actions
#-------------------------------------------------------------------------------

class LogDisplay(wx.TextCtrl):
	# this GUI is specific to the torque debugger and the information received form torque 
	# through the TELNET concetion
	# This function is called each time that the debugger in Torque send information via the port
	# in order to display the compile error and take into account the break and watched the value

	def __init__(self, parent,ID):
		wx.TextCtrl.__init__(self, parent, ID, size=(400,90), style=wx.TE_MULTILINE)
		self.breakList	= ''
		self.marker			= 0
		self.firstTime	= True
		self.dump				= False
		
	def append(self,data):
		# add the line	return by Torque into the GUI if the condition are fullfill
	
		data	= data.replace('\r','')
		lis		= data.split('\n')
		lineprevious = ''
		dump = False
		
		for l in lis:		
			l = l.replace('\n','')
			
			# if it is simple diplay of torque debugger

			if l.startswith('COUT '):
				l = l.replace('COUT ','')
				line = l
				l = l.lstrip() 
				
				if ( self.dump ):
					try:
						self.getparents().mainFrame.nboo.list_logDump.AppendText(line + '\n')
						continue
					except UnicodeDecodeError:
						continue
				else:					
					try:
						self.AppendText(line + '\n')
					except UnicodeDecodeError:
						continue


				# if error of compilation found 
				if l.endswith('- parse error'):
					l = l.replace(' Line: ',':')
					try:
						(line,err) = l.split(' - ')
					except ValueError:
						continue
					
					self.getparents().mainFrame.nboo.list_logCompile.Populate(line,err,'')
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue
					
				# if missing file during script compilation found
				if l.startswith('Missing file:'):
					(line,err) = l.split(':')
					self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'',err)
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue
				
				# if file are missing during script compilation 
				if l.startswith('Could not locate'):
					(line,err) = l.split(':')
					self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'',err)
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue

				# if object are missing during script compilation
				if l.find('Unable to find object') > -1:
					l = l.replace(' (',':')
					l = l.replace('): ',' - ')
					(line,err) = l.split(' - ')
					
					self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'',err)
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue
					
				# if animation are missing during script compilation	
				if l.find('is not a member') > -1:
					l = l.replace(' (',':')
					l = l.replace('): ',' - ')
					(line,err) = l.split('is not a member')
					self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'is not a member',err)
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue
					
				# if preload fialed for an object 
				if l.find('preload failed for') > -1:
					l = l.replace('): ',')')
					(line,err) = l.split('preload failed for')
					self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'preload failed for',err)
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue
					
				# if unknown command
				if l.find('Unknown command') > -1:
					(line,err) = l.split(':')
					self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'unknown command'," ")
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue

				# if Unable to find function
				if l.find('Unable to find function') > -1:
					l = l.replace(' (',':')
					l = l.replace('): ',' - ')
					(line,err) = l.split(' - ')
					self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'Unable to find function',err)
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue
					
				if l.find('Missing terrain texture') > -1:
					(line,err) = l.split(':')
					self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'',err)
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue

				if l.find('nable to load') > -1:
					if lineprevious:
						(line,err) = lineprevious.split(':')
						err = l
						self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'Unable to load',err)
						self.getparents().mainFrame.SetStatusText(_("_error-compile"))
						lineprevious = ''
						continue
					else:
						self.getparents().mainFrame.nboo.list_logCompile.Populate('Missing object','Unable to load',l)
						self.getparents().mainFrame.SetStatusText(_("_error-compile"))
				else: 
					try:
						if lineprevious:
							(line,err) = lineprevious.split(':')
							self.getparents().mainFrame.nboo.list_logCompile.Populate(line,'Unable to load',err)
							self.getparents().mainFrame.SetStatusText(_("_error-compile"))
							lineprevious = ''
							continue
					except UnboundLocalError:
						lineprevious = ''
						continue
										
				if l.find('Register object failed') > -1:
					lineprevious = l
					continue
					
				if l.find('No mission specified') > -1:
					self.getparents().mainFrame.nboo.list_logCompile.Populate('parameters wrong','Missing mission',l)
					self.getparents().mainFrame.SetStatusText(_("_error-compile"))
					continue


			# if torque stop running
			#if l.startswith('*** ENDING MISSION'):
			# self.getparents().mainFrame.OnMenu_Stop(-1)
			# continue
			
			# if debugger just connect to torque
			if l.startswith('PASS Connected'):
				liste = self.getparents().mainFrame.menu.getParameter('break')
				
				# put in place the break point list into torque
				for l in liste:
					(title,line) = l.split(':') 
					title = title.replace('\\','/') # windows
					if line:
						x = ('BRKSET' + ' ' + title + ' ' + line + ' 0 0 1\r\n')
						x = str(x)
						
						self.getparents().mainFrame.host.write(x)
				
				# stop torque waiting
				self.getparents().mainFrame.OnMenu_RunCurs(-1)
				continue
				
			# if a break point has been detected by Torque activate the debuggeur
			if l.startswith('BREAK'):
				self.getparents().mainFrame.toolBar.enableDebug(True)
				if len(l) > 5 :
					l = l.replace('BREAK ','')
					self.displayBreak(l)
				else:
					self.breakList = 'BREAK'
				continue
			else:
				if self.breakList:
					self.breakList = ''
					#activate the debugger
					self.displayBreak(l)
					continue

			# if evaluation of varibale requested by 'displayBreak()' 
			# the return value send by torque are loaded into the debugger
			if l.startswith('EVALOUT') and l.find('DUMP') < 0 :
				lis = l.split(' ')
				pop = lis[1].split('|')
				self.getparents().mainFrame.nboo.list_watchValue.Populate(pop[0]+':'+pop[1],pop[2],lis[2])
				continue

			# if evaluation of variable requested by 'dump()' 
			if l.startswith('EVALOUT') and l.find('STARTDUMP') > -1 :
				try:
					self.getparents().mainFrame.nboo.list_logDump.AppendText(l + '\n')
				except UnicodeDecodeError:
					pass
					
				self.dump = True
				continue

			if l.startswith('EVALOUT') and l.find('ENDDUMP') > -1 :
				try:
					self.getparents().mainFrame.nboo.list_logDump.AppendText(l + '\n')
				except UnicodeDecodeError:
					pass
					
				self.dump = False
				continue

				
			# function implemented by a patch on torque C++ code 
			# for more information see installation procedure on LINUX
			if l.startswith('DEBUG'):
				print l
				continue

				
	def displayBreak(self,l):
		# this function manage the break done by the torque debugger 
		# -Identify the current break line with a blue arrow
		# -Display the value of the variables in the function
		# -populate the panel call stack with the list of hierarchy of called function
		
	
		# reload the script in the text area where the break occurs
		l			= l.lstrip()
		val		= l.split(' ')
		fic		= os.path.join(self.getparents().mainFrame.menu.getEnvDir(),val[0])
		filL	= val[0]
		self.getparents().mainFrame.editor.load(fic,val[0],val[1])
		
		# display the blue arrow on the line breaked
		i = int(val[1]) -1
		self.getparents().mainFrame.editor.MarkerDelete(self.marker,2) # delete the previous one arrow
		self.getparents().mainFrame.editor.MarkerAdd(i, 2)
		self.marker = i
		
		# poupulate the panel call stack with the list of functions
		j=0
		try:
			while val[j]:
				j = j + 1
		except IndexError:
			pass
			j = j -1
			
		self.getparents().mainFrame.nboo.list_callStack.reset()
		if j > 0:
			i			= j
			
			while i >= 0:
				self.getparents().mainFrame.nboo.list_callStack.Populate(val[i-2]+':'+val[i-1],val[i],'')
				i = i - 3
					
		# clean the panel with attribute value
		self.getparents().mainFrame.nboo.list_watchValue.reset()

		#the attributes which belong to the function are saerched into the text loaded		
		i = self.marker + 1
		while True:
			# the line with 'function' are searched form the current line to the top
			text = self.getparents().mainFrame.editor.GetLine(i)
			
			text = text.lstrip()
			text = text.lower()
			# when the line 'function' is found a new search is done until the end of the function is reached 
			if text.startswith('function'):
				func = str(i+1)
				lis = self.prepareVariable(text,[])
				curly = self.countCurly(text,0) 
				i = i + 1
				while True:
					text = self.getparents().mainFrame.editor.GetLine(i)
					lis = self.prepareVariable(text,lis)
					curly = self.countCurly(text,curly)
					if text and curly == 0:
						break							
					i = i + 1
				
				# the list of variable found is send to torque debugger in order to get the value
				# this value is returned later on , see EVALOUT for more information
				lis.sort()
				for x in lis:
					# the first part of the EVAL function is formatted in order to retrieve easly
					# the funciton by EVALUOUT, lign and variable name : it is a comment. 
					# 0 = mandatory to retieve the value of the local variable 
					# variable : get the value
					val = str('EVAL ' + filL + '|' + func + '|' + x + ' 0 ' + x	 + '\r\n')
					try:
						self.getparents().mainFrame.host.write(val)
					except AttributeError:
						pass
						break
				break
			i = i - 1
			if i < 0:
				break
			
			# if no function are found the panel with watched value is empty
		
		# pop up a message in order to inform the user that a break is performed by torque , one time
		if self.firstTime:
			self.firstTime = False
			MsgDlg(self.getparents().mainFrame, _('_message-debug-ready-lib'),_('_message-debug-ready'), wx.OK | wx.ICON_INFORMATION)
	
	def getparents(self):
		return self.GetParent().GetParent()
		
	def reset(self):
		self.SetValue('')
		
	def countCurly(self,text,curly):
		# counr the curly in order to identif the start/end of function
		curly = curly + text.count('{')
		curly = curly - text.count('}')
		
		return curly
	
		
	def prepareVariable(self,text,lis):
		# the lines get in the function are splitted depending of the separation character used in scripts
		li	= re.split('[=!><)(;+-/|^~}{.,;\]\[?\t@ ]',text)
		
		# a list of varaible is created
		for x in li:
			if x.startswith('%') or x.startswith('$') and len(x) > 1 :
				if lis.count(x) == 0:
					lis.append(x)
		
		return lis
		
		
#-------------------------------------------------------------------------------
# tab GUI common functions
#-------------------------------------------------------------------------------
		
			
def listGetLastIndex(self):
	# get the last index of the lign displayed in the tab
	found			= 1
	lastFound = -1
	count			= 0
	
	while found:
		index = self.GetNextItem(lastFound,wx.LIST_NEXT_ALL)
		if index == -1:
			break
		else:
			lastFound = index
			count = count + 1
			
	if count == -1:
		count = 0
	
	count = count + 1
	
	return count

def listGetLineIndex(self,line):
	# get the index relative to a line
	found = 1
	lastFound = -1
	while found:
		
		index = self.GetNextItem(lastFound,wx.LIST_NEXT_ALL)

		if index == -1:
			return None
		else:
			lastFound = index
		if self.GetItemText(index) == line:
			return index

	return -1

