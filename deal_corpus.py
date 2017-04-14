# 替换文章中的化学物质和疾病为MeSH@ID
def deal_set(filename):
    # 写入文件
    fw = open("data/temp.txt", 'w')

    if "Develop" in filename:
        fw = open("data/corpus/develop.txt", 'w')
    elif "Train" in filename:
        fw = open("data/corpus/train.txt", 'w')

    with open(filename) as fp:
        title = fp.readline()
        while len(title) > 0:
            # 获取文章编号及标题
            title = title.partition("|t|")
            fw.write('passage:' + title[0] + '\n')
            # 获取文章摘要
            abstract = fp.readline().partition('|a|')[2]

            # 待匹配文章
            passage_raw = title[2] + abstract
            # 存储匹配后文章
            passage = 'title:' + title[2] + 'abstract:' + abstract

            CID = {}
            # 实体分为化学物质,疾病,CID关系
            entity = fp.readline()
            while len(entity) > 1:
                entity = entity.split()
                l = len(entity)
                if l >= 6:
                    start, end = int(entity[1]), int(entity[2])
                    if entity[l - 2] == 'Chemical':
                        passage = passage.replace(passage_raw[start:end], 'C_' + entity[l - 1])
                    elif entity[l - 2] == 'Disease':
                        passage = passage.replace(passage_raw[start:end], 'D_' + entity[l - 1])
                if l == 4:
                    if 'C_' + entity[2] in CID:
                        CID['C_' + entity[2]].add('D_' + entity[3])
                    else:
                        CID['C_' + entity[2]] = set(['D_' + entity[3]])
                entity = fp.readline()
            # 存储
            fw.write(passage)
            for c, d in CID.items():
                for item in d:
                    fw.write("CID:\t%s\t%s\n" % (c, item))
            title = fp.readline()
    fw.close()


# 统计训练集和开发集中的化学物质和疾病
chemical = set()
disease = set()
CID = {}


def chemical_disease_get(filename):
    # chemical.clear()
    # disease.clear()
    # CID.clear()
    with open(filename) as fp:
        title = fp.readline()
        while len(title) > 0:
            abstract = fp.readline()

            entity = fp.readline()
            while len(entity) > 1:
                entity = entity.split()
                l = len(entity)
                if l >= 6:
                    if entity[l - 2] == 'Chemical':
                        chemical.add(entity[l - 1])
                    if entity[l - 2] == 'Disease':
                        disease.add(entity[l - 1])
                if l == 4:
                    CID['C_' + entity[2]] = 'D_' + entity[3]
                entity = fp.readline()
            title = fp.readline()


if __name__ == '__main__':
    file_list = ["data/raw_data/CDR_TrainingSet.txt",
                 "data/raw_data/CDR_DevelopmentSet.txt"
                 ]
    # for file in file_list:
    #     deal_set(file)

    # for file in file_list:
    #     chemical_disease_get(file)
    #     print(len(chemical), len(disease),len(CID))
