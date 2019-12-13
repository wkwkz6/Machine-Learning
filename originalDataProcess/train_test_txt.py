import os
import random

trainval_percent = 0.8  # 作为trainval_percent的比例，在整个数据集，可以修改
train_percent = 0.8  # 用于训练的数据的比例，可以修改
xmlfilepath = r'C:\Users\asus\Desktop\VOC200\Annotations'
txtsavepath = r'C:\Users\asus\Desktop\VOC200\ImageSets\Main'
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open(txtsavepath + r'\trainval.txt', 'w')
ftest = open(txtsavepath + r'\test.txt', 'w')
ftrain = open(txtsavepath + r'\train.txt', 'w')
fval = open(txtsavepath + r'\val.txt', 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()
