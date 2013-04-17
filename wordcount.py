# Determine word frequency within a Word document

import re, os, collections
import win32com.client as win32
from operator import itemgetter

# Instance of MS Word
word = win32.gencache.EnsureDispatch('Word.Application')

# Run MS Word in background
word.Visible = False

# Specify source document
infile = 'Handling of HI DOE Source System Audit Fields.docx'

doc = word.Documents.Open(os.getcwd()+'\\'+infile)

# Extract the text to a string
docText = doc.Content.Text

# Convert document string to lowercase list of words
wordList = re.findall(r"\w+", docText.lower())

# Delete stop words
stopWords = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']
wordList = [w for w in wordList if not w in stopWords]

# Create a counter of words
counts = collections.Counter(wordList)

# Sort by values
countSort = sorted(counts.items(), key=itemgetter(1), reverse=True)

# Output
for word, frequency in countSort:
    print("%s, %d" % (word, frequency))
