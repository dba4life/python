#!/usr/bin/env python3
'''
Converts specified PDFs that contain a checklist to an HTML table
'''
__author__ = "Benjamin Monk"
__copyright__ = "Copyright 2013, COG Industries"
__credits__ = ["PDFMiner3k", "Stack Overflow"]
__license__ = "GPL"
__version__ = "1.0"

import sys
import io
import getopt
import os.path

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.pdfdevice import TagExtractor
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

def main(argv):
    def usage():
        print(('usage: %s [-d directory] [-P password] [-n filename pattern]' % argv[0]))
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'P:n:d:')
    except getopt.GetoptError:
        return usage()

    # input option
    password = ''
    pagenos = set()

    # output option
    pattern = ''
    outfile = None
    outtype = 'text'
    outdir = None
    layoutmode = 'normal'
    codec = 'utf-8'
    pageno = 1
    scale = 1
    caching = True
    showpageno = True
    laparams = LAParams()
    inputDirectory = None

    for (k, v) in opts:
        print('%s -> %s' % (k ,v))
        if k == '-P': password = v
        elif k == '-n': pattern = v
        elif k == '-d': inputDirectory = v

    rsrcmgr = PDFResourceManager(caching=caching)

    # Create StringIO object to trick PDF Miner into not writing to file
    pdfTxt = io.StringIO()
    outfp = pdfTxt

    device = TextConverter(rsrcmgr, outfp, laparams=laparams)

    # Specify processing directory, defaulting to current directory
    if(inputDirectory):
        folder = os.path.abspath(inputDirectory)
    else:
        folder = os.path.abspath(argv[0])

    # Start the html output
    print('<htlm><head></head><body><table border="1">')
        
    # Cycle through all PDFs in directory, convert PDFs to text
    for filename in os.listdir(folder):
        if(filename.lower().endswith('.pdf') and pattern.lower() in filename.lower()):
            # Cleanup filename
            checklist = ''
            checkList = filename.replace('eplc_', '').replace('_checklist.pdf', '')
            checkList = checkList.replace('_', ' ').title()
            
            # Add path to filename
            filename = os.path.join(folder, filename)
            
            # Open PDF
            fp = io.open(filename, 'rb')
            
            # Extract text
            process_pdf(rsrcmgr, device, fp, pagenos, password=password,
                        caching=caching, check_extractable=True)
            
            fp.close()        
            
            # Convert StringIO to actual string
            str = pdfTxt.getvalue()
            
            # Strip untranslateable unicode
            str = str.replace('\u2019', '')
            str = str.replace('\u201c', '')
            str = str.replace('\u201d', '')
            str = str.replace('\u2022', '')
            str = str.replace('\uf0b7', '')
            
            # Cleanup anomalies
            str = str.replace('W ill', 'Will')
            str = str.replace('Change Management Checklist (One Time Activities)', '')
            str = str.replace('Communications Management Checklist', '')

            # Strip leadin text (and 'activities checklist'
            str = str[str.find('Activities Checklist') + 20:]

            # Some files have a checklist intro; strip it            
            if('This section' in str):
                str = str[str.find('continued use of this template.') + 31:].strip()
                if(str.startswith('Checklist')):
                    str = str[str.find('Checklist') + 9:]

            # Strip final text and whitespace
            str = str[:str.rfind('?') + 1].strip()

            # Determine checklist items
            itemParticle = ['Has', 'Have', 'Do', 'What', 'Will', 'Are', 'If', 'Is']

            # Check for checklist items; break into rows, labeled with checklist name            
            for item in itemParticle:
                str = str.replace('\n' + item, '</td></tr><tr><td>' + checkList + '</td><td>' + item)
            
            # Add initial row tags and final row tags
            str = '<tr><td>' + checkList + '</td><td>' + str + '</td></tr>'
            
            # Output checklist table
            print(str)
            
            # Clear out PDF text object
            pdfTxt.truncate(0)

    device.close()
    
    # Close html
    print('</table></body></html>')

if __name__ == '__main__':
    sys.exit(main(sys.argv))
