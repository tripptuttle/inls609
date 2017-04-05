import math
import enchant
import nltk
import stop_words
import string
import os
from natsort import natsorted
import xml.etree.ElementTree as et



## function parses XML tree, returns a dictionary object to be used by other functions
## specify which parent element the child node you want to retrieve the text from, as well as
## the child element. By default, it will pull the summary text from the 'topic' XML element

def get_xml_text(filename, parent_element='topic', child_element='summary'):
    inFile = open(filename, 'r')  # creates file object with inFile
    tree = et.parse(inFile)  # creates an element tree object of the inFile XML
    root = tree.getroot()  # determines root of XML
    xmlOutput = {}  # initializes the array which will hold topicNum:processedText
    for topic in root.findall(parent_element):  # loops through each parent element
        key = str(topic.get('number'))
        value = topic.find(child_element).text  # returns text within the child element
        xmlOutput[key] = value
    return xmlOutput


## function iterates through each word in a passed dictionary and adds words not found
## in the dictionary to the end of the query text, you can control how many words are added
## by the optional percent parameter, by default it adds the ceiling of 20% of the words
## suggested by the enchant spell check.

def check_spelling(dictionary, percent=0.20):
    d = enchant.Dict("en_US")  # defines dictionary to use
    for key, value in dictionary.items():  # iterates through passed dictionary of query text
        addlWords = []
        for word in value.split():
            if not d.check(word):
                suggestions = d.suggest(word)
                if suggestions:
                    numInclude = math.ceil(len(suggestions) * percent)
                    addlWords.append(' '.join(suggestions[0:numInclude]))
        dictionary[key] = dictionary[key] + ' ' + ' '.join(addlWords)
    return dictionary


## function takes a dictionary/array of queryNumber : Text pairs and runs it through the
## NLTK plain language tokenizer, you can change the tokenizer used, see nltk.org for details

def tokenize_text(dictionary, tokenizer=nltk.TweetTokenizer()):
    tknzr = tokenizer  # sets the tokenizer used
    for key, value in dictionary.items():  # iterates through dictionary
        tokenText = tknzr.tokenize(value)  # tokenizes the text in the dictionary
        cleanText = []  # empty list for cleaned text
        for word in tokenText:  # removes all punctuation per indri specs
            cleanWord = word
            for item in string.punctuation:  # interates through list of punctuation, replaces with space
                cleanWord = cleanWord.replace(str(item), ' ')
            cleanWord = cleanWord.strip(
                string.punctuation).lower()  # removes list items that are only punct and makes LC
            cleanWord = cleanWord.strip()  # removes empty space
            if cleanWord:  # to ignore now empty list elements
                cleanText.append(cleanWord)  # adds word to list
        dictionary[key] = ' '.join(map(str, cleanText))  # writes list back out to dictionary
    return dictionary


## function merges two dictionaries with the same key into indri trec-formatted query file and allows
## you to set weight for Indri to give the text from each dictionary and writes the bsub file to
## call with 'bsub < "filename.bsub"' on Killdevil (you'll need to edit the
## write bsub function to point to your directory
## p.s. this is super lame code that doesn't even use an XMLobject, but it's easy :)

def write_to_trec_two(name, dictionary1, dictionary2, weight1=1, weight2=1, dir=''):
    w1 = str(weight1)
    w2 = str(weight2)
    if not os.path.exists(dir):
        os.makedirs(dir)
    outFile = open(os.path.join(dir, (name + '.xml')), 'w')
    outFile.write('<parameter>\n')
    for key in natsorted(dictionary1.keys()):
        outFile.write('<query>\n')
        outFile.write('\t<number>' + str(key) + '</number>\n')
        outFile.write('\t<text>\n')
        outFile.write('\t\t#weight( ' + str(weight1) + ' #combine(' + dictionary1[key] + ')\n')
        outFile.write('\t\t ' + str(weight2) + ' #combine(' + dictionary2[key] + '))\n')
        outFile.write('\t</text>\n')
        outFile.write('</query>\n')
    outFile.write('</parameter>\n')
    outFile.close()


## simply writes a dictionary out to indri trec-formatted query file
## p.s. this is super lame code that doesn't even use an XMLobject, but it's easy :)
def write_to_trec_one(name, dictionary, dir=''):
    outFile = open(os.path.join(dir, (name + '.xml')), 'w')
    outFile.write('<parameter>\n')
    for key in natsorted(dictionary.keys()):
        outFile.write('<query>\n')
        outFile.write('\t<number>' + str(key) + '</number>\n')
        outFile.write('\t<text>\n')
        outFile.write('\t\t#combine(' + dictionary[key] + ')\n')
        outFile.write('\t</text>\n')
        outFile.write('</query>\n')
    outFile.write('</parameter>\n')
    outFile.close()


## this function generates the bsub command file, based on the parameters passed and
## then you can call it on KillDevil with the ' bsub < "name.bsub" ' command.
## Defaults to the day queue and pwd, you can spec a directory from the location where you run it.

def generate_bsub_file(name, KDdir='', dir='', queue='day'):
    bsubFile = open(os.path.join(dir, (name + '.bsub')), 'w')
    bsubFile.write('#BSUB -J ' + name)
    bsubFile.write('\n#BSUB -q ' + queue)
    bsubFile.write('\n#BSUB -o ' + KDdir + '/' + name + '-%J.output')
    bsubFile.write(
        '\n/webdex/expir/indri/indri-5.4/runquery/IndriRunQuery ' + KDdir + '/' + name + '.xml -index=/webdex/expir/index/pmc -count=1000 -trecFormat=true > ' + KDdir + '/' + name + '.results')
    bsubFile.write(
        '\n/webdex/expir/script/trec_eval.9.0/trec_eval -q /webdex/expir/corpus/pmc/qrels.txt ' + KDdir + '/' + name + '.results >' + KDdir + '/' + name + '.stats')
    bsubFile.close()


## function removes stopwords based on the basic english list in


def remove_stopwords(dictionary, swords=''):
    if not swords:
        swords = stop_words.get_stop_words('english')
    for key, value in dictionary.items():
        newValue = []
        for word in value.split():
            if word not in swords:
                newValue.append(word)
        dictionary[key] = ' '.join(map(str, newValue))
    return dictionary




