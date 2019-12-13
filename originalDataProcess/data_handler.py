import copy
from lxml.etree import Element, SubElement, tostring, ElementTree
import cv2
import os

def make_voc_dir():
    os.makedirs(r'C:\Users\asus\Desktop\VOC2007\Annotations')
    os.makedirs(r'C:\Users\asus\Desktop\VOC2007\ImageSets')
    os.makedirs(r'C:\Users\asus\Desktop\VOC2007\ImageSets\Main')
    os.makedirs(r'C:\Users\asus\Desktop\VOC2007\ImageSets\Layout')
    os.makedirs(r'C:\Users\asus\Desktop\VOC2007\ImageSets\Segmentation')
    os.makedirs(r'C:\Users\asus\Desktop\VOC2007\JPEGImages')
    os.makedirs(r'C:\Users\asus\Desktop\VOC2007\SegmentationClass')
    os.makedirs(r'C:\Users\asus\Desktop\VOC2007\SegmentationObject')

def conver_voc():
    template_file = r'C:\Users\asus\Pictures\testxml\test.xml'
    target_dir = r'C:\Users\asus\Desktop\VOC2007\Annotations\\'
    image_dir = r'C:\Users\asus\Desktop\core_500\Image\\'    # 图片文件夹
    label_dir = r'C:\Users\asus\Desktop\core_500\Annotation\\'    # 存储了图片信息的txt文件
    for parent, dirnames, label_files in os.walk(label_dir):
        print(label_files)
        for label_file in label_files:
            print(label_file)
            with open(r'C:\Users\asus\Desktop\core_500\Annotation\\' + label_file, 'r+', encoding='utf-8') as f:
                label_line = f.readlines()  # 标注数据
            file_names = []
            for line in label_line:
                labelx = line.split(' ')
                file_name = label_file.split('.')[0] + '.jpg'
                print(file_name)

                if file_name not in file_names:
                    file_names.append(file_name)
                    lable = labelx[1]
                    xmin = labelx[2]
                    ymin = labelx[3]
                    xmax = labelx[4]
                    ymax = labelx[5].split('\n')[0]

                    tree = ElementTree()
                    tree.parse(template_file)
                    root = tree.getroot()
                    # filename
                    root.find('filename').text = file_name
                    # size
                    sz = root.find('size')
                    im = cv2.imread(image_dir + file_name)
                    sz.find('height').text = str(im.shape[0])
                    sz.find('width').text = str(im.shape[1])
                    sz.find('depth').text = str(im.shape[2])
                    obj = root.find('object')
                    obj.find('name').text = lable
                    bb = obj.find('bndbox')
                    bb.find('xmin').text = xmin
                    bb.find('ymin').text = ymin
                    bb.find('xmax').text = xmax
                    bb.find('ymax').text = ymax
                # 添加object框
                else:
                    lable = labelx[1]
                    xmin = labelx[2]
                    ymin = labelx[3]
                    xmax = labelx[4]
                    ymax = labelx[5].split('\n')[0]

                    obj_ori = root.find('object')
                    obj = copy.deepcopy(obj_ori)  # 注意这里深拷贝

                    obj.find('name').text = lable
                    bb = obj.find('bndbox')
                    bb.find('xmin').text = xmin
                    bb.find('ymin').text = ymin
                    bb.find('xmax').text = xmax
                    bb.find('ymax').text = ymax
                    root.append(obj)

                xml_file = file_name.replace('jpg', 'xml')

                tree.write(target_dir + xml_file, encoding='utf-8')
def conver_voc_1():
    template_file = r'C:\Users\asus\Pictures\testxml\test.xml'
    target_dir = r'C:\Users\asus\Desktop\VOC2007_1\Annotations\\'
    image_dir = r'C:\Users\asus\Desktop\sample\coreless_5000\Image\\'    # 图片文件夹
    label_dir = r'C:\Users\asus\Desktop\sample\coreless_5000\Annotation\\'    # 存储了图片信息的txt文件
    for parent, dirnames, label_files in os.walk(label_dir):
        print(label_files)
        for label_file in label_files:
            print(label_file)
            with open(r'C:\Users\asus\Desktop\sample\coreless_5000\Annotation\\' + label_file, 'r+', encoding='utf-8') as f:
                label_line = f.readlines()  # 标注数据
            file_names = []
            for line in label_line:
                labelx = line.split(' ')
                file_name = label_file.split('.')[0] + '.jpg'
                print(file_name)

                if file_name not in file_names:
                    file_names.append(file_name)
                    lable = labelx[1]
                    xmin = labelx[2]
                    ymin = labelx[3]
                    xmax = labelx[4]
                    ymax = labelx[5].split('\n')[0]

                    tree = ElementTree()
                    tree.parse(template_file)
                    root = tree.getroot()
                    # filename
                    root.find('filename').text = file_name
                    # size
                    sz = root.find('size')
                    im = cv2.imread(image_dir + file_name)
                    sz.find('height').text = str(im.shape[0])
                    sz.find('width').text = str(im.shape[1])
                    sz.find('depth').text = str(im.shape[2])
                    obj = root.find('object')
                    obj.find('name').text = lable
                    bb = obj.find('bndbox')
                    bb.find('xmin').text = xmin
                    bb.find('ymin').text = ymin
                    bb.find('xmax').text = xmax
                    bb.find('ymax').text = ymax
                # 添加object框
                else:
                    lable = labelx[1]
                    xmin = labelx[2]
                    ymin = labelx[3]
                    xmax = labelx[4]
                    ymax = labelx[5].split('\n')[0]

                    obj_ori = root.find('object')
                    obj = copy.deepcopy(obj_ori)  # 注意这里深拷贝

                    obj.find('name').text = lable
                    bb = obj.find('bndbox')
                    bb.find('xmin').text = xmin
                    bb.find('ymin').text = ymin
                    bb.find('xmax').text = xmax
                    bb.find('ymax').text = ymax
                    root.append(obj)

                xml_file = file_name.replace('jpg', 'xml')

                tree.write(target_dir + xml_file, encoding='utf-8')
if __name__ == '__main__':
    make_voc_dir()
    conver_voc()
    # conver_voc_1()