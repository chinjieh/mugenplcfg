# Module to update tool
import paths
import urllib
import urllib2

PCI_IDS = "https://pci-ids.ucw.cz/v2.2/pci.ids"

def update():
	print "Updating tool..."
	updatePciIds(PCI_IDS, paths.PCIIDS)

def updatePciIds(url, location):
	print "Attempting to update file: %s" % location
	try:
		urllib2.urlopen(PCI_IDS)
	except urllib2.URLError:
		print "pci.ids file could not be updated from url: %s" % PCI_IDS
		print "The file can be obtained manually from the repository."
	else:
		print "Updating file: %s" % location
		urllib.urlretrieve(url, location)
		
	
	
