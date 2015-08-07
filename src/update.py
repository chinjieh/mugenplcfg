# Module to update tool
import paths
import urllib
import urllib2
import customExceptions

PCI_IDS = "https://pci-ids.ucw.cz/v2.2/pci.ids"

def update():
	print "Updating tool..."
	updatePciIds(PCI_IDS, paths.PCIIDS)

def updatePciIds(url, location):
	print "Attempting to update file: %s" % location
	try:
		print "Checking for resource file @ '%s'" % url
		urllib2.urlopen(url)
	except (urllib2.URLError):
		print "Failed to update file: %s" % location
		print "> pci.ids file could not be updated from url: %s" % url
		print "> The file can be obtained manually from the repository."
		raise customExceptions.PciIdsInvalidLink()
	else:
		print "Updating file: %s" % location
		urllib.urlretrieve(url, location)