# 获取实体对的依存距离及句法标注

# 获取实体的句法标注
def deal_signal(line):
    line = line.split()
    l = len(line)
    signal = line[l - 1][1:-1].split(':')[0]
    return signal


# 获取实体对的依存距离及句法标注
def dependency_distance_get(d_file, e_file, r_file):
    depend = open(d_file)
    entity = open(e_file)
    result = open(r_file, 'w')

    depend_line = depend.readline()
    entity_line = entity.readline()

    while len(depend_line) > 0 and len(entity_line) > 0:
        while "passage" in entity_line or entity_line == '\n':
            result.write(entity_line)
            entity_line = entity.readline()
        while "passage" in depend_line:
            depend_line = depend.readline()

        start, end = entity_line.split()[-9], entity_line.split()[-8]

        line = 0
        start_line = 0
        end_line = 0
        start_signal = ''
        end_signal = ''
        CID = entity_line.split()[-1]
        while not "passage" in depend_line and len(depend_line) > 0:
            if line >= 1 and depend_line.startswith('->'):
                break
            if start in depend_line:
                start_line = line
                start_signal = deal_signal(depend_line)
                depend_line = depend.readline()
            elif end in depend_line:
                end_line = line
                end_signal = deal_signal(depend_line)
                depend_line = depend.readline()
            else:
                depend_line = depend.readline()

            line += 1

        result.write("%d\t%d\t%s\t%s\t%s\n" % (abs(start_line - end_line), line, start_signal, end_signal, CID))
        entity_line = entity.readline()


if __name__ == '__main__':
    dependency_list = ["data/corpus/train_dependency.txt", "data/corpus/develop_dependency.txt"]
    entity_list = ["data/corpus/TrainSentence.txt", "data/corpus/DevelopSentence.txt"]
    result_list = ["data/corpus/TrainDependResult1.txt", "data/corpus/DevelopDependResult1.txt"]


    # for i in range(2):
    #     dependency_distance_get(dependency_list[i],entity_list[i],result_list[i])
    # dependency_distance_get("data/temp.txt","data/train.txt","data/result.txt")
