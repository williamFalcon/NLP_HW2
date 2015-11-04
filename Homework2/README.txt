===========================================
WILLIAM FALCON - WAF2107
NLP - HW2
===========================================



-------------------------------------------
QUESTION 1:

A - Images: Images are located under Homerwork2/.
			They are: figure_en.png, figure_dn.png, figure_sw.png

B - In a projective dependency graph, lines do not cross over each other. If we see a graph were all the lines above the words do not cross another line, this graph is projective.

C - Projective Sentence:		root The giraffe ate the tiny lollipop.
	Non-projective Sentence:	root I crashed a car yesterday morning which was a cadillac.
-------------------------------------------



*******************************************
QUESTION 2:
A - Implementation complete.

B - Scores with the badfeatures model on swedish are:
	UAS: 0.229038040231 
	LAS: 0.125473013344

*******************************************



-------------------------------------------
QUESTION 3:
-------------------------------------------

A - To edit features, I added an svmfeatureoptimizer class. This class uses
    a single method to generate a test for whatever combination of subject/feature given.
    The subjects are either words in the stack or words in the buffer. Ex: STK_0, STK_1 (last and last-1 items on the stack)
    The number in the test gives the location of the subject to use.
    The first part gives the algorithm the data_source to use (stack or buffer)
    The last part tells the algorithm the data_field to use.

    The strategy I used was to generate similar fields for clusters of words in the stack and buffer, specifically the tags and words. Sometimes going deeper in the buffer
    than in the stack. THis makes sense because the parser conducts a look ahead on the stack and the buffer to make its decision. The most important fetures seem to be the stack_0 and buffer_0 words and tags. I achieved marked improvement when I 
    added the LDEP and RDEP (as added by the sample program and ok'd in piazza). For some languages, the performance was better when I didn't go too deep in the buffer, and limited the search scope to BUF_2.

    The FEATS tag seemed to lower the accuracy of the tagger. I imagine it added too much data for the svm to be effective.

    Complexity of adding these features was O(V*N) where V is the number of features to add, and N is the number of sentences.

    The following are the tests I ran for each language:


	Swedish model:
	Features = ['STK_-1_WORD_', 'STK_-1_TAG_', 'STK_-1_LEMMA_', 					'STK_-1_LDEP_', 'STK_-1_RDEP_',
	            'STK_-2_TAG_',
	            'BUF_0_WORD_', 'BUF_0_TAG_', 'BUF_0_LEMMA_', 'BUF_0_LDEP_', 'BUF_0_RDEP_',
	            'BUF_1_TAG_', 'BUF_1_WORD_',
	            'BUF_2_TAG_'
	           ]


	English model:
	Features = ['STK_-1_WORD_', 'STK_-1_TAG_', 'STK_-1_LEMMA_', 'STK_-1_LDEP_', 'STK_-1_RDEP_',
	            'STK_-2_TAG_',
	            'BUF_0_WORD_', 'BUF_0_TAG_', 'BUF_0_LEMMA_', 'BUF_0_LDEP_', 'BUF_0_RDEP_',
	            'BUF_1_TAG_', 'BUF_1_WORD_'
	           ]


	Danish model:
	Features = ['STK_-1_WORD_', 'STK_-1_TAG_', 'STK_-1_LEMMA_', 					'STK_-1_LDEP_', 'STK_-1_RDEP_',
	            'STK_-2_TAG_',
	            'BUF_0_WORD_', 'BUF_0_TAG_', 'BUF_0_LEMMA_', 'BUF_0_LDEP_', 'BUF_0_RDEP_',
	            'BUF_1_TAG_', 'BUF_1_WORD_',
	            'BUF_2_TAG_'
	           ]

B - Done. Model files in folder

C - Scores:

	Swedish
	Results:
		UAS: 0.790878311093 
		LAS: 0.682931686915

	Danish
	Results:
		UAS: 0.785660674517 
		LAS: 0.701795184132

D - The arc-eager shift-reduce parser has a O(N) complexity, where N is the number of words in the sentence.
	The parser is greedy because it makes the best decision it can think of and moves on from there. It is efficient because it does not backup or backtracks from it's decision.
	Generally a trade-off is that you also have to train an SVM (or similar classifier) to make the decisions (shift, reduce, left-arc, right-arc) for the parser. This can take a very long time if the model is too complex. This also adds the complexity of feature selection for the SVM, which in itself can be a very complex problem. 


	English
	Results:
		UAS: 0.748148148148 
		LAS: 0.708641975309

*******************************************
QUESTION 4:
*******************************************



