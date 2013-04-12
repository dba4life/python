import subprocess
from lxml import etree

# create XML
#<?xml version="1.0" encoding="UTF-8"?>
#<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">


wallpapers = etree.Element('wallpapers')

wallpaper = etree.SubElement(wallpapers, "wallpaper")
name = etree.SubElement(wallpaper, "name")
name.text = 'Picasa Albums'

filename = etree.SubElement(wallpaper, "filename")
filename.text = '.local/share/backgrounds/wallpaper1/slideshow.xml'

options = etree.SubElement(wallpaper, "options")
options.text = 'scale'

pcolor = etree.SubElement(wallpaper, "pcolor")
pcolor.text = '#2c001e'

scolor = etree.SubElement(wallpaper, "scolor")
scolor.text = '#2c001e'

shade_type = etree.SubElement(wallpaper, "shade_type")
shade_type.text = 'solid'

tree = etree.ElementTree(wallpapers)



#<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">
# pretty string
s = etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8', doctype='<!DOCTYPE wallpapers SYSTEM "gnome-wp-list.dtd">')

print s

