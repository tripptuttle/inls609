import trechelpers as h # imports the trechelpers.py file - see if for detailed comments

dir = 'exp_test1' # local dir for output, relative to the location of this file
KDdir = '/webdex/expir/ttuttle/cds/exp_test' # directory on KillDevil where you'll have all files
name = 'test1-A' # file name pattern for output files
trecXML = 'topics2016.xml' # specify name of original trecXML file, must be in same directory as this file


originalQueries1 = h.get_xml_text(trecXML, 'topic', 'summary') # builds array of summary text
originalQueries2 = h.get_xml_text(trecXML, 'topic', 'description') # builds array of description text
originalQueries3 = h.get_xml_text(trecXML, 'topic', 'note') # builds array of notes


# tokenize all the queries and return a dictionary of queryNumber:text
# see trechelpers.py on ways to customize it
tokenizedQueries1 = h.tokenize_text(originalQueries1)
tokenizedQueries2 = h.tokenize_text(originalQueries2)
tokenizedQueries3 = h.tokenize_text(originalQueries3)

# removes basic stopwords from the stop_words module from a dictionary's values
# you can add optional parameter to specify another list with your own chosen stopwords
removedStopwordsQueries1 = h.remove_stopwords(tokenizedQueries1)


# checks spelling of text, adding the ceiling percentage specified of suggested words to the query
spellcheckQueries3 = h.check_spelling(tokenizedQueries3, 0.50)

# writes to trec format the two passed dictionaries (arrays) and sets them with an indri weight of 1,
# and 2 respectively, XML query file will be output in directory specified
# if you want to output to two separate files, you'll need to modify the name to avoid overwriting
# the first output xml file.
h.write_to_trec_two(name, tokenizedQueries1, removedStopwordsQueries1, 1, 2, dir)
h.write_to_trec_one(name + '_option2', removedStopwordsQueries1, dir)


# generates bsub file which has commands to run the queries, then calculate stats
h.generate_bsub_file(name, KDdir, dir)

