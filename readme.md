I'm posting some helper scripts and my result sets for my project in Jaime Arguello's
INLS609 Experimental Information Retrieval.

The trechelpers.py file has highly-commented, but probably not that well formed scripts that work
to automate some of the basic tasks we need to do to prepare our TREC runs including:

* get_xml_text(): Parsing an XML tree and pulling the query text into an array (Python dictionary)
* tokenize_text(): Tokenizing the text, and removing all punctuation (there's probably a much cleaner method than what I used ;-))
* check_spelling(): Checking if the words in a given string are an English word - if not, adding likely replacements to the end of the query.
* write_to_trec_one(): Writing any given dictionary to the Indri TREC-format query XML
* write_to_trec_two(): Writing any two given dictionaries with shared keys into the Indri TREC-format query XML, with weights set differently (or the same) for each dictionary text.
* generate_bsub_file(): Creating a bsub file for each iteration which can be used in LSF on KillDevil to automate the long RunQuery and calcuate stats


The example.py file shows how to call the helper functions from the trechelpers.py file.

Feel free to adapt to your needs, but if possible, fork this repo so I can learn from those of you
who are more experienced programmers.



import trechelpers as h # imports the trechelpers.py file - see if for detailed comments

dir = 'exp_test1' # local directory you want things to be placed in
KDdir = '/webdex/expir/ttuttle/cds/exp_test' # directory on KillDevil where you'll have all files
name = 'test1-A' # file name pattern for output files

originalQueries1 = h.get_xml_text('topics2016.xml', 'topic', 'summary') # builds array of summary text
originalQueries2 = h.get_xml_text('topics2016.xml', 'topic', 'description') # builds array of description text
originalQueries3 = h.get_xml_text('topics2016.xml', 'topic', 'notes') # builds array of notes

tokenizedQueries1 = h.tokenize_text(originalQueries1)
tokenizedQueries2 = h.tokenize_text(originalQueries2)
tokenizedQueries3 = h.tokenize_text(originalQueries2)

# writes to trec format the two passed dictionaries (arrays) and sets them with an indri weight of 1,
# and 2 respectively, XML query file will be output in directory specified
h.write_to_trec_two(name, tokenizedQueries1, tokenizedQueries2, 1, 2, dir)


# generates bsub file which has commands to run the queries, then calculate stats
h.generate_bsub_file(name, KDdir, dir)

