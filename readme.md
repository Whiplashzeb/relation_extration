# 使用指南

1. **deal_corpus.py**
- 替换文章中的化学物质和疾病为MeSH@ID
- 统计训练集和开发集中的化学物质,疾病和CID关系


- 需要文件:data/raw_data/CDR_TrainingSet.txt;data/raw_data/CDR_DevelopmentSet.txt
- 生成文件:data/corpus/train.txt;data/corpus/develop.txt


- 训练集中共500篇文章,开发集中共504篇文章.
- 训练集中共标注出665种化学物质,649种疾病.开发集中共标注出660种化学物质,589种疾病.
- 训练集中共标注出344种CID关系,开发集中供标注出347种CID关系.
- 共标注出998种化学物质,882种疾病,527种CID关系.


2. **StanfordTest.java/Passage**
- 进行分句操作


- 需要文件:data/corpus/train.txt;data/corpus/develop.txt
- 生成文件:data/corpus/TrainSet.txt;data/corpus/DevelopSet.txt


- 训练集中共4600句,开发集中共4577句.


3. **inner_sentence.py**
- 读取文章中的每一句话,判断句子中是否存在实体对,对于句内存在实体对的句子,抽取句内的全部实体<br>
针对每一对实体计算实体在句内的位置,实体间距离,实体顺序,是否存在于知识特征中,是否存在CID关系.<br>
并计算该句的句长,和关键词获得的总分数.<br>
关键字为后来补充内容


- 需要文件:<br>
data/corpus/TrainSet.txt;data/corpus/DevelopSet.txt<br>
data/keyword.txt   保存抽取出的关键词及其权值<br>
data/knowledge.txt    保存CTD数据库中一百万对化学物质致病关系.<br>


- 生成文件:<br>
data/corpus/TrainSentence.txt;data/corpus/DevelopSentence.txt<br>
格式为:句子 化学物质 疾病 化学物质位置 疾病位置 距离 句长 顺序 关键词 知识 标题 CID


- 训练集中共3602句,开发集中共3833句


4. **keyword_sentence.py**
- 抽取全部正例中的句子,用作关键字统计


- 需要文件:data/corpus/TrainSentence.txt;data/corpus/DevelopSentence.txt
- 生成文件:data/corpus/keyword_sentence.txt


- 共3048句

5. **StanfordTest.java/keyword**
- 对句子进行分词,并去除词形变换,保留全部的单词


- 需要文件:data/corpus/keyword_sentence.txt
- 生成文件:data/corpus/keyword.txt

6. **keyword_count.py**
- 统计关键词,统计出现次数超过100次的并且全部为字母的单词,并且人工过滤代词,介词,连词等.


- 需要文件:data/corpus/keyword.txt
- 生成文件:data/keyword.txt


- 共31个词

7. **deal_sentence.py**
- 只保留文件中的句子,用作依存句法分析


- 需要文件:data/corpus/TrainSentence.txt;data/corpus/DevelopSentence.txt
- 生成文件:data/corpus/TrainDependSentence.txt;data/corpus/DevelopDependSentence.txt


8. **StanfordTest.java/dependency**
- 对每一句话进行句法分析,并生成依赖句法树


- 需要文件:data/corpus/TrainDependSentence.txt;data/corpus/DevelopDependSentence.txt
- 生成文件:data/corpus/train_dependecny.txt;data/corpus/develop_dependecny.txt

9. **deal_dependency.py**
- 获取实体对的依存距离及句法标注


- 需要文件:<br>
data/corpus/train_dependency.txt;data/corpus/develop_dependency.txt<br>
data/corpus/TrainSentence.txt;data/corpus/DevelopSentence.txt<br>
- 生成文件:<br>
data/corpus/TrainDependResult.txt;data/corpus/DevelopDependResult.txt


10. **annotate.py**
- 用于正例句法标记统计


- 需要文件:data/corpus/TrainDependResult.txt;data/corpus/DevelopDependResult.txt
- 生成文件:data/annotate.txt

11. **combine.py**
- 生成最终句内的特征
- 格式为:依存距离 依存句法树长度 句法标注值 句子 化学物质 疾病 化学物质位置 疾病位置 距离 句长 顺序 关键词 知识 标题 CID


- 需要文件:<br>
data/corpus/TrainSentence.txt;data/corpus/DevelopSentence.txt<br>
data/corpus/TrainDependResult.txt;data/corpus/DevelopDependResult.txt
- 生成文件:<br>
data/result/train_in_result.txt;data/result/develop_in_result.txt

12. **out_sentence.py**
- 跨句分析
- 针对每篇文章的摘要,选取其中的两句,统计跨句的实体对,针对存在实体对的句对,抽取全部的实体对<br>
针对每一对实体,计算实体间距离,跨句句长,化学物质在句内位置,疾病在句内位置,跨句数量,<br>实体对包含其他实体数量,是否在知识内,关键字得分,顺序,关键字得分


- 需要文件:data/corpus/TrainSet.txt;data/corpus/DevelopSet.txt
- 生成文件:data/result/train_out_result.txt;data/result/develop_out_result.txt





