# 统计关键词

from collections import OrderedDict

key = {}


def cal_keyword(file):
    with open(file) as fp:
        line = fp.readline()
        while len(line) > 0:
            line = line.split()
            for word in line:
                if word in key:
                    key[word] += 1
                else:
                    key[word] = 1
            line = fp.readline()


if __name__ == '__main__':
    file = 'data/corpus/keyword.txt'

    cal_keyword(file)

    key = OrderedDict(sorted(key.items(), key=lambda t: -t[1]))

    # with open('data/keyword.txt', 'w') as fp:
    #     for k, n in key.items():
    #         if k.isalpha() and n >= 100:
    #             fp.write("%s\t%d\n" % (k, n))

    count = 0
    with open('data/keyword.txt') as fp:
        line = fp.readline()
        while len(line) > 0:
            line = line.split()
            count += int(line[1])
            line = fp.readline()

    print(count)
