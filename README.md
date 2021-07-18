# FirstOrderLogicResolution

## Task:
1. The task is to decide the entailment of a query sentence in a given KB. 
2. Given an input of the form, 

<N = NUMBER OF QUERIES>
<QUERY 1>
…
<QUERY N>
<K = NUMBER OF GIVEN SENTENCES IN THE KNOWLEDGE BASE>
<SENTENCE 1>
…
<SENTENCE K>

For each query, determine if that query can be inferred from the knowledge base or not, one 
query per line:

<ANSWER 1>
.
.
.
\<ANSWER N\>

Each answer should be either TRUE if you can prove that the corresponding query sentence is 
true given the knowledge base, or FALSE if you cannot.

## Implementation Details:
1. Firstly, every sentence in the KB is converted to CNF Form.
2. The First order logic resolution logic utilizes multiple techniques such as unit resolution, factorization, depth-first-search to decide entailment of a given query. 
3. Unit Tests for every python script and integration tests have been added.
