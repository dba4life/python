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
#import StringIO

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.pdfdevice import TagExtractor
#from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
# from pdfminer.utils import set_debug_logging

def main(argv):
    def usage():
        print(('usage: %s [-d directory] [-P password] [-o output file] [-O output directory] [-n filename pattern] file ...' % argv[0]))
        return 100
    try:
        #(opts, args) = getopt.getopt(argv[1:], 'dp:m:P:o:CnAVM:L:W:F:Y:O:t:c:s:')
        (opts, args) = getopt.getopt(argv[1:], 'P:o:O:n:')
    except getopt.GetoptError:
        return usage()

    if not args: return usage()

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

    for (k, v) in opts:
        if k == '-P': password = v
        elif k == '-o': outfile = v
        elif k == '-O': outdir = v
        elif k == '-n': pattern = v

    rsrcmgr = PDFResourceManager(caching=caching)

    # Create StringIO object to trick PDF Miner into not writing to file
    pdfTxt = io.StringIO()
    outfp = pdfTxt

    device = TextConverter(rsrcmgr, outfp, laparams=laparams)

    # TODO: Change to variable, defaulting to current directory
    folder = os.path.dirname(argv[0])

    # Start the html output
    print('<htlm><head></head><body><table border="1">')
        
    # Cycle through all PDFs in directory, convert PDFs to text
    for filename in os.listdir(folder):
        if(filename.lower().endswith('.pdf') and pattern.lower() in filename.lower()):
            print('Processing %s' % filename)
            fp = io.open(filename, 'rb')
            process_pdf(rsrcmgr, device, fp, pagenos, password=password,
                        caching=caching, check_extractable=True)
            
            fp.close()        
            
            # Cleanup filename
            checklist = ''
            checkList = filename.replace('eplc_', '').replace('_checklist.pdf', '')
            checkList = checkList.replace('_', ' ').title()
            
            # Convert StringIO to actual string
            str = pdfTxt.getvalue()
            
            # Strip untranslateable unicode
            str = str.replace('\u2019', '')
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
