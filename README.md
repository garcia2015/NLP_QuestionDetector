# NLP_QuestionDetector
A heuristic-based, binary question classifier

1. [Read before running code](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/README.md#read-before-running-code)
2. [Intro](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/README.md#intro)
3. [Approach](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/README.md#approach)
4. [Datasets](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/README.md#datasets)
5. [Code](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/README.md#code)
6. [Results](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/README.md#results)
7. [Areas for Improvement](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/README.md#areas-for-improvement)

## Intro ##

For this project I went back to first principles in order to understand the objective: take an input string from a file and be able to detect or classify it as a sentence or not. The most logical way to approach the problem is to define a question, grammatically, without having to rely on question marks.

## Approach ##

My first step was to review academic journals to figure out which approaches have provided the most accurate results. There are quite a few research papers which approach classifying question type in order to improve question answering systems. Some group questions by classifying the response such as the answer to “when is dinner ready?” would be a time, “where is the park?” would be a place, etc. Most papers I read used Li and Roth's research (see research papers section) from 2004 and built on that; Sangodiah et al did a good review of the state-of-the-art in 2015 which reviewed all the approaches tried since. This was all research concerned with classifying question types, but nothing in the realm of differentiating between questions and non-questions.

Sangodiah's review along with my own research led me to the conclusion that clause-level syntactic parsing along with SVM classifier produced the best results when it came to coarse-grained classification of question types. This was not the exercise at hand, so it would be a starting point. 

I reviewed the synctactic parsing covered in the papers I read. When trying to identify a parser or POS tagger that would lead me to the common tags found in questions, I found that clause level tags are very useful as they follow this pattern. I was able to come up with 5 distinct types of questions, based on their grammatical structures and in some cases based on the type of response. The five question types are as follows:
 *(It is worth noting that for the purposes of this exercise, indirect questions are not considered questions)*
 
 ```
      (1) WH Questions                 ---> SBARQ
      (2) Yes/No questions             ---> SQ
      (3)Subject-less yes/no questions ---> SQ
      (4)Tag questions                 ---> SQ
      (5)Choice questions              ---> SQ
          -- basically yes/no questions since first part is an auxiliary verb followed by "or" and second choice
 ```
 Reference: "Bracketing Guidelines for Treebank II Style Penn Treebank Project", sections 1.2.5 - 1.2.6
            URL: http://www.sfs.uni-tuebingen.de/~dm/07/autumn/795.10/ptb-annotation-guide/root.html
  
 See also: https://preply.com/en/blog/2014/11/13/types-of-questions-in-english/
   
            
 Therefore, questions *MUST* contain **SBARQ** clauses, **SQ** clauses, or **both** clauses.
 
 Any line of text that does NOT contain the above is NOT a question (indirect questions do not count as questions for the purpose of this classifier). There are additional exceptions below.
 
 **Cases not covered:**
```
   (1) indirect questions,
   (2) questions that read like statements when no question mark present (e.g. "This is Japan" vs "This is Japan?")
```
 Other approaches use tokenizers and/or parsers such as those available libraries such as NLTK and spaCy. In my search for a good parser I came across StanfordParser and the reason I chose it above the others was its ability to group by clause. I went with Stanford CoreNLP since it was easier to integrate using pycorenlp wrapper for python. It also offered other advanced features.

In the end, a heuristic-based approach made the most sense as differentiating between statements and non-statements (questions) is simpler and less nuanced than question classification. 



## Datasets ##

###### Training data ######
- [Input files (training)](https://github.com/garcia2015/NLP_QuestionDetector/tree/master/training_data)

The training dataset(s) came from the Sentence Corpus at http://archive.ics.uci.edu/ml/machine-learning-databases/00311/ from the UCI ML repository. The files used for this project were from the arxiv_unlabeled articles, expecting over 95% of the text to be non-questions; from the .txt files I selected 1.txt through 51.text and turned it into 1 long file, with each sentence ending in a newline char. Then I divided it into 3 sections: trainingSents1.txt, trainingSents2.txt, and trainingSents3.txt to expedite testing.

I chose this dataset before I decided on my heuristics-only approach; my intent was to have as many instances of non-questions as questions to prevent imbalanced classes in my ML model. I also planned to use the labeled question dataset provided by Li and Roth at http://cogcomp.org/Data/QA/QC/. 

###### Test Data ######
- [Input file (test)](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/test-inputs.txt)

## Code ##
- [Shell](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/qDetect.sh)
- [Final version, Python](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/qDetect_v3.py)

- [Previous versions](https://github.com/garcia2015/NLP_QuestionDetector/tree/older-versions)

## Results ##

###### Results of training dataset classification ######
I went over the output of the classified training data line by line (572 lines) and compared to the original text. I made some annotations along the way on whether or not the text was correctly or incorrectly classified as a question. There were a few false negatives and false positives. See the next section on rejected cases. 
- [Output file (training)](ToucanAI-QDetector/classifiedSents_annotated.txt)

**Cases rejected by classifier (using training datasets):**
```
   (1) Questions that start with "Given xyz, [WH Question goes here]
   (2) Questions that start with "Assuming xyz, [WH Question goes here]
```
**Cases which gave false positives (using training datasets):**
```
   (1) Example: "It should not be limited to any particular set of senses, environments or goals, nor should it be limited to 
        any specific kind of hardware, such as silicon or biological neurons"
```
###### Results of test dataset classification ######
There was exactly 1 extra line in the output file, to allow for the labels row: SBARQ, SQ, and CLASS. I removed it manually after uploading to repository for ease of review/audit.

- [Output file](https://github.com/garcia2015/NLP_QuestionDetector/blob/master/test-outputs.txt)
      
I had an issue with line 128 in the test inputs file, but I realized it was the sentence length that was crashing the CoreNLP server but solved the issue with a timeout several orders of magnitude large enough to accommodate the large chunk of text going through the CoreNLP server. This happened again around the 4000th line and again at line 8221. 

I selected a few lines of the output to audit. One of the incorrectly classified lines from the test file was line 1381, "What triggers a slow killing response." This is an example of a WH-question, and thus an SBARQ clause tag should be present. However when I tested it on the CoreNLP parser website it labeled the clause as SBAR rather than SBARQ. After trying it on the StanfordParser site, it was tagged correctly as SBARQ.

## Areas for improvement ##
I'd spend time testing other versions of StanfordCoreNLP and StanfordParser to see which one could catch the WHPP clauses that escaped the version I used as well as the cases rejected by the classifier in the training dataset. Compare both and see which one has higher rates of FP vs FN. I could also do some further statistical analysis to truly evaluate the performance of this classifier anf provide some AUC and acuracy graphs.
  
  
## Read before running code ##

To run this code you will need:
- To make sure StanfordCoreNLP is installed (v.3.9.2) (download folder name: stanford-corenlp-full-2018-10-05)
- Python 3.6 or later



