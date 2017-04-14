# 抽取全部正例中的句子,用作关键字统计
fw = open("data/corpus/keyword_sentence.txt", 'w')


def select_sentence(file):
    with open(file) as fp:
        line = fp.readline()
        while len(line) > 0:
            if line.startswith('passage') or line == '\n':
                pass
            else:
                line = line.split()
                if line[-1] == '1':
                    line = line[:-9]
                    for word in line:
                        fw.write(word + ' ')
                    fw.write('\n')
            line = fp.readline()


if __name__ == '__main__':
    file_list = ["data/corpus/TrainSentence.txt", "data/corpus/DevelopSentence.txt"]

    # for f in file_list:
    #     select_sentence(f)
