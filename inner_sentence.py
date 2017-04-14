# 处理句内实体对 标记 句子 化学物质 疾病 化学物质位置 疾病位置 距离 句长 顺序 标题 CID
import re

CID = {}
keyword = {}
knowledge = {}


def read_sentence(file, writefile):
    fw = open(writefile, 'w')

    with open(file) as fp:
        passage = fp.readline()
        # 标注文章
        fw.write(passage)
        while len(passage) > 0:
            line = fp.readline()
            while "passage" not in line and len(line) > 0:
                if line == 'title:\n' or line == 'abstract:\n' or line.startswith("CID"):
                    pass
                else:
                    # 标注是否在标题内,并去除前面的标注
                    if line.startswith('title'):
                        line_flag = 0
                        line = line[6:]
                    elif line.startswith('abstract'):
                        line_flag = 1
                        line = line[9:]

                    if contain_entity(line):
                        result = is_CID(line)

                        k_count = keyword_count(line)
                        # 统计所有包含实体对的句子,并标注出具体实体对
                        for c_d, flag in result.items():
                            if_knowledge = in_knowledge(c_d[0], c_d[1])
                            ret = distance_and_order_cal(line[:-1], c_d[0], c_d[1])
                            # 标记 句子 化学物质 疾病 化学物质位置 疾病位置 距离 句长 顺序 关键词 知识 标题 CID
                            fw.write("%s\t\t%s\t\t%s\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\t\t%d\n" % (
                                line[:-1], c_d[0], c_d[1], ret[0], ret[1], ret[2], ret[3], ret[4], k_count,
                                if_knowledge, line_flag,
                                flag))
                line = fp.readline()
            fw.write('\n')
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


# 判断是否包含实体对
def contain_entity(sentence):
    sentence = sentence.split()

    chemical = False
    disease = False
    for word in sentence:
        if "C_D" in word or "C_C" in word:
            chemical = True
        if "D_D" in word or "D_C" in word:
            disease = True

    if chemical == True and disease == True:
        return True
    else:
        return False


# 抽取全部实体对及标注是否为CID关系
def is_CID(sentence):
    chemical = []
    disease = []

    result = {}
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

    for c in chemical:
        for d in disease:
            if c in CID and d in CID[c]:
                result[(c, d)] = 1
            else:
                result[(c, d)] = 0
    return result


# 计算实体间距离,顺序及句长
def distance_and_order_cal(sentence, chemical, disease):
    c_pos = 0
    d_pos = 0
    sentence = sentence.split()
    l = len(sentence)
    for i in range(l):
        if chemical in sentence[i]:
            c_pos = i
        if disease in sentence[i]:
            d_pos = i
    if c_pos > d_pos:
        order = 1
    else:
        order = 0
    result = [c_pos, d_pos, abs(c_pos - d_pos), l, order]

    return result


# 获取全部的关键词
def keyword_get():
    global keyword
    with open("data/keyword.txt") as fp:
        line = fp.readline()
        while len(line) > 0:
            line = line.split()
            keyword[line[0]] = int(line[1])
            line = fp.readline()


# 计算一句话的关键词总值
def keyword_count(word):
    global keyword

    words = re.split(r'[\s\,\;\.\|\-\(\)\?\:\\/]+', word)
    count = 0
    for word in words:
        for key in keyword:
            if key in word:
                count += keyword[key]

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


# 判断是否在知识内
def in_knowledge(c, d):
    global knowledge

    c = c[3:]
    d = d[3:]
    if c in knowledge:
        if d in knowledge[c]:
            return True
    return False


if __name__ == '__main__':
    file_list = ["data/corpus/TrainSet.txt", "data/corpus/DevelopSet.txt"]
    write_list = ["data/corpus/TrainSentence.txt", "data/corpus/DevelopSentence.txt"]

    # keyword_get()
    # knowledge_get()
    #
    # for file, fw in zip(file_list, write_list):
    #     read_CID(file)
    #     read_sentence(file, fw)
