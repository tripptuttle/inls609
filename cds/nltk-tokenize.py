import xml.etree.ElementTree as et
import nltk
import os

inFilename = os.path.join(os.getcwd(), 'topics2016.xml')
outFilename = os.path.join(os.getcwd(),  'test.xml')
inFile = open('topics2016.xml', 'r')
outFile = open(outFilename, 'w')

tree = et.parse(inFile)
root = tree.getroot()

print(root.tag)

print(inFilename)