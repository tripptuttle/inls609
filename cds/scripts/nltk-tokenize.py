import xml.etree.ElementTree as et
import nltk
import string
from natsort import natsorted, ns
import enchant

d = enchant.Dict("en_US")

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

def checkSpell(dictionary):
    for key, value in dictionary.items():
        addlWords = d.suggest(value)
        if addlWords:
            dictionary[key] = dictionary[key] + addlWords
        return dictionary


# function parses array of topic numbers (key) and text (values) and outputs it in the trec query format
# you can modify the output.append() statements to change the method used by indri #combine, etc.

def write_to_trec_format(filename, dictionary):
    outFile = open(filename, 'w')
    output = []
    outFile.write('<parameter>\n')
    for key in natsorted(dictionary.keys()): # key is topic number, value is processed text from element specified in process_xml_text()
        outFile.write('<query>\n')
        outFile.write('\t<number>' + key + '</number>\n')
        outFile.write('\t<text>\n')
        outFile.write('\t\t#combine(' + dictionary[key] + ')\n')
        outFile.write('\t</text>\n')
        outFile.write('</query>\n')
    outFile.write('</parameter>\n')


dict = get_xml_text('topics2016.xml', 'topic', 'summary') #xml file, parent element, and child element you want to process

processedText = tokenize_text(dict)

write_to_trec_format('test-summary-parse4.xml', processedText)

