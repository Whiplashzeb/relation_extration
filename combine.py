anno = {}


def get_annotate():
    with open("data/annotate.txt") as fp:
        line = fp.readline()
        while len(line) > 0:
            line = line.split()
            anno[line[0]] = int(line[1])
            line = fp.readline()


def cal_annotate(s_signal, e_signal):
    count = 0
    if s_signal in anno:
        count += anno[s_signal]
    if e_signal in anno:
        count += anno[e_signal]

    return count


def combine_result(s_file, d_file, result_file):
    sent = open(s_file)
    depend = open(d_file)
    result = open(result_file, 'w')

    s_line = sent.readline()
    d_line = depend.readline()

    while len(s_line) > 0 and len(d_line) > 0:
        while s_line.startswith('passage') or s_line == '\n':
            result.write(s_line)
            s_line = sent.readline()
            d_line = depend.readline()

        s_line = s_line.split()
        d_line = d_line.split()

        ret = cal_annotate(d_line[2], d_line[3])

        result.write("%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s%-8s\n" % (
        d_line[0], d_line[1], str(ret), s_line[-9], s_line[-8], s_line[-7], s_line[-6], s_line[-5], s_line[-4],
        s_line[-3], s_line[-2], s_line[-1]))

        s_line = sent.readline()
        d_line = depend.readline()


if __name__ == '__main__':
    sentence_file = ["data/corpus/TrainSentence.txt", "data/corpus/DevelopSentence.txt"]
    depend_file = ["data/corpus/TrainDependResult.txt", "data/corpus/DevelopDependResult.txt"]
    result_file = ["data/result/train_in_result.txt", "data/result/develop_in_result.txt"]

    get_annotate()

    for i in range(2):
        combine_result(sentence_file[i], depend_file[i], result_file[i])
