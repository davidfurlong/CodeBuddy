import sublime, sublime_plugin, math, random

# GNU License Copyright David Furlong
# Used some Scrolling code from
# https://github.com/zzjin/syncViewScroll
# which is licensed under GNU
# Copyright (C) 2012 Tito Bouzout <tito.bouzout@gmail.com>

# TODOS: Auto Language detection + comment syntax {}
# Find, Search, Replace, Save, Save as, Save all
# IE Non text based shortcuts
# Double click to select a line selects the new line char too, so isnt being counted as "select line"
# Probably falsely.

languagesCommentSymbol = []
keyHistory = []
actionLog = []
actionLineLog = []
specialkey = "cmd" if sublime.platform() == "osx" else "ctrl"
sublime.log_commands(False)
sublime.log_input(False)
global hasWarned
sublime.run_command('toggle_sync_scroll')
todaysFocus = random.randrange(1,5+1)

if(sublime.active_window().active_view().size() > 50000):
	sublime.run_command("sub_notify", {"title": "Welcome to CodeBuddy, Try "+specialkey+" + R", "msg": "This file is big, use "+specialkey+" + R to quickly navigate functions", "sound": False})
	# sublime.message_dialog("Welcome to CodeBuddy. This file is sizeable, so remember to use "+specialkey+" + R to quickly navigate functions")
elif(todaysFocus == 1):
	sublime.run_command("sub_notify", {"title": "Welcome to CodeBuddy, Try "+specialkey+" + P", "msg": specialkey+" + P to quickly navigate files", "sound": False})
	# sublime.message_dialog(". Try to focus on using "+specialkey+" + P to quickly navigate files")
elif(todaysFocus == 2):
	sublime.run_command("sub_notify", {"title": "Welcome to CodeBuddy, Try "+specialkey+" + D", "msg":  "Did you know you can use "+specialkey+" + D or "+specialkey+" + click to create multiple cursors?", "sound": False})
	# sublime.message_dialog("Welcome to CodeBuddy. Did you know you can use "+specialkey+" + D or "+specialkey+" + click to create multiple cursors?")
elif(todaysFocus == 3):
	sublime.run_command("sub_notify", {"title": "Welcome to CodeBuddy, Try "+specialkey+" + P then :40", "msg":  specialkey+" + P followed by :<line> to navigate by line", "sound": False})
	# sublime.message_dialog("Welcome to CodeBuddy. Did you know you can use "+specialkey+" + D or "+specialkey+" + click to create multiple cursors?")
elif(todaysFocus == 4):
	sublime.run_command("sub_notify", {"title": "Welcome to CodeBuddy", "msg": "Try "+specialkey+" + K B to toggle sidebar", "sound": False})
	# sublime.message_dialog("Welcome to CodeBuddy. Did you know you can use "+specialkey+" + D or "+specialkey+" + click to create multiple cursors?")

class isDeletingLineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				lineA = self.view.full_line(region.a)
				lineB = self.view.full_line(region.b)
				posA = self.view.rowcol(region.a)
				posB = self.view.rowcol(region.b)
				if(posA[0] - posB[0] == 1 or posA[0] - posB[0] == -1):
					if(posA[0] > posB[0]):
						if(len(self.view.substr(lineA)[:posA[1]].replace(' ', '').replace('\t', '')) == 0 and self.view.substr(lineB)[posB[1]:].replace(' ', '').replace('\t', '') == "\n"):
							sublime.run_command("sub_notify", {"title": "Shortcut Tip, "+specialkey+" + J", "msg":  "Press Cmd J to delete the new line after the current line", "sound": False})
					else:
						if(len(self.view.substr(lineB)[:posB[1]].replace(' ', '').replace('\t', '')) == 0 and self.view.substr(lineA)[posA[1]:].replace(' ', '').replace('\t', '') == "\n"):
							sublime.run_command("sub_notify", {"title": "Shortcut Tip, "+specialkey+" + J", "msg":  "Press Cmd J to delete the new line after the current line", "sound": False})

				pos = self.view.rowcol(region.a)[1]
				line_contents = self.view.substr(lineA)
				if(pos > 0):
					l = len(actionLog)
					if(l > 1):
						if(actionLog[l-1] == "drag_select" or actionLog[l-2] == "drag_select"):
							if(line_contents[pos-1] == "{" or line_contents[pos] == "{" or line_contents[pos-1] == "}" or line_contents[pos] == "}"):
								sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  "Press ^ + M to find matching bracket, or ^ + shift + M to select all contents of current parentheses", "sound": False})


class isNextToBracketCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				lines = self.view.line(region)

				pos = self.view.rowcol(region.a)[1]
				line_contents = self.view.substr(lines) + '\n'
				if(pos > 0):
					l = len(actionLog)
					if(l > 1):
						if(actionLog[l-1] == "drag_select" or actionLog[l-2] == "drag_select"):
							if(line_contents[pos-1] == "{" or line_contents[pos] == "{" or line_contents[pos-1] == "}" or line_contents[pos] == "}"):
								sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  "Press ^ + M to find matching bracket, or ^ + shift + M to select all contents of current parentheses", "sound": False})

								# sublime.message_dialog("Press ^ + M to find matching bracket, or ^ + shift + M to select all contents of current parentheses")
				
class getSelectedRegionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
	    for region in self.view.sel():
	        if region.empty():
	            line = self.view.line(region)
	            line_contents = self.view.substr(line) + '\n'
	        else:
	        	print(region)

class isRegionWholeLineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				return
			else:
				if(self.view.rowcol(region.a)[0] != self.view.rowcol(region.b)[0]):
					return
				else:
					if (self.view.rowcol(region.a)[1] == 0 and len(self.view.substr(self.view.line(region.b))) == self.view.rowcol(region.b)[1]) or (self.view.rowcol(region.b)[1] == 0 and len(self.view.substr(self.view.line(region.a))) == self.view.rowcol(region.a)[1]) or (self.view.rowcol(region.a)[1] == 0 and len(self.view.substr(self.view.full_line(region.b))) == self.view.rowcol(region.b)[1]) or (self.view.rowcol(region.b)[1] == 0 and len(self.view.substr(self.view.full_line(region.a))) == self.view.rowcol(region.a)[1]):
						sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  "Press "+specialkey+" + L to select line", "sound": False})
						# sublime.message_dialog("Press "+specialkey+" + L to select line")
						actionLog.append('select_line')
						actionLineLog.append(self.view.rowcol(region.a)[0])
						return

class isAtLineStartCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if region.empty():
				x = self.view.line(region.a)
				p = self.view.rowcol(region.a)[1]
				if len(self.view.substr(x)[:p].replace(" ", "").replace("\t", "").replace("//", "").replace("/*", "").replace("<!--", "").replace('#', '')) != 0:
					return
			else:
				if len(self.view.substr(region).replace(" ", "").replace("\t", "").replace("//", "").replace("/*", "").replace("<!--", "").replace('#', '')) != 0:
					return
		sublime.run_command("sub_notify", {"title": "Comment current Line "+specialkey+" + /", "msg":  "To Comment current line press "+specialkey+" + /", "sound": False})
		# sublime.message_dialog("To Comment current line press "+specialkey+" + /")


class isAtLineStartTabCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		print ('tab')
		for region in self.view.sel():
			if region.empty():
				x = self.view.line(region.a)
				p = self.view.rowcol(region.a)[1]
				if len(self.view.substr(x)[:p].replace(" ", "").replace("\t", "").replace("//", "").replace("/*", "").replace("<!--", "").replace('#', '')) != 0:
					return
			else:
				if len(self.view.substr(region).replace(" ", "").replace("\t", "").replace("//", "").replace("/*", "").replace("<!--", "").replace('#', '')) != 0:
					return
		sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  specialkey+" + [ to indent line, and "+specialkey+" + ] to unindent line from cursor anywhere in the line", "sound": False})
		# sublime.message_dialog("Better than tab to indent is "+specialkey+" + [ to indent line, and "+specialkey+" + ] to unindent line")

class CodeBuddy(sublime_plugin.EventListener):

	def on_modified(self, view):
		print("on modified")
		actionLog.append(view.command_history(0))
		actionLineLog.append(view.rowcol(view.sel()[0].a)[0])
		# actionLineLog.append(view.)
		# view.command_history(0);
		 
		keyHistory.append(view.substr(sublime.Region(0, view.size())))
		if (view.command_history(0)[1]):
			# Comment Line for 2 languages?
			if (view.command_history(0)[1]['characters'] == "//" or view.command_history(0)[1]['characters'] == "<!--" or view.command_history(0)[1]['characters'] == "/*" or view.command_history(0)[1]['characters'] == "#"):
				view.run_command('is_at_line_start')


	def on_text_command(command_name, view, args, ne): #args and command_name is swapped?
		print('text command')

		if(sublime.active_window().active_view().name() == "Find Results"):
			sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  'Double click the left gutter in find to go to the file and line number', "sound": False})
			# sublime.status_message('Double click the gutter in find to go to the file and line number')
		# if args == "drag_select":
		# 	view.run_command('is_region_whole_line')
		view.run_command('is_deleting_line')
		view.run_command('is_next_to_bracket')
		try:
			if len(actionLog) > 0 and (actionLog[len(actionLog)-1] == "drag_select" or ne['by'] == 'lines'):
				if (args == "left_delete"):
					sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg": specialkey+' + X to delete the current line', "sound": False})
				else:
					view.run_command('is_region_whole_line')
		except:
			pass
		actionLog.append(args)
		actionLineLog.append(view.rowcol(view.sel()[0].a)[0])

		keyHistory.append(command_name)
		try:
			if( ne['default'] == "\t"):
				view.run_command('is_at_line_start_tab')
		except:
			pass
	
		
		l = len(actionLog)

		# TODO
		if(l > 2 and len(keyHistory) != 0):
			
			# scenario 1 no new line
			try:
				if(actionLog[l-1]=="paste_and_indent" and actionLog[l-2] == "drag_select" and actionLog[l-3][0]=="cut" and actionLog[l-5]=="drag_select" and (actionLineLog[l-3] == 1+actionLineLog[l-1] or actionLineLog[l-3]+1 == actionLineLog[l-1] or actionLineLog[l-3]+2 == actionLineLog[l-1] or actionLineLog[l-3] == 2+actionLineLog[l-1])):
					sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  "ctrl + "+specialkey+" + ↑ or ↓ to swap lines (transpose)", "sound": False})	
			except:
				pass
			# scenario 2 new line
			try:
				if(actionLog[l-1]=="paste_and_indent" and actionLog[l-2][1]['characters'] == "\n" and actionLog[l-3]=="insert" and actionLog[l-5][0]=="cut" and (actionLineLog[l-5] == 1+actionLineLog[l-1] or actionLineLog[l-5]+1 == actionLineLog[l-1] or actionLineLog[l-5]+2 == actionLineLog[l-1] or actionLineLog[l-5] == 2+actionLineLog[l-1])):
					sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  "ctrl + "+specialkey+" + ↑ or ↓ to swap lines (transpose)", "sound": False})	
			except:
				pass
			try:
				if(actionLog[l-1]=="paste_and_indent" and actionLog[l-2][1]['characters'] == "\n" and actionLog[l-3]=="insert" and actionLog[l-5]=="copy" and (actionLineLog[l-5] == 1+actionLineLog[l-1] or actionLineLog[l-5]+1 == actionLineLog[l-1])):
					sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  specialkey+" + shift + D to duplicate a line. Remember, D for duplicate", "sound": False})
					# sublime.message_dialog(""+specialkey+" + shift + D to duplicate a line. Remember, D for duplicate")
			except:
				pass

	def on_window_command(self, window, command_name, args):

		print('window command')
		print(window)
		print(command_name)
		print(args)
		if(sublime.active_window().active_view().name() == "Find Results"):
			sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  'Double click the gutter in find to go to the file and line number', "sound": False})
			# sublime.status_message('Double click the gutter in find to go to the file and line number')
		if len(actionLog) > 0 and actionLog[len(actionLog)-1] == "drag_select":
			window.active_view().run_command('is_region_whole_line')
		actionLog.append(args)
		actionLineLog.append(sublime.active_window().active_view().rowcol(sublime.active_window().active_view().sel()[0].a)[0])

# UNUSED. FOR FUTURE EXTENSION INTO SCROLLING

import _thread as thread
import time

synch_scroll_running = False
synch_scroll_current_view_object = None

def updatePos(view):
	view.settings().set('origPos',view.viewport_position()[1])

def initialize(view):
	#print 'initialize'
	if not view.settings().has('syncScroll'):
		view.settings().set('syncScroll',False)
		#the add on change should be here, it's elsewhere for debug reasons
	updatePos(view)
	view.settings().clear_on_change('syncScroll') #for debug reasons
	view.settings().add_on_change('syncScroll', updateStatus) #when syncScroll is toggled, update status bar
def plugin_loaded():
	if not 'running_synch_scroll_loop' in globals():
		global running_synch_scroll_loop
		running_synch_scroll_loop = True
		thread.start_new_thread(synch_scroll_loop, ())
	#on startup initialize every view
	print ("syncScroll starting")
	for window in sublime.windows():
		for view in window.views():
			initialize(view)
def synch_scroll_loop():
	while True:
		global synch_scroll_running
		if not synch_scroll_running:
			synch_scroll_running = True
			sublime.set_timeout(lambda: synch_scroll(), 0)
		time.sleep(0.08)

def synch_scroll():
	global synch_scroll_running
	global synch_scroll_current_view_object

	# print ("one timeout")

	current_view = synch_scroll_current_view_object
	try:
		if(100 < current_view.viewport_position()[1] and not hasWarned):
			hasWarned = True
			sublime.run_command("sub_notify", {"title": "Shortcut Tip", "msg":  "Stop scrolling! Use "+specialkey+" + P then : for line number, enter or @ for function definitions. You can also try bookmarking by installing the SublimeBookmarks package", "sound": False})
			# sublime.message_dialog("Stop scrolling! Use "+specialkey+" + P then : for line number, enter or @ for function definitions. You can also try bookmarking by installing the SublimeBookmarks package")
	except:
		hasWarned = False
		pass
	# 	x = 1

	# previousPosition = current_view.viewport_position()[1]
	if current_view is None or current_view.is_loading() or not current_view.settings().get('syncScroll'):
		synch_scroll_running = False
		return
	callingViewPos = current_view.viewport_position()[1]
	origCallingViewPos = current_view.settings().get('origPos')
	# print ('modified. origCallingViewPos=', origCallingViewPos, 'callingViewPos= ', callingViewPos)
	if callingViewPos != origCallingViewPos: #and it moved vertically
		# print ("it moved")
		for view in current_view.window().views():
			if view.settings().get('syncScroll') and view.id() != current_view.id(): #if view has syncScroll enabled AND we're not talking about the same view as view
				#we move view
				viewPos = view.viewport_position()[1]
				newViewPos = viewPos+callingViewPos-origCallingViewPos
				# print ("moving. viewPos= ",viewPos," newViewPos= ",newViewPos)
				view.set_viewport_position((view.viewport_position()[0],newViewPos), True) #move the other view
				updatePos(view)
		updatePos(current_view) #update original positions
	synch_scroll_running = False

def updateStatus():
	# print "updateStatus"
	for window in sublime.windows():
		for view in window.views():
			if view.settings().get('syncScroll'):
				view.set_status('syncScroll','[Sync ON]')
			else:
				view.erase_status('syncScroll')

class syncScrollListener(sublime_plugin.EventListener):
	def on_activated(self, view):
		global synch_scroll_current_view_object
		synch_scroll_current_view_object = view

	def on_load(self,view):
		#on load add settings to a view
		# print ("on_load")
		initialize(view)

class ToggleSyncScrollCommand(sublime_plugin.TextCommand):
	def run(self, edit, setting):
		current_state = self.view.settings().get('syncScroll')
		self.view.settings().set('syncScroll',not current_state)
	def is_checked(self, setting):
		if not self.view.settings().has('syncScroll'):
			initialize(self.view)
		# print ("current setting",self.view.settings().get('syncScroll'))
		return self.view.settings().get('syncScroll')
