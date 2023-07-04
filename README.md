# A DIV based website crawler for Semantic Search 

Generating text splits according to DIV tags offers following benefits:
- Preserving logical structure in the document such that sub-documents has focused content.
- Web pages generally has a structure. This structure causes substantial text duplication. DIV based splitting allows easy removal of duplicates.
- Tag based splitting prevents text being split in the middle of sentences.

Content of DIV tags can be split again if they are too large. 
Overlapping chunks can be used to avoid incomplete text splits. 
DIV based approach requires less overlapped chunks. 

