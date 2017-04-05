import trechelpers as h # imports the trechelpers.py file - see if for detailed comments

dir = 'exp_test1' # local directory you want things to be placed in
KDdir = '/webdex/expir/ttuttle/cds/exp_test' # directory on KillDevil where you'll have all files
name = 'test1-A' # file name pattern for output files


originalQueries1 = h.get_xml_text('topics2016.xml', 'topic', 'summary') # builds array of summary text
originalQueries2 = h.get_xml_text('topics2016.xml', 'topic', 'description') # builds array of description text
originalQueries3 = h.get_xml_text('topics2016.xml', 'topic', 'note') # builds array of notes


# tokenize all the queries, see trechelpers.py on ways to customize it
tokenizedQueries1 = h.tokenize_text(originalQueries1)
tokenizedQueries2 = h.tokenize_text(originalQueries2)
tokenizedQueries3 = h.tokenize_text(originalQueries3)


# checks spelling of text, adding the ceiling percentage specified of suggested words to the query
spellcheckQueries3 = h.check_spelling(tokenizedQueries3, 0.50)

# writes to trec format the two passed dictionaries (arrays) and sets them with an indri weight of 1,
# and 2 respectively, XML query file will be output in directory specified
h.write_to_trec_two(name, tokenizedQueries1, tokenizedQueries2, 1, 2, dir)


# generates bsub file which has commands to run the queries, then calculate stats
h.generate_bsub_file(name, KDdir, dir)

