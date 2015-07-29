#Module to contain functions to handle warnings

def printWarnings():
	print ""
	for warning in warnings:
		print "<< WARNING: %s >>\n" % warning

def addWarning(warningmsg):
	if warningmsg not in warnings:
		warnings.append(warningmsg)

warnings = []

