import subprocess
import random
from lxml import etree

# create XML
background = etree.Element('background')

# Start time for Slideshow
starttime = etree.SubElement(background, "starttime")
year = etree.SubElement(starttime, "year")
year.text = '2013'

month = etree.SubElement(starttime, "month")
month.text = '01'

day = etree.SubElement(starttime, "day")
day.text = '01'

hour = etree.SubElement(starttime, "hour")
hour.text = '00'

minute = etree.SubElement(starttime, "minute")
minute.text = '00'

second = etree.SubElement(starttime, "second")
second.text = '00'


# Retrieve list of album names
proc = subprocess.Popen(['find', '~/Pictures', '-type', 'f'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

lastFile = ""
fileList = []

# Process the albums; adding to list
for line in proc.stdout : 
	# Add to array
	fileList.append(line.rstrip('\n'))

# Randomize the order
random.shuffle(fileList)

# Generate XML
for line in fileList :
	if(lastFile == "") :
		veryFirst = line

	# Static element
	static = etree.SubElement(background, "static")
	duration = etree.SubElement(static, "duration")
	duration.text = '300.0'
	filename = etree.SubElement(static, "file")
	filename.text = line

	# Transition element
	if(lastFile > ""):
		transition = etree.SubElement(background, "transition")
		duration = etree.SubElement(transition, "duration")
		duration.text = '5.0'
		fromFile = etree.SubElement(transition, 'from')
		fromFile.text = lastFile

		toFile = etree.SubElement(transition, "to")
		toFile.text = line

	lastFile = line

# Wrap back to first item
# Static element
static = etree.SubElement(background, "static")
duration = etree.SubElement(static, "duration")
duration.text = '300.0'
filename = etree.SubElement(static, "file")
filename.text = veryFirst

# Transition element
if(lastFile > ""):
	transition = etree.SubElement(background, "transition")
	duration = etree.SubElement(transition, "duration")
	duration.text = '5.0'
	fromFile = etree.SubElement(transition, 'from')
	fromFile.text = lastFile

	toFile = etree.SubElement(transition, "to")
	toFile.text = veryFirst

# pretty string
s = etree.tostring(background, pretty_print=True)
print s

