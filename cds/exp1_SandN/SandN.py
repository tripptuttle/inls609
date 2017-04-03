import xml.etree.ElementTree as et
import nltk
import string
from natsort import natsorted, ns
import os

# function parses XML tree, tokenizes and removed stopwords and punctuation and returns a dictionary object
def get_xml_text(filename, parent_element, child_element): #tokenizes the elements
    inFile = open(filename, 'r')  # creates file object with inFile
    tree = et.parse(inFile)  # creates an element tree object of the inFile XML
    root = tree.getroot()  # determines root of XML
    xmlOutput = {} # initializes the array which will hold topicNum:processedText
    for topic in root.findall(parent_element): # loops through each parent element
        key = str(topic.get('number'))
        value = topic.find(child_element).text # returns text within the child element
        xmlOutput[key] = value
    return xmlOutput

def tokenize_text(dictionary):
    cleanOutput = {}
    tknzr = nltk.TweetTokenizer() # defines the tokenizer - in this case, a casual language processor, more available at nltk.org
    for key, value in dictionary.items():
        tokenText = tknzr.tokenize(value)
        cleanText = []
        for word in tokenText:
            cleanWord = word
            for item in string.punctuation:
                cleanWord = cleanWord.replace(str(item), ' ')
            cleanWord = cleanWord.strip(string.punctuation).lower()
            cleanWord = cleanWord.strip()
            if cleanWord:
                cleanText.append(cleanWord)
        dictionary[key] = ' '.join(map(str, cleanText))
    return dictionary


# function parses array of topic numbers (key) and text (values) and outputs it in the trec query format
# you can modify the output.append() statements to change the method used by indri #combine, etc.

def write_to_trec_format_twoDicts(filename, dictionary1, weight1, dictionary2, weight2, dir):
    outFile = open(os.path.join(dir, filename), 'w')
    output = []
    outFile.write('<parameter>\n')
    for key in natsorted(dictionary1.keys()): # key is topic number, value is processed text from element specified in process_xml_text()
        outFile.write('<query>\n')
        outFile.write('\t<number>' + key + '</number>\n')
        outFile.write('\t<text>\n')
        outFile.write('\t\t#weight( ' + str(weight1) + ' #combine(' + dictionary1[key] + ')\n')
        outFile.write('\t\t' + str(weight2) + ' #combine(' + dictionary2[key] + '))\n')
        outFile.write('\t</text>\n')
        outFile.write('</query>\n')
    outFile.write('</parameter>\n')
    outFile.close()
    generate_bsub_file(filename, dir)


def write_to_trec_format(name, dictionary, dir):
    outFile = open(os.path.join(dir, (name + '.xml')), 'w')
    outFile.write('<parameter>\n')
    for key in natsorted(dictionary.keys()): # key is topic number, value is processed text from element specified in process_xml_text()
        outFile.write('<query>\n')
        outFile.write('\t<number>' + key + '</number>\n')
        outFile.write('\t<text>\n')
        outFile.write('\t\t#combine(' + dictionary[key] + ')\n')
        outFile.write('\t</text>\n')
        outFile.write('</query>\n')
    outFile.write('</parameter>\n')
    outFile.close()
    generate_bsub_file(filename, dir)


def generate_bsub_file(filename, dir='/webdex/expir/'):
    bsubFileName = filename.strip('.xml')
    bsubExt = bsubFileName + '.bsub'
    bsubFile = open(os.path.join(dir, bsubExt), 'w')
    bsubFile.write('#BSUB -J spell-notesAndSpell\n#BSUB -q day\n#BSUB -o ' + dir + '/' + filename + '.output')
    bsubFile.write('\n/webdex/expir/indri/indri-5.4/runquery/IndriRunQuery ' + dir + '/' + filename + ' -index=/webdex/expir/index/pmc -count=1000 -trecFormat=true > ' + dir + '/' + bsubFileName + '.results')
    bsubFile.write('\n/webdex/expir/script/trec_eval.9.0/trec_eval -q /webdex/expir/corpus/pmc/qrels.txt ' + dir + '/'  + bsubFileName + '.results >' + dir + '/'  + bsubFileName + '.stats')
    bsubFile.close()

dir = '/webdex/expir/ttuttle/cds/ttuttle/exp1_SandN'

summaryDict = tokenize_text(get_xml_text('topics2016.xml', 'topic', 'summary')) #xml file, parent element, and child element you want to process

notesDict = tokenize_text(get_xml_text('topics2016.xml', 'topic', 'note'))

write_to_trec_format_twoDicts('SandN_1to2.xml', summaryDict, 1, notesDict, 2, dir)
write_to_trec_format_twoDicts('SandN_1to1.xml', summaryDict, 1, notesDict, 1, dir)
write_to_trec_format_twoDicts('SandN_2to1.xml', summaryDict, 2, notesDict, 1, dir)
write_to_trec_format('SandN_summary.xml', summaryDict, dir)
write_to_trec_format('SandN_notes.xml', notesDict, dir)

