import re

CID = {}
knowledge = {}
keyword = {}


def read_sentence(file, writefile):
    fw = open(writefile, 'w')

    with open(file) as fp:
        passage = fp.readline()
        # 标注文章
        fw.write(passage)

        while len(passage) > 0:
            sentences = []

            line = fp.readline()
            while "passage" not in line and len(line) > 0:
                if line.startswith('title:') or line == 'abstract:\n' or line.startswith("CID"):
                    pass
                else:
                    if line.startswith('abstract'):
                        line = line[9:]
                    sentences.append(line)
                line = fp.readline()

            l = len(sentences)
            if l >= 2:
                for i in range(l):
                    for j in range(i + 1, l):
                        if contain_entity(sentences[i], sentences[j]):
                            ret = is_cid(sentences[i], sentences[j])
                            # order为True的
                            for c_d, cid in ret[0].items():
                                distance, total, start, end = cal_distance(sentences[i:j + 1], c_d[0], c_d[1])
                                entity = cal_entity(sentences[i:j + 1], start, end)
                                is_knowledge = in_knowledge(c_d[0], c_d[1])
                                key = keyword_count(sentences[i], sentences[j])
                                fw.write('%-8d%-8d%-16f%-16f%-8d%-8d%-8d%-8d%-8d%-8d\n' % (
                                    distance, total, start/len(sentences[i].split()), end/len(sentences[j].split()), j - i, entity, is_knowledge, key, 0, cid))
                            # order为False的
                            for c_d, cid in ret[1].items():
                                distance, total, start, end = cal_distance(sentences[i:j + 1], c_d[1], c_d[0])
                                entity = cal_entity(sentences[i:j + 1], start, end)
                                is_knowledge = in_knowledge(c_d[0], c_d[1])
                                key = keyword_count(sentences[i], sentences[j])
                                fw.write('%-8d%-8d%-16f%-16f%-8d%-8d%-8d%-8d%-8d%-8d\n' % (
                                    distance, total, end/len(sentences[j].split()), start/len(sentences[i].split()), j - i, entity, is_knowledge, key, 1, cid))
            passage = line
            fw.write(passage)


# 读取全部CID关系
def read_CID(file):
    with open(file) as fp:
        line = fp.readline()
        while len(line) > 0:
            if line.startswith("CID"):
                line = line.split()
                if line[1] in CID:
                    CID[line[1]].add(line[2])
                else:
                    CID[line[1]] = set([line[2]])
            line = fp.readline()


# 判断句对中是否包含实体对
def contain_entity(sentence1, sentence2):
    sentence1 = sentence1.split()
    sentence2 = sentence2.split()

    chemical1 = False
    disease1 = False
    for word in sentence1:
        if "C_D" in word or "C_C" in word:
            chemical1 = True
        if "D_D" in word or "D_C" in word:
            disease1 = True

    chemical2 = False
    disease2 = False
    for word in sentence2:
        if "C_D" in word or "C_C" in word:
            chemical2 = True
        if "D_D" in word or "D_C" in word:
            disease2 = True

    if (chemical1 == True and disease2 == True) or (chemical2 == True and disease1 == True):
        return True
    else:
        return False


# 返回全部实体对及判断是否为CID关系.
def is_cid(sentence1, sentence2):
    result = []
    chemical1, disease1 = get_chemical_disease(sentence1)
    chemical2, disease2 = get_chemical_disease(sentence2)

    result1 = get_cid(chemical1, disease2)
    result.append(result1)
    result2 = get_cid(chemical2, disease1)
    result.append(result2)

    return result


# 获取句子中的化学物质和疾病
def get_chemical_disease(sentence):
    chemical, disease = [], []

    sentence = sentence.split()
    for word in sentence:
        if "C_D" in word or "C_C" in word:
            pattern = re.compile(r'C_D[-]*\d+|C_C[-]*\d+')
            match = pattern.search(word)
            if match:
                chemical.append(match.group())
        if "D_D" in word or "D_D" in word:
            pattern = re.compile(r'D_D[-]*\d+|D_C[-]*\d+')
            match = pattern.search(word)
            if match:
                disease.append(match.group())

    return chemical, disease


# 判断实体对是否为CID关系
def get_cid(chemical, disease):
    result = {}
    for c in chemical:
        for d in disease:
            if c in CID and d in CID[c]:
                result[(c, d)] = 1
            else:
                result[(c, d)] = 0

    return result


# 计算两实体间的距离,及句子的总距离
def cal_distance(line, entity1, entity2):
    count = 0
    start = location(line[0], entity1)
    count += len(line[0].split()) - start
    end = location(line[-1], entity2)
    count += end

    for i in range(1, len(line) - 1):
        count += len(line[i].split())

    total = 0
    for i in range(0, len(line)):
        total += len(line[i].split())

    return count, total, start, end


# 计算实体句中位置
def location(sentence, entity):
    sentence = sentence.split()
    for i in range(len(sentence)):
        if entity in sentence[i]:
            return i
    return -1


# 计算实体对间实体的个数
def cal_entity(line, start, end):
    count = 0
    for i in range(start + 1, len(line[0].split())):
        word = line[0].split()[i]
        pattern = re.compile(r'C_D[-]*\d+|C_C[-]*\d+|D_D[-]*\d+|D_C[-]*\d+')
        match = pattern.search(word)
        if match:
            count += 1
    for i in range(0, end):
        word = line[-1].split()[i]
        pattern = re.compile(r'C_D[-]*\d+|C_C[-]*\d+|D_D[-]*\d+|D_C[-]*\d+')
        match = pattern.search(word)
        if match:
            count += 1

    for i in range(1, len(line) - 1):
        for j in range(0, len(line[i].split())):
            word = line[i].split()[j]
            pattern = re.compile(r'C_D[-]*\d+|C_C[-]*\d+|D_D[-]*\d+|D_C[-]*\d+')
            match = pattern.search(word)
            if match:
                count += 1

    return count


# 获取全部知识
def knowledge_get():
    global knowledge

    with open('data/knowledge.txt') as fp:
        line = fp.readline().split()
        while len(line) > 0:
            c_pattern = re.compile(r'C\d+|D\d+')
            c_match = c_pattern.search(line[0])
            if c_match:
                chemical = c_match.group()[1:]

            d_pattern = re.compile(r'D\d+|C\d+')
            d_match = d_pattern.search(line[1])
            if d_match:
                disease = d_match.group()[1:]

            if chemical in knowledge:
                knowledge[chemical].add(disease)
            else:
                knowledge[chemical] = set([disease])
            line = fp.readline().split()


# 判断是否在知识中
def in_knowledge(c, d):
    global knowledge

    c = c[3:]
    d = d[3:]
    if c in knowledge:
        if d in knowledge[c]:
            return True
    return False


# 获取全部的关键词
def keyword_get():
    global keyword
    with open("data/keyword.txt") as fp:
        line = fp.readline()
        while len(line) > 0:
            line = line.split()
            keyword[line[0]] = int(line[1])
            line = fp.readline()


def keyword_count(start, end):
    global keyword

    line = [start, end]
    for word in line:
        words = re.split(r'[\s\,\;\.\|\-\(\)\?\:\\/]+', word)
        count = 0
        for word in words:
            for key in keyword:
                if key in word:
                    count += keyword[key]

    return count


if __name__ == '__main__':
    file_list = ["data/corpus/TrainSet.txt", "data/corpus/DevelopSet.txt"]
    write_list = ["data/result/train_out_result.txt", "data/result/develop_out_result.txt"]

    knowledge_get()
    keyword_get()

    for file, fw in zip(file_list, write_list):
        read_CID(file)
        read_sentence(file, fw)

        # read_CID('data/test.txt')
        # read_sentence("data/test.txt", 'data/result.txt')
