import xml.etree.cElementTree as ET
import os
if not os.path.exists("locations.xml"):
	root = ET.Element("root")
	tree = ET.ElementTree(root)
	tree.write("locations.xml")

class Locations:
	def __init__(self):
		self.tree = ET.parse('locations.xml')
		self.root = self.tree.getroot()
	
	def get(self, location):
		"""
		Returns the Location object if it exists, otherwise returns None.
		"""
		cur = None
		for i in self.root:
			if i.get('name')==location:
				cur=i
				break
		return cur
	
	def addLocation(self, name, lat, lng):
		attrib={
			"name": name,
			"lat": str(lat),
			"lng": str(lng)
		}
		ET.SubElement(self.root, "location", attrib)
	
	def removeLocation(self, alias):
		for i in self.root:
			if i.get('name') == alias:
				self.root.remove(i)
				return True
		return False
	
	def close(self):
		self.tree.write("locations.xml")
	
	def __del__(self):
		pass
		self.close()