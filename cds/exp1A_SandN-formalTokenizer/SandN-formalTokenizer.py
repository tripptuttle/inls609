import trechelpers as h

dir = 'exp1A_SandN-formalTokenizer' # local dir for output, relative to the location of this file
KDdir = '/webdex/expir/ttuttle/cds/exp1A_SandN-formalTokenizer' # directory on KillDevil where you'll have all files
name = 'exp1A_SandN-formalTokenizer' # file name pattern for output files

notesDict = h.get_xml_text('topics2016.xml', 'topic', 'note')
summaryDict = h.get_xml_text('topics2016.xml', 'topic', 'summary')

notesDict = h.tokenize_text(notesDict)
summaryDict = h.tokenize_text(summaryDict)

notesDict = h.remove_stopwords(notesDict)
summaryDict = h.remove_stopwords(summaryDict)

notesDict = h.check_spelling(notesDict)

h.write_to_trec_two(name, summaryDict, notesDict, 1, 2, dir)
h.write_to_trec_two(name, summaryDict, notesDict, 1, 2, dir)
h.write_to_trec_two(name, summaryDict, notesDict, 2, 1, dir)
h.write_to_trec_one(name, summaryDict, dir)
h.write_to_trec_one(name, notesDict, dir)
