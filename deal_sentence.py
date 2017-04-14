# 只保留文件中的句子,用作依存句法分析
def del_sentence(file, writefile):
    fw = open(writefile, 'w')

    with open(file) as fp:
        line = fp.readline()
        while len(line) > 0:
            if line.startswith('passage') or line == '\n':
                fw.write(line)
            else:
                line = line.split()
                line = line[:-9]
                for word in line:
                    fw.write(word + ' ')
                fw.write('\n')
            line = fp.readline()


if __name__ == '__main__':
    file_list = ["data/corpus/TrainSentence.txt", "data/corpus/DevelopSentence.txt"]
    writefile_list = ["data/corpus/TrainDependSentence.txt", "data/corpus/DevelopDependSentence.txt"]

    # for f,fw in zip(file_list,writefile_list):
    #     del_sentence(f,fw)
