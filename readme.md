**I'm posting some helper scripts and my result sets for my project in Jaime Arguello's
[INLS 609 (Spring 2017) Experimental Information Retrieval](https://ils.unc.edu/courses/2017_spring/inls609_001/)**

For our project, we are performing the [TREC 2016 CDS Track](http://trec-cds.org)

The [trechelpers.py](trechelpers.py) file has highly-commented, but probably not that well formed scripts that work
to automate some of the basic tasks we need to do to prepare our TREC runs including:

* get_xml_text(): Parsing an XML tree and pulling the query text into an array (Python dictionary)
* tokenize_text(): Tokenizing the text, and removing all punctuation (there's probably a much cleaner method than what I used ;-))
* check_spelling(): Checking if the words in a given string are an English word - if not, adding likely replacements to the end of the query.
* write_to_trec_one(): Writing any given dictionary to the Indri TREC-format query XML
* write_to_trec_two(): Writing any two given dictionaries with shared keys into the Indri TREC-format query XML, with weights set differently (or the same) for each dictionary text.
* generate_bsub_file(): Creating a bsub file for each iteration which can be used in LSF on KillDevil to automate the long RunQuery and calcuate stats

The [example.py](example.py) file shows how to call the helper functions from the trechelpers.py file.

Feel free to adapt to your needs, but please fork and share back so I can learn from those of you who are more experienced programmers.