# NLP Question Detector for Toucan AI
# Author: Maria E. Garcia
# Email: megarcia1234@gmail.com

# import statements
from pycorenlp import StanfordCoreNLP
from nltk.tokenize import word_tokenize
import spacy
from spacy.tokens import Doc
from spacy.tokens import Token
import re
import csv

# needed to run StanfordCoreNLP server
nlp = StanfordCoreNLP('http://localhost:9000')

nlp2 = spacy.load('en_core_web_sm')

filePathIn1 = 'example2.txt'  # use example file for debugging, then training text files when classifier ready
filePathOut1 = 'annotatedEx2.txt'
filePathIn2 = filePathOut1
filePathOut2 = 'annotatedEx2Flat.txt'
########################################################################################################################
#
# This block of text opens text file, reads and turns each line into annotated Tree and writes it to new text file,
#  with a \r\n at the end of each Tree to help in next step
#
# Data preprocessing/cleaning is done outside of this code since assignment prompt indicated we are to assume the input
# string to have no end-punctuation
#
#######################################################################################################################
with open(filePathIn1) as fp:  # open text file and read line by line
    counter = 0
    print("Reading file 1:")
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

        annotatedEx2 = open(filePathOut1, 'a')
        annotatedEx2.write(outputRaw['sentences'][0]['parse'])
        annotatedEx2.write("\n")
        counter += 1
        print("Added 1 to counter")
        line = fp.readline()
    annotatedEx2.close()
fp.close()

########################################################################################################################
#
# This block of code turns tree into 1 line, tokenized, with parentheses removed
# then we search each line for SBAR, SBARQ, SINV + NEG, SINV + Or
# See next comment block for details on 4 types of questions
#
########################################################################################################################

with open(filePathIn2) as fp2:
    counter = 0
    print("Reading file 2:")
    line = fp2.readline()
    while line:
        annotatedEx2Flat = open(filePathOut2, 'a')
        print("This is line without brackets ")
        bracketsRemoved = line.strip("()[]")
        print(bracketsRemoved)
        doc = nlp2(bracketsRemoved)
        docStatement = Doc(doc.vocab, words=[t.text for t in doc])
        blockStr = ""
        print("This is first block of line")
        print(blockStr)
        tokens_text = [t.text for t in doc]
        while tokens_text:
            tagWord = tokens_text
            print("This is tagWord")
            print(tagWord)
            blockStr = blockStr + tagWord
            print("Block")
            print(blockStr)
            print("This is block after appending")
            print(blockStr)
            if tagWord == "SBAR" or token.text == "SBARQ":      # this covers question types 1 and 2
                questionLabel = '1\n'
                print("Tagword is SBAR or SBARQ and questionLabel is " + questionLabel)
            elif tagWord == "SINV":
                print("Tagword is SINV")                        # this covers question types 3 and 4
                if (t.text for t in doc) == "NEG":
                    questionLabel = '1\n'
                    print("SINV followed by NEG and questionLabel is " + questionLabel)
                elif (t.text for t in doc) == "or":
                    questionLabel = '1\n'
                    print("SINV followed by Or and questionLabel is " + questionLabel)
                else:
                    questionLabel = '0\n'
                    print("Not a type 3 or 4 question and questionLabel is " + questionLabel)        # used for testing
            else:
                questionLabel = '0\n'
                print("Not a question and questionLabel is " + questionLabel)
        else:
            blockStr = blockStr + questionLabel
            annotatedEx2Flat.write(blockStr)
            print("Doc complete:\n " + blockStr)
    else:
        print("File complete")
    print("No more lines in file left to read. Closing output file 2")
    annotatedEx2Flat.close()
print("Closing Input File 2")
fp2.close()
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
#
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
# from sklearn.svm import LinearSVC
# import pandas
#
# en_doc = en_nlp(u'' + question_to_predict)
# question_data = get_question_predict_features(en_doc)
# X_predict = pandas.get_dummies(question_data)
#
# y = dta.pop('questionLabel')
# dta.pop('blockStr')
#
# X_train = pandas.get_dummies(dta)   #get_dummies() function converts the actual values into dummy values or binary values

#
# additional code I was planning on modifying and implementing with StanfordCoreNLP
# parser at https://shirishkadam.com/category/2017/
######################################################################################################################


# End of code
