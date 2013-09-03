'''
Takes a PHPAdmin XML export of tiki_pages and concatenates the pages
based on a Table of Contents to determine the order.

phpMyAdmin XML Dump - version 3.3.10deb1 uses an attribute oriented
layout:

<database>
    <table name="tiki_pages">
        <column name="pageName">text</column>
        ...
        <column name="data">text</column>
        ...
    </table>
</database>

Created on Aug 31, 2013

@author: Benjamin
'''
import xml.etree.ElementTree as ET
import re

tree = ET.parse('C:/Downloads/tiki_pages.xml')
root = tree.getroot()

pages = {}


for page in(list(root.iter("table"))):
    columns = page.findall('column') 

    for column in columns:
        if('pageName' in column.attrib.values()):
            title = column.text
            #print(title)
        elif('data' in column.attrib.values()):
            content = column.text
        
    pages[title] = content

'''
# This commented out block was for element based parsing

pages = {}

# Add the pages to a dictionary, by title
for page in list(root):
    title = page.find('pageName').text
    content = page.find('data').text

    pages[title] = content
    
    # Load the Table of Contents to drive page order
    if(re.search(r'.*:table.*contents', title.lower())):
        toc = content
'''

# Use page 'VVP Table of Contents'
#     Page Names should be referenced as [Section] \t (([Prefix]:[Page Name]|[Friendly tite]))

# Build a list of contents that have supporting pages
#     Extract [Prefix]:[Page Name]
contents = [c[(c.find('((') + 2):c.find('|')] for c in pages['VVP:Table of Contents'].split('\n') if(re.search(r'\(.*\|.*\)', c))]

# Build the Table of Contents by stripping the markup
#     Extract [Section] \t [Page Name]
toc = [c[:c.find('|')].replace('((', '').replace('VVP:', '') for c in pages['VVP:Table of Contents'].split('\n') if(re.search(r'\(.*\|.*\)', c))]

# Add Table of Contents to output
output = 'Table of Contents\n\n' + '\n'.join(toc)

# Look for pages/sections to add to ouput
for item in contents:
    # Output the numbered section title
    for i in range(len(toc)):
        if toc[i].find(item.replace('VVP:', ''))!=-1:
            output += '\n\n\n' + toc[i]
                  
    # Add section to output    
    output += '\n\n' + pages.get(item, '') + '\n\n'

print(output)
