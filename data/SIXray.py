"""VOC Dataset Classes

Original author: Francisco Massa
https://github.com/fmassa/vision/blob/voc_dataset/torchvision/datasets/voc.py

Updated by: Ellis Brown, Max deGroot
"""
import os
from .config import HOME
import os.path as osp
import sys
import torch
import torch.utils.data as data
import cv2
import numpy as np

if sys.version_info[0] == 2:
    import xml.etree.cElementTree as ET
else:
    import xml.etree.ElementTree as ET

'''
SIXray_CLASSES = (  # always index 0
    'gun', 'knife', 'wrench', 'pliers',
    'scissors'
    )
'''

'''
SIXray_CLASSES = (
    '带电芯充电宝', '不带电芯充电宝', '劣质充电宝', '其它充电宝',
    '金属打火机' '非金属打火机', '点烟器', '异形打火机', '镁棒', '其它火种',
    '扳手', '螺丝刀', '钳子', '其他日常工具',
    '管制刀具', '直刀', '折叠刀', '异形刀', '剪刀', '其它刀具',
    '电击器', '手铐', '警鞭', '弩', '其它军警器具',
    '手枪', '长枪', '仿真枪', '枪支部件', '其它枪支',
    '子弹', '空包弹', '信号弹', '其它弹药',
    '液化石油气', 'ZIPPO油', '打火机气', '压缩气体瓶', '其它危险品',
    '烟花', '礼花', '鞭炮', '烟饼（包）', '其它烟火制品',
    '雷管', '拉火管', '导火索', '炸药', '爆炸装置', '其它爆炸装置'
)
'''

SIXray_CLASSES = (
    '带电芯充电宝', '不带电芯充电宝'
)
# note: if you used our download scripts, this should be right
# SIXray_ROOT = osp.join(HOME, r"ssdpytorch\VOC2007")
SIXray_ROOT=r"F:\pycharm_codes\ssdpytorch\VOC2007"


class SIXrayAnnotationTransform(object):
    """Transforms a VOC annotation into a Tensor of bbox coords and label index
    Initilized with a dictionary lookup of classnames to indexes

    Arguments:
        class_to_ind (dict, optional): dictionary lookup of classnames -> indexes
            (default: alphabetic indexing of VOC's 20 classes)
        keep_difficult (bool, optional): keep difficult instances or not
            (default: False)
        height (int): height
        width (int): width
    """

    def __init__(self, class_to_ind=None, keep_difficult=False):
        self.class_to_ind = class_to_ind or dict(
            # zip(SIXray_CLASSES, range(len(SIXray_CLASSES))))
            zip(SIXray_CLASSES, range(len(SIXray_CLASSES))))
        self.keep_difficult = keep_difficult
        # 添加的记录所有小类总数
        self.type_dict = {}
        # 记录大类数量
        self.type_sum_dict = {}

    def __call__(self, target, width, height, idx):
        """
        Arguments:
            target (annotation) : the target annotation to be made usable
                will be an ET.Element
            it has been changed to the path of annotation-2019-07-10
        Returns:
            a list containing lists of bounding boxes  [bbox coords, class name]
        """
        # print (idx)

        ###读取所有类
        # class_path = "C:/Users/石玉峰/PycharmProjects/untitled1/package2/class.xml"
        '''
        class_path = SIXray_ROOT + "class.xml"
        tree = ET.parse(class_path)
        class_root = tree.getroot()
        for child in class_root:
            one_dict = {}
            type_name = None
            find_name = 0
            for grandson in child:
                if find_name == 0:
                    find_name = 1
                    type_name = grandson.text
                else:
                    one_dict[grandson.text] = 0
            self.type_dict[type_name] = one_dict
        #print(self.type_dict)
        '''
        # 遍历Annotation
        # root_annotation = '/media/dsg3/datasets/Xray20190704/Annotation/'
        res = []
        with open(target, "r", encoding='utf-8') as f1:
            dataread = f1.readlines()
        for annotation in dataread:
            bndbox = []
            temp = annotation.split()
            name = temp[1]
            # 只读两类
            if name != '带电芯充电宝' and name != '不带电芯充电宝':
                continue
            xmin = int(temp[2]) / width
            # 只读取V视角的
            if xmin > 1:
                continue
            if xmin < 0:
                xmin = 0
            ymin = int(temp[3]) / height
            if ymin < 0:
                ymin = 0
            xmax = int(temp[4]) / width
            if xmax > 1:  # 是这么个意思吧？
                xmax = 1
            ymax = int(temp[5]) / height
            if ymax > 1:
                ymax = 1
            bndbox.append(xmin)
            bndbox.append(ymin)
            bndbox.append(xmax)
            bndbox.append(ymax)
            label_idx = self.class_to_ind[name]
            # label_idx = name
            bndbox.append(label_idx)
            res += [bndbox]  # [xmin, ymin, xmax, ymax, label_ind]
        if len(res) == 0:
            return [[0, 0, 0, 0, 3]]
        return res


class SIXrayDetection(data.Dataset):
    """VOC Detection Dataset Object

    input is image, target is annotation

    Arguments:
        root (string): filepath to VOCdevkit folder.
        image_set (string): imageset to use (eg. 'train', 'val', 'test')
        transform (callable, optional): transformation to perform on the
            input image
        target_transform (callable, optional): transformation to perform on the
            target `annotation`
            (eg: take in caption string, return tensor of word indices)
        dataset_name (string, optional): which dataset to load
            (default: 'VOC2007')
    """

    def __init__(self, root,
                 image_sets,
                 transform=None, target_transform=SIXrayAnnotationTransform(),
                 # dataset_name='SIXray'):
                 dataset_name='SIXray'):
        # self.root = root
        self.root = r'F:\pycharm_codes\ssdpytorch\all_samples'
        self.image_set = r'F:\pycharm_codes\ssdpytorch\VOC2007\VOC2007\ImageSets\Main\test.txt'
        self.transform = transform
        self.target_transform = target_transform
        # self.name = dataset_name
        self.name = 'Xray0723_bat_core_coreless'
        # self._annopath = osp.join('%s' % self.root, 'Annotation', '%s.xml')
        self._annopath = osp.join('%s' % self.root, 'Annotation', '%s.txt')
        # self._annopath = osp.join('%s' % self.root, 'Anno_core_coreless_battery_sub_2000_500', '%s.txt')
        # self._imgpath = osp.join('%s' % self.root, 'Image', '%s.jpg')
        self._imgpath = osp.join('%s' % self.root, 'cut_Image_core_coreless_battery_sub_2000_500', '%s.TIFF')
        ###这尼玛还有小写的tiff？
        self._imgpath1 = osp.join('%s' % self.root, 'cut_Image_core_coreless_battery_sub_2000_500', '%s.tiff')
        # self._imgpath_jpg = osp.join('%s' % self.root, 'cut_Image_core_coreless_battery_sub_2000_500', '%s.jpg')
        self._imgpath_jpg = osp.join('%s' % self.root, 'Image', '%s.jpg')
        self.ids = list()

        # listdir = os.listdir(osp.join('%s' % self.root, 'Annotation'))

        with open(self.image_set, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.ids.append(line.strip('\n'))

        '''
        for name in listdir:
            self.ids.append(osp.splitext(name)[0])
        '''

    def __getitem__(self, index):
        im, gt, h, w, og_im = self.pull_item(index)

        return im, gt

    def __len__(self):
        return len(self.ids)

    def pull_item(self, index):
        img_id = self.ids[index]

        # target = ET.parse(self._annopath % img_id).getroot()

        target = self._annopath % img_id  # 注释目录
        # print(target)
        # print(self._imgpath % img_id)
        img = cv2.imread(self._imgpath % img_id)
        if img is None:
            img = cv2.imread(self._imgpath1 % img_id)
        if img is None:
            img = cv2.imread(self._imgpath_jpg % img_id)

        if img is None:
            print('\nwrong\n')
            print(self._imgpath_jpg % img_id)

        # print()
        height, width, channels = img.shape
        # print("height: " + str(height) + " ; width : " + str(width) + " ; channels " + str(channels) )
        og_img = img

        # print (img_id)
        if self.target_transform is not None:
            target = self.target_transform(target, width, height, img_id)

        if self.transform is not None:
            target = np.array(target)
            # print(target)
            img, boxes, labels = self.transform(img, target[:, :4], target[:, 4])
            # to rgb
            img = img[:, :, (2, 1, 0)]
            # img = img.transpose(a2, 0, a1)
            target = np.hstack((boxes, np.expand_dims(labels, axis=1)))
        return torch.from_numpy(img).permute(2, 0, 1), target, height, width, og_img
        # return torch.from_numpy(img), target, height, width

    """
    class_path = "C:/Users/石玉峰/PycharmProjects/untitled1/package2/class.xml"
    tree = ET.parse(class_path)
    class_root = tree.getroot()
    type_dict = {}
    for child in class_root:
        one_dict = {}
        type_name = None
        find_name = 0
        for grandson in child:
            if find_name == 0:
                find_name = 1
                type_name = grandson.text
            else:
                one_dict[grandson.text] = 0
        type_dict[type_name] = one_dict
    print(type_dict)
    """

    """
    def pull_image(self, index):
        '''Returns the original image object at index in PIL form

        Note: not using self.__getitem__(), as any transformations passed in
        could mess up this functionality.

        Argument:
            index (int): index of img to show
        Return:
            PIL img
        '''
        img_id = self.ids[index]
        return cv2.imread(self._imgpath % img_id, cv2.IMREAD_COLOR)

    def pull_anno(self, index):
        '''Returns the original annotation of image at index

        Note: not using self.__getitem__(), as any transformations passed in
        could mess up this functionality.

        Argument:
            index (int): index of img to get annotation of
        Return:
            list:  [img_id, [(label, bbox coords),...]]
                eg: ('001718', [('dog', (96, 13, 438, 332))])
        '''
        img_id = self.ids[index]
        anno = ET.parse(self._annopath % img_id).getroot()
        gt = self.target_transform(anno, a1, a1)
        return img_id[a1], gt

    def pull_tensor(self, index):
        '''Returns the original image at an index in tensor form

        Note: not using self.__getitem__(), as any transformations passed in
        could mess up this functionality.

        Argument:
            index (int): index of img to show
        Return:
            tensorized version of img, squeezed
        '''
        return torch.Tensor(self.pull_image(index)).unsqueeze_(0)
    """
