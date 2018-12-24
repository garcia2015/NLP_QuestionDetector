# NLP Question Detector for Toucan AI
# Author: Maria E. Garcia
# Email: megarcia1234@gmail.com

# import statements
from pycorenlp import StanfordCoreNLP
from nltk.tree import Tree
#from nltk.parse.stanford import StanfordDependencyParser


# needed to run StanfordCoreNLP server
nlp = StanfordCoreNLP('http://localhost:9000')


filePathIn1 = 'example.txt'  # use example file for debugging, then training text files when classifier ready
filePathOut1 = 'annotatedText.txt'
filePathOut2 = 'classifiedText.txt'
########################################################################################################################
#
# This block of text opens text file, reads each line, and parses each line using Stanford Parser. If the annotated
# line contains clause label SBARQ or SQ, then the line is a question. If it is a question, a 1 is printed to its cor-
# responding line in a new file; if it is NOT a question, a 0 will print to its corresponding line in the
#
# Data preprocessing/cleaning is done outside of this code since assignment prompt indicated we are to assume the input
# string to have no end-punctuation
#
#######################################################################################################################
with open(filePathIn1) as fp:  # open text file and read line by line
    counter = 0
    print("Reading file 1:")
    line = fp.readline()

    while line:
        print("Reading Line {}: {}".format(counter, line.strip()))

        outputRaw = nlp.annotate(line, properties={
            'annotators': 'tokenize,ssplit,pos,depparse,parse',
            'outputFormat': 'json'
        })

        annotatedText = open(filePathOut1, 'a')
        classifiedText = open(filePathOut2, 'a')
        #print labels on first line of classifiedText file
        classifiedText.write("SBARQ SQ CLASS\n")

        parseTree = outputRaw['sentences'][0]['parse']
        for i in Tree.fromstring(parseTree).subtrees():
            if i.label() == 'SBARQ':
                print(i.leaves(), i.label())  # used for testing
                annotatedText.write("SBARQ\n")
                classifiedText.write("1 0 1\n")
            elif i.label() == 'SQ':
                print(i.leaves(), i.label())  # used for testing
                annotatedText.write("SQ\n")
                classifiedText.write("0 1 1\n")
            else:
                annotatedText.write("None\n")
                classifiedText.write("0 0 0\n")
        counter += 1
        print("Added 1 to counter")
        line = fp.readline()
    annotatedText.close()
    classifiedText.close()
fp.close()