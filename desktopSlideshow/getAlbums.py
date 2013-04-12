# Import Picasa albums
# 	google picasa list-albums --owner <Google account> | cut -d, -f 1
# 	google picasa get "$album" 
import subprocess

owner = 'google account name'

# Retrieve list of album names
proc = subprocess.Popen(['google', 'picasa', 'list-albums', '--owner', owner],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

# Process the albums
for line in proc.stdout : 

	# Split line into [Album name], [URL]
	album = line.split(',')
	subprocess.call(['google', 'picasa', 'get', album[0], '--dest', '.'])

