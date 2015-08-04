#Module to contain functions to handle messages
import sys

class Message():
	shortname = "message(s)"
	"Class that describes messages displayed at end of program"
	def __init__(self,msg):
		self.msg = msg	
		addToCount(Message)
		
	def display(self):
		print ""
		print self.msg + "\n"


class WarningMessage(Message):
	shortname = "warning(s)"
	def __init__(self,msg):
		self.msg = msg
		addToCount(WarningMessage)

	def display(self):
		print "<< WARNING: %s >>\n" % self.msg


class ErrorMessage(Message):
	shortname = "error(s)"
	def __init__(self,msg,forcequit=False):
		self.msg = msg
		addToCount(ErrorMessage)

	def display(self):
		print ""
		print "<< ERROR: %s >>\n" % self.msg


def addToCount(classname):
	if classname not in messagecount:
		messagecount[classname] = 1
	else:
		messagecount[classname] += 1

def printMessages():
	print ""
	for message in messagequeue:
		message.display()

def add(Message):
	exists = False
	for message in messagequeue:
		if Message.msg == message.msg:
			exists = True

	if not exists:
		messagequeue.append(Message)


def addWarning(msg):
	add(WarningMessage(msg))

def addError(msg, forcequit=True):
	add(ErrorMessage(msg))
	if forcequit:
		printMessages()
		sys.exit() #Terminate script upon error

messagecount = {} #Message, count
messagequeue = []

