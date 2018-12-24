# ToucanAI-QDetector
A heuristic-based question detecting classifier



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
 
 Reference: "Bracketing Guidelines for Treebank II Style Penn Treebank Project", sections 1.2.5 - 1.2.6
            URL: http://www.sfs.uni-tuebingen.de/~dm/07/autumn/795.10/ptb-annotation-guide/root.html
  
 See also: https://preply.com/en/blog/2014/11/13/types-of-questions-in-english/
 ```  
            
 Therefore, questions *MUST* contain **SBARQ** clauses, **SQ** clauses, or **both** clauses.
 
 Any line of text that does NOT contain the above is NOT a question (indirect questions do not count as questions for the purpose of this classifier). There are additional exceptions below.
 
 **Cases not covered:**
```
   (1) indirect questions,
   (2) questions that read like statements when no question mark present (e.g. "This is Japan" vs "This is Japan?")
```
 Other approaches use tokenizers and/or parsers such as those available libraries such as NLTK and spaCy. In my search for a good parser I came across StanfordParser and the reason I chose it above the others was its ability to group by clause. I went with Stanford CoreNLP since it was easier to integrate using pycorenlp wrapper for python. It also offered other advanced features.

In the end, a heuristic-based approach made the most sense as differentiating between statements and non-statements (questions) is simpler and less nuanced than question classification. 
   
## Outcome of training dataset classification ##

  **Cases rejected by classifier (using training datasets):**
  ```
   (1) Questions that start with "Given xyz, [WH Question goes here]
   (2) Questions that start with "Assuming xyz, [WH Question goes here]
   (3) 
```
**Cases which gave false positives (using training datasets):**
  ```
   (1) "It should not be limited to any particular set of senses, environments or goals, nor should it be limited to 
        any specific kind of hardware, such as silicon or biological neurons"
```

## Outcome of test dataset classification ##

I had an issue with line 128 in the test inputs file, but I realized it was the sentence length that was crashing the CoreNLP server but solved the issue with a timeout value large enough to accommodate the large chunk of text. This happened again around the 4000th line and again at line 8221.

  
## Read before running program ##

To run this program you will need:
--to make sure StanfordCoreNLP is installed (v.3.9.2) (download folder name: stanford-corenlp-full-2018-10-05)
--Python 3.6 or later



