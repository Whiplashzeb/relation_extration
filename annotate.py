# 用于句法标记统计

import collections

anno = {}


def annotate(file):
    with open(file) as fp:
        line = fp.readline()
        while len(line) > 0:
            if "passage" in line or line == '\n':
                line = fp.readline()
            else:
                line = line.split()
                if line[4] == '1':
                    for i in range(2, 4):
                        if line[i] in anno:
                            anno[line[i]] += 1
                        else:
                            anno[line[i]] = 1
            line = fp.readline()


if __name__ == '__main__':
    file_list = ["data/corpus/TrainDependResult.txt", "data/corpus/DevelopDependResult.txt"]

    for file in file_list:
        annotate(file)

    anno = collections.OrderedDict(sorted(anno.items(), key=lambda t: -t[1]))

    with open('data/annotate.txt','w') as fp:
        for a,n in anno.items():
            fp.write(a+'\t'+str(n)+'\n')
