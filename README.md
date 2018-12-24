# ToucanAI-QDetector
A heuristic-based question detecting classifier

For this project I went back to first principles in order to understand the objective: take an input string from a file and be able to detect or classify it as a sentence or not. The most logical way to approach the problem is to define a question, grammatically, without having to rely on question marks.

The approach I took was then to try and understand and group together categories of questions. There are quite a few research papers which approach classifying question type in order to improve question answering systems. Some group questions by classifying the response such as the answer to “when is dinner ready?” would be a time, “where is the park?” would be a place, etc. After some reading I was able to come up with 5 distinct types of questions, based on their grammatical structures and in some cases based on the type of response. The five question types are as follows:

      (1) WH-Questions (which contain an SQ clause as well)
      (2) Yes/No questions
      (3) Subject-less yes/no questions
      (4) Tag questions
      (5) Choice questions (which are basically yes/no questions since first part is an auxiliary verb followed by "or" 
          and second choice
  
  Therefore, questions MUST contain SBARQ clauses, SQ clauses, or both clauses

  Any line of text that does NOT contain the above is NOT a question (indirect questions do not count as questions for the purpose of this classifier)

   <b>Cases not covered:</b>
   (1) indirect questions,
   (2) questions that read like statements when no question mark present (e.g. "This is Japan" vs "This is Japan?")

  <b>Cases rejected by classifier (using training datasets):</b>
   (1) Questions that start with "Given xyz, [WH Question goes here]
   (2) Questions that start with "Assuming xyz, [WH Question goes here]
   (3) 

  <b>Cases which gave false positives (using training datasets):</b>
   (1)

Reference: "Bracketing Guidelines for Treebank II Style Penn Treebank Project", sections 1.2.5 - 1.2.6
(URL: http://www.sfs.uni-tuebingen.de/~dm/07/autumn/795.10/ptb-annotation-guide/root.html)

See also: https://preply.com/en/blog/2014/11/13/types-of-questions-in-english/


Other approaches use tokenizers and/or parsers such as those available libraries such as NLTK and spaCy. In my search for a good parser I came across StanfordParser and the reason I chose it above the others was its ability to group by clause. I went with Stanford CoreNLP since it was easier to integrate using pycorenlp wrapper for python. It also offered advanced features.

Towards the end I had an issue with line 128 in the test inputs file, but I realized it was the sentence length that was crashing the CoreNLP server but solved the issue with a timeout value large enough to accommodate the large chunk of text
