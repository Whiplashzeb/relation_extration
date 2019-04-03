import nltk.data
from nltk.tokenize import word_tokenize


class Replace:
    """处理原始数据，替换其中的化学物质和疾病实体"""

    def __init__(self, raw_file, replace_file):
        self.raw_file = raw_file
        self.replace_file = replace_file
        self.tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
        self.passages = []
        self.repalce_passages = []
        self.cids = []

    def get_passage(self):
        """
        切分原始语料，存储每篇文章相关信息
        """
        with open(self.raw_file) as fp:
            first = fp.readline()
            while len(first) > 0:
                passage = []
                number = first.partition('|t|')[0]
                passage.append(number)
                title = first.partition('|t|')[2]
                passage.append(title)
                abstract = fp.readline().partition('|a|')[2]
                passage.append(abstract)

                entity = fp.readline()
                while len(entity) > 1:
                    passage.append(entity)
                    entity = fp.readline()
                first = fp.readline()
                self.passages.append(passage)

    def replace_entity(self):
        """
        替换每篇文章中的实体并存储替换后文章以及标准的实体对
        """
        for passage in self.passages:
            number = passage[0]
            raw_passage = passage[1] + passage[2]
            replace_passage = raw_passage

            cid = {}
            for entity in passage[3:]:
                entity = entity.split()
                l = len(entity)
                # 处理实体对
                if l >= 6:
                    start, end = int(entity[1]), int(entity[2])  # 替换实体在文章中的位置
                    if entity[l - 2] == 'Chemical':
                        if '|' in entity[l - 1]:  # 处理等价情况
                            entity[l - 1] = self.__equals(entity[l - 1], 'C_')
                        replace_passage = replace_passage.replace(raw_passage[start:end], 'C_' + entity[l - 1])
                    elif entity[l - 2] == 'Disease':
                        if '|' in entity[l - 1]:
                            entity[l - 1] = self.__equals(entity[l - 1], 'D_')
                        replace_passage = replace_passage.replace(raw_passage[start:end], 'D_' + entity[l - 1])
                # 存储CID关系
                if l == 4:
                    chemical = 'C_' + entity[2]
                    disease = 'D_' + entity[3]
                    if chemical in cid:
                        cid[chemical].add(disease)
                    else:
                        cid[chemical] = set([disease])
            # 对替换后的文章做tokenization
            result = []
            token = self.tokenizer.tokenize(replace_passage)
            for words in token:
                sentence = ' '.join(word_tokenize(words))
                result.append(sentence)
            replace_passage = passage[0] + '\n' + '\n'.join(result)

            self.repalce_passages.append(replace_passage)
            self.cids.append(cid)

    def store_passage(self):
        with open(self.replace_file, 'w') as fp:
            for replace_passage, cid in zip(self.repalce_passages, self.cids):
                fp.write(replace_passage + '\n')
                for c, ds in cid.items():
                    for d in ds:
                        fp.write("%s\t%s\n" % (c, d))
                fp.write('\n')

    def __equals(self, entity, flag):
        result = []
        for en in entity.split('|'):
            result.append(flag + en)
        result[0] = result[0][2:]
        return '|'.join(result)


if __name__ == "__main__":
    raw_file_list = ["data/raw/train.txt", "data/raw/develop.txt", "data/raw/test.txt"]
    replace_file_list = ["data/replace/train.txt", "data/replace/develop.txt", "data/replace/test.txt"]

    for raw_file, replace_file in zip(raw_file_list, replace_file_list):
        replace = Replace(raw_file, replace_file)
        replace.get_passage()
        replace.replace_entity()
        replace.store_passage()
