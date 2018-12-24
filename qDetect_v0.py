# NLP Question Detector for Toucan AI
# Author: Maria E. Garcia
# Email: megarcia1234@gmail.com

# import statements
from pycorenlp import StanfordCoreNLP
from nltk.tokenize import word_tokenize
import spacy
import csv

# needed to run StanfordCoreNLP server
nlp = StanfordCoreNLP('http://localhost:9000')

nlp2 = spacy.load('en_core_web_sm')

filePath = 'example2.txt'  # use example file for debugging, then training text files when classifier ready
filePathOut = 'annotatedEx2.txt'

########################################################################################################################
#
# This block of text opens text file, reads and turns each line into annotated Tree and writes it to new text file,
#  with a \r\n at the end of each Tree to help in next step
#
# Data preprocessing/cleaning is done outside of this code since assignment prompt indicated we are to assume the input
# string to have no end-punctuation
#
#######################################################################################################################
with open(filePath) as fp:  # open text file and read line by line
    counter = 0
    print("Reading file:")
    line = fp.readline()
    # print("Line {}: {}".format(counter, line.strip()))
    while line:
        print("Reading Line {}: {}".format(counter, line.strip()))
        # ptree = ParentedTree.fromstring(format(counter, str(nlp.parse(line.split()))))    # used for testing
        # resultTree = nlp.parse(line.split())                                               # used for testing
        outputRaw = nlp.annotate(line, properties={
            'annotators': 'tokenize,ssplit,pos,depparse,parse',
            'outputFormat': 'json'
        })
        # print(outputRaw['sentences'][0]['parse'])                                              # used for testing

        annotatedEx2 = open(filePathOut, 'a')
        annotatedEx2.write(outputRaw['sentences'][0]['parse'])
        annotatedEx2.write("\r\n")

        ###########################################################
        #
        # played around with semgrex to find syntactic clause tags
        #
        ##########################################################
        # nlp.semgrex(line, pattern='{tag: SBARQ}', filter=False)                               # used for testing
        # targetStr = 'SBARQ'
        # print("Start if loop")
        # if targetStr in result:
        #     print("\nIt's a WH or YN question")
        #     print("End IF loop")
        # else:
        #     print("Not a question")
        ##########################################################

        counter += 1
        print("Added 1 to counter")
        line = fp.readline()
    annotatedEx2.close()

########################################################################################################################
#
# This block of text takes annotated Tree from text file and writes it to new text file as single line, using \r\n
# to distinguish each flattened tree (single line) from the next
#
#######################################################################################################################
# code to turn tree into 1 line, tokenized, with parentheses removed
# then we search each line forSBAR, SBARQ, CC + Or, and 2nd to last word NEG
filePathOut2 = 'annotatedEx2Flat.txt'
filePath2 = 'annotatedEx2.txt'
with open(filePath2) as fp2:
    counter = 0
    print("Reading file:")
    contents = fp2.read()
    file_as_list = contents.splitlines()  # word_tokenize
    for line in file_as_list:
        annotatedEx2Flat = open(filePathOut2, 'a')
        tokenizedLine = word_tokenize(line)
        parenthRemoved = tokenizedLine.strip('()')
        doc = nlp2(parenthRemoved)
        block = []
        for token in doc:
            tagWord = token.text
            block.append(tagWord)
            if tagWord == "SBAR" or token.text == "SBARQ":   # this covers question types 1 and 2
                questionBool = '1\n'
                block.append(questionBool)
                annotatedEx2Flat.write(block)
            elif tagWord == "SINV":                           # this covers question types 3 and 4
                if (t.text for t in doc) == "NEG":
                    questionBool = '1\n'
                    block.append(questionBool)
                    annotatedEx2Flat.write(block)
                elif (t.text for t in doc) == "or":
                    questionBool = '1\n'
                    block.append(questionBool)
                    annotatedEx2Flat.write(block)
                else:
                    questionBool = '0\n'
                    block.append(questionBool)
                    print "Not a type 3 or 4 question"                  # used for testing
            else:
                questionBool = '0\n'
                block.append(questionBool)
                print "Not a type 1 or 2 question"
        else:



annotatedEx2Flat.close()

########################################################################################################################
#
# This block of code is meant to search through each line of the flattened tree for markers/tags which indicate
# the statements are questions (see 4 types of questions below)
#
# The best way to do this is to use spacy to tokenize the flattened annotation text
#
# To search through for the 4 different tags which indicate the questions, set up if statements or cases that if tag
# for question type 1, 2, 3, or 4 is found, return a 1
# If none of the tags were found, return a 0, indicating text is not a question
# The number of lines in this new file (referred to as results.txt should match the number of lines in original file)
#
#######################################################################################################################
#   4 types of questions:
#       (1) WH Questions                -- indicated by SBARQ tag produced by Stanford Parser
#               ex. Questions which start with Who/What/When/Where/Why/How

#       (2) Yes/No Questions            -- indicated by SBAR tag
#               ex. Is it raining in Phoenix?
#
#       (3) Choice Questions            -- indicated by SINV tag followed by CC and Or
#               ex. Do you like the Atlanta Braves or Boston Red Sox better?
#
#       (4) Tag/disjunctive Questions   -- SINV and a NEG; edge case tested
#               ex. It is really cold out, isn't i?
#               edge case: Your father isn’t working today, is he?
#
########################################################################################################################
#
# This part of the code is meant to implement the classifier on the results.txt file
# LibSVM ws found to have the best results
#
######################################################################################################################


# End of code
