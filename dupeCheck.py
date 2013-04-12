# encoding: utf-8
'''
dupeCheck locates identical files, by contents (using a hash), and removes them.

@author:     Benjamin
        
@copyright:  2013 COG. All rights reserved.        
@license:    GNU GPL

@contact:    benjamin@relativeprime.com
@deffield    updated: Updated
'''

import sys
import os
import hashlib
import optparse

DELETE = False # Determines whether files are deleted; set by '-r' 

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk

def check_for_duplicates(paths, hash=hashlib.sha1):
    hashes = {}
    deletes = []

    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                hashobj = hash()
                
                for chunk in chunk_reader(open(full_path, 'rb')):
                    hashobj.update(chunk)
                
                file_id = (hashobj.digest(), os.path.getsize(full_path))
                duplicate = hashes.get(file_id, None)
                
                if duplicate:
                    print("%s == %s" % (full_path, duplicate))
                    
                    if(DELETE == True):
                        if(duplicate not in deletes):
                            os.remove(duplicate)
                            
                            deletes.append(duplicate)
                else:
                    hashes[file_id] = full_path
    print('[Processed %d duplicates]' % (len(deletes)))

def main(argv=None): # IGNORE:C0111
    global DELETE
    
    '''Command line options.'''
    parser = optparse.OptionParser('usage %prog <path> '+ '-r')

    # Sets DELETE variable based on command line flag
    parser.add_option('-r', dest='flagDelete', default=False, action='store_true', help='specify remove files')

    (options, args) = parser.parse_args()

    if len(args) == 0:
        print(parser.usage)
        exit(0  )
    else:
        print('[Checking ' + sys.argv[1] + ']')
        
        if(options.flagDelete == True):
            print('[Removing files]')
            DELETE = True
        else:
            print('[Find only]')
            
        check_for_duplicates(sys.argv[1:])
        exit(0)

if __name__ == "__main__":
    sys.exit(main())
