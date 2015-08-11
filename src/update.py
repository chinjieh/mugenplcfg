# Module to update tool
import paths
import urllib
import urllib2
import customExceptions
import parseutil
import extractor

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
		oldver = ""
		newver = ""
		
		try:
			with open(location) as oldfile:
				for line in oldfile.readlines():
					if "Version:" in line:
						oldver = parseutil.parseLine_Sep(line,"Version", ":").strip()
						break
		except IOError:
			pass

		urllib.urlretrieve(url, location)
		
		with open(location) as newfile:
			for line in newfile.readlines():
				if "Version" in line:
					newver = parseutil.parseLine_Sep(line,"Version", ":").strip()
					break
		print "pci.ids updated: Version %s > %s" % (oldver, newver)