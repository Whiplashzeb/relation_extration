import numpy as np

def statistic(file):
    feature = []
    cid = []
    CID = {'1':0,'0':0}
    with open(file) as fp:
        line = fp.readline()
        while len(line) > 0:
            if line.startswith('passage') or line == '\n':
                pass
            else:
                line = line.split()
                # CID[line[-1]] += 1
                cid.append(int(line[-1]))
                feature.append(int(line[8]))
                # print(float(line[3]))
            line = fp.readline()
    print(np.corrcoef(feature,cid))




if __name__ == '__main__':
    file_list = ["data/result/train_out_result.txt","data/result/develop_out_result.txt"]

    for file in file_list:
        statistic(file)