# ReadMe

- Python3
- 使用 nltk 库 + chardet
- Windows 系统可能要改 utils.py 里的路径
- 倒排索引一开始跑一遍就行了，后面再跑时需要注释掉
- 经过测试，Windows 系统下跑 VSM.json 有可能是空的，原因不明，可以用文件夹里的 VSM.json 

## 结构

```
IRProject
|_Reuters // 语料库文件夹
|
|_readme.txt // 就是你在读的这个
|
|_main.py // main
|_utils.py // 一些轮子，具体看注释
|_InvertedIndex.py // 倒排索引模块（构建/获取倒排索引，构建 VSM ）
|_BooleanQuery.py // 布尔检索
|_GlobbingQuery.py // 通配符检索(使用b-tree构建词典)
|_PhraseQuery.py // 短语检索
|_SpellingCorrect.py // 拼写纠正
|_Score.py // 评分
|_VBcompress.py // 使用VBcode进行索引压缩
|_topk.py // top-K
|_Synonyms // 同义词扩展
|
|_index.json // 跑出来的示例倒排索引
|_wordlist.json // 跑出来的示例词表
|_VSM.json // 跑出来的示例 VSM
|_VSM_sum.json // 跑出来的示例 tf-idf 胜者表
|_doc_size.json // 跑出来的示例文档词数表

```


