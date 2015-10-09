# ADB-Project-1
COMS 6111 Advanced Database Systems Project 1: Relevance Feedback

By:

Xuejun Wang, UNI: xw2355

Akshaan Kakar, UNI: ak3808

## Essential Information

### List of Files in Submission
<pre><code>
dyn-160-39-205-135:ADB-Project-1 AmyWang$ tree
.
├── LICENSE
├── MainScript.py
├── README.md
├── ScoringSystem.py
├── ScoringSystem.pyc
├── TermParamsClass.py
├── TermParamsClass.pyc
├── VectorSpaceClass.py
├── VectorSpaceClass.pyc
├── key.json
├── resources
│   └── english
└── transcript.txt
</code></pre>

######Additional Remark: 
1. Bing Search API accountKey is in file <code>key.json</code> and it is in the submission directory
2. The transcript contains our results for 3 required test cases, and additional test case 'columbia' for Columbia University at required precision@10 0.9


### Compile/ Run Instructions
1. <code>key.json</code> is the file that stores Bing Search API accountKey. Make sure it is under the same file path as <code>MainScript.py</code>. The file is in following format:<pre><code>{"accountKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"}</code></pre>
2. From terminal, change file path to the project root folder
3. Run the project using following command format: <pre><code>python MainScript.py -q 'your query' -p 0.9</code></pre>
4. When asked for relevance feedback, input n/N/y/Y are all going to be accepted, any other characters will not be recognised and you will be prompted to input until the project receives acceptable character


## Internal Design
Purpose of each class and the input output they need

&

sample of datastructure used(inverted file list, termParams, termweights vectors, etc)


## Query Modification Mechanism

Inverted file list

&

Rocchio

&

Decision on words to add and when to add two words, when to add one


## References

1. Stop-word corpus was borrowed as-is from the NLTK toolkit.  
   Bird, Steven, Edward Loper, and Ewan Klein. "Natural Language Processing with Python." Http://www.nltk.org/nltk_data/. O'Reilly Media, n.d. Web. <http://www.nltk.org/nltk_data/>.
