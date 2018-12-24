# NLP Question Detector for Toucan AI
# Author: Maria E. Garcia
# Email: megarcia1234@gmail.com

# import statements
from pycorenlp import StanfordCoreNLP
from nltk.tree import Tree
import string
#from nltk.parse.stanford import StanfordDependencyParser

# needed to run StanfordCoreNLP server
nlp = StanfordCoreNLP('http://localhost:9000')


def question_classifier(filePathIn, filePathOut):
########################################################################################################################
#
# This block of text opens text file, reads each line, and parses each line using Stanford Parser. If the annotated
# line contains clause label SBARQ or SQ, then the line is a question. If it is a question, a 1 is printed to its cor-
# responding line in a new file; if it is NOT a question, a 0 will print to its corresponding line in the file.
#
#  4 Question types included in this classifier are as follows:
#
#  SBARQ clause label indicates:
#       (1) WH-Questions (which contain an SQ clause as well)
#  SQ denotes
#       (2) Yes/No questions,
#       (3) Subject-less yes/no questions,
#       (4) Tag questions, and
#       (5) choice questions
#           (which basically are yes/no questions since first part is auxiliary verb followed by "or" and second choice)
#
#  Therefore, questions MUST contain SBARQ clauses, SQ clauses, or both clauses
#  Any line of text that does NOT contain the above is NOT a question
#  (indirect questions do not count as questions for the purpose of this classifier)
#
#   Cases not covered:
#   (1) indirect questions,
#   (2) questions that read like statements when no question mark present (e.g. "This is Japan" vs "This is Japan?")
#   (3)
#
# (Reference: "Bracketing Guidelines for Treebank II Style Penn Treebank Project", sections 1.2.5 - 1.2.6
# (URL: http://www.sfs.uni-tuebingen.de/~dm/07/autumn/795.10/ptb-annotation-guide/root.html)
# See also: https://preply.com/en/blog/2014/11/13/types-of-questions-in-english/
#
#######################################################################################################################
    with open(filePathIn) as fp:  # open text file and read line by line
        counter = 1
        print("Reading file 1:")
        translator = str.maketrans('', '', string.punctuation)          #   remove punctuation
        line = fp.readline()                                            #   ensure line is only read once
        classifiedText = open(filePathOut, 'a')
        # print labels on first line of classifiedText file
        classifiedText.write("SBARQ\tSQ\tCLASS\n")
        while line:
            print("Reading Line {}: {}".format( counter, (line.strip()).translate(translator)))
            outputRaw = nlp.annotate(line, properties={
                'annotators': 'tokenize,ssplit,pos,depparse,parse',
                'outputFormat': 'json'
            })
            parseTree = outputRaw['sentences'][0]['parse']
            label1Val = "0\t"  # SBARQ label
            label2Val = "0\t"  # SQ label
            label3Val = "0\t"  # Class label

            #print(parseTree) #used to test

            for i in Tree.fromstring(parseTree).subtrees():
                if i.label() == 'SBARQ':
                    print(i.leaves(), i.label())  # used for testing
                    label1Val = "1\t"
                    label3Val = "1\t"
                    print("SBARQ")
                elif i.label() == 'SQ':
                    print(i.leaves(), i.label())  # used for testing
                    label2Val = "1\t"
                    label3Val = "1\t"
                    print("SQ")
                else:
                    print(" ")
            classifiedText.write(label1Val + label2Val + label3Val + "\n")
            counter += 1
            print("Added 1 to counter")
            line = fp.readline()
    print("No more lines")
    classifiedText.close()
    fp.close()
    return


#MAIN

#question_classifier('trainingSents1.txt', 'classifiedSents1.txt')
#question_classifier('trainingSents2.txt', 'classifiedSents2.txt')
#question_classifier('trainingSents3.txt', 'classifiedSents3.txt')
question_classifier('test-inputs.txt', 'test-outputs.txt')