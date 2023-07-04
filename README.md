# Block Based Crawler for Semantic Search

## The Algorithm

The algorithm has two parts: text scrapping and link mining.


### Text Scrapping

A depth first tree search algorithm is implemtened to traverse DOM nodes found in an HTML document. If a DIV block is met, a new split is created and all contained text is included. 

If a block of text is too long, it is splitted into overlapping chunks.

A set of previous text blocks is kept so that a text block is added only if it passes duplication check. Block based scrapping allows repetition check which is not possible with the plain scrapping.

### Link Mining

All links in a page are put into a list.
Links in the list are visited one by one and scrapped in the way.


## Example 

Following blocks shows two html text presumably belongs to two different page of a website. Content is copied from britannica.

```html
<body>
  <div>Britannica contains a lot of information.</div>
<div>

  <h1>Europe Countries</h1>
  <div>
    <h2>Germany
    </h2>
    <p>Germany, officially Federal Republic of Germany, German Deutschland or Bundesrepublik Deutschland, country of north-central Europe, traversing the continent’s main physical divisions, from the outer ranges of the Alps northward across the varied landscape of the Central German Uplands and then across the North German Plain.
    </p>
  </div>

  <div>
    <h2>France
    </h2>
    <p>France, officially French Republic, French France or République Française, country of northwestern Europe. Historically and culturally among the most important nations in the Western world, France has also played a highly significant role in international affairs, with former colonies in every corner of the globe.
    </p>
  </div>

</div>
</body>
```

```html
<body>
  <div>Britannica contains a lot of information.</div>
  <div>

  <h1>Asia Countries</h1>
  <div>
    <h2>China
    </h2>
    <p>China, Chinese (Pinyin) Zhonghua or (Wade-Giles romanization) Chung-hua, also spelled (Pinyin) Zhongguo or (Wade-Giles romanization) Chung-kuo, officially People’s Republic of China or Chinese (Pinyin) Zhonghua Renmin Gongheguo or (Wade-Giles romanization) Chung-hua Jen-min Kung-ho-kuo, country of East Asia. It is the largest of all Asian countries and has the largest population of any country in the world. 
    </p>
  </div>

  <div>
    <h2>India
    </h2>
    <p>India, country that occupies the greater part of South Asia. Its capital is New Delhi, built in the 20th century just south of the historic hub of Old Delhi to serve as India’s administrative centre. Its government is a constitutional republic that represents a highly diverse population consisting of thousands of ethnic groups and likely hundreds of languages.
    </p>
  </div>
  </div>
</body>
```

Chunk size is selected as 100 and overlap as 20.

### Plain Scrapping

```python
['\nBritannica contains a lot of information.\n\nEurope Countries\n\nGermany\n    \nGermany, officially Federal Republic of Germany, German Deutschland or Bundesrepublik Deutschland, country of north-central Europe, traversing the continent’s main physical divisions, from the outer ranges of the Alps northward across the varied landscape of the Central German Uplands and then across the North German Plain.\n    \n\n\nFrance\n ',
 'plands and then across the North German Plain.\n    \n\n\nFrance\n    \nFrance, officially French Republic, French France or République Française, country of northwestern Europe. Historically and culturally among the most important nations in the Western world, France has also played a highly significant role in international affairs, with former colonies in every corner of the globe.\n    \n\n\n',
 '\n    \n\n\n']

```

```python
['\nBritannica contains a lot of information.\n\nAsia Countries\n\nChina\n    \nChina, Chinese (Pinyin) Zhonghua or (Wade-Giles romanization) Chung-hua, also spelled (Pinyin) Zhongguo or (Wade-Giles romanization) Chung-kuo, officially People’s Republic of China or Chinese (Pinyin) Zhonghua Renmin Gongheguo',
 's Republic of China or Chinese (Pinyin) Zhonghua Renmin Gongheguo or (Wade-Giles romanization) Chung-hua Jen-min Kung-ho-kuo, country of East Asia. It is the largest of all Asian countries and has the largest population of any country in the world. \n    \n\n\nIndia\n    \nIndia, country that occupies the greater part of South Asia. Its capital is New',
 '   \nIndia, country that occupies the greater part of South Asia. Its capital is New Delhi, built in the 20th century just south of the historic hub of Old Delhi to serve as India’s administrative centre. Its government is a constitutional republic that represents a highly diverse population consisting of thousands of ethnic groups and likely hundreds of languages.\n    \n\n\n']
```

Note that common text mentioning Britannica is included in both pages. 

Also note that word france follows definition germany. And definition of france starts with some text from germany part.

Similarly definition of china includes parts from india definition. By mere coincidence last element contains information only about india. Note that some text is overlapping in 2nd and 3rd elements.



### Block Scrapping


```python
['Britannica contains a lot of information.',
 'Germany: Germany, officially Federal Republic of Germany, German Deutschland or Bundesrepublik Deutschland, country of north-central Europe, traversing the continent’s main physical divisions, from the outer ranges of the Alps northward across the varied landscape of the Central German Uplands and then across the North German Plain.',
 'France: France, officially French Republic, French France or République Française, country of northwestern Europe. Historically and culturally among the most important nations in the Western world, France has also played a highly significant role in international affairs, with former colonies in every corner of the globe.',
 'Europe Countries:']
```


```python
['China: China, Chinese (Pinyin) Zhonghua or (Wade-Giles romanization) Chung-hua, also spelled (Pinyin) Zhongguo or (Wade-Giles romanization) Chung-kuo, officially People’s Republic of China or Chinese (Pinyin) Zhonghua Renmin Gongheguo or (Wade-Giles romanization) Chung-hua Jen-min Kung-ho-',
 'India: India, country that occupies the greater part of South Asia. Its capital is New Delhi, built in the 20th century just south of the historic hub of Old Delhi to serve as India’s administrative centre. Its government is a constitutional republic that represents a highly diverse population consisting of thousands of ethnic groups and likely hundreds of languages.',
 'Asia Countries:',
 ' (Wade-Giles romanization) Chung-hua Jen-min Kung-ho-kuo, country of East Asia. It is the largest of all Asian countries and has the largest population of any country in the world.']
```

Note that common text is only included in the first page. 

Splits are shorter than they are in regular scrapping. As a result there are more chunks.

Sections defining countries are not overlapping. The only overlap occurs in definition of china because it is too long and needs to be split. 


