from dfs_block_crawler import dom_to_text_list
from langchain.text_splitter import TokenTextSplitter
from lxml import etree
from lxml.etree import HTMLParser
from dfs_block_crawler import dom_to_text_list

page2="""<body>
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
</body>"""

dom = etree.HTML(page2, parser=HTMLParser(remove_comments=True))
docs = dom_to_text_list(dom)
print(docs)