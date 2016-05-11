from lxml import etree as ET
doc = ET.Element("function_locations")
ET.SubElement(doc, "fun", module="blah", name='hi')
ET.SubElement(doc, "fun", module="asdfasd", name='by')
tree = ET.ElementTree(doc)
tree.write("filename.xml")