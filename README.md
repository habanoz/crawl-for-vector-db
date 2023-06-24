# A DIV based website crawler for Semantic Search 

Semantic search mostly requires text to be split into chunks. This is necessary because LLMs have a limited context size. 
Even if context size were unlimited sending large texts to an LLM would be wasteful because it would increase the cost of using LLMs. 
Considering the fact that only a small section of the text is relevant to a query, this cost increase is not necessary.

For these reasons, regular crawlers are not suitable for semantic search. 

DIV blocks can be used as abstraction blocks. 
It is safe to assume different div blocks contain text which tries to explain different topics. 
If div blocks are not kept the nuance in the text is lost.
Thus different div block texts should be regarded as different documents.

This repository contains a DIV-based depth-first-search crawler. It is simple. 
It can be extended for specific purposes.
e.g. for some text using p blocks may be more relevant.


