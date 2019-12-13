from PIL import Image
import os
import os.path

count = 0
rootdir = r'C:\Users\asus\Desktop\sample\core_500\Image'   #读取文件夹位置
for parent, dirnames, filenames in os.walk(rootdir):      #水平翻转
    curnum = 1000
    basename = 'core_battery0000'
    for filename in filenames:
        curnum += 1
        filename_txt = filename.split('.')[0] + '.txt'
        # print(filename_txt)
        currentPath = os.path.join(parent, filename)
        txtPath = r'C:\Users\asus\Desktop\sample\core_500\Annotation' + '\\' + filename_txt
        im = Image.open(currentPath)
        x = im.size[0]
        y = im.size[1]
        out = im.transpose(Image.FLIP_LEFT_RIGHT)      #水平翻转
        with open(txtPath, 'r+', encoding='utf-8') as f:
            f1 = open(r'C:\Users\asus\Desktop\sample\core_500\Annotation' + '\\' + basename + str(curnum) + '.txt', 'w',encoding='utf-8')
            lines = f.readlines()
            line_num = lines.__len__()
            for line in lines:
                # line_num -= 1
                # print(line_num)
                # # linedata = f.readline()
                # if line_num < 0:
                #     print(line_num)
                #     break
                # print(line)

                data = line.split(' ')
                # print(data)
                # print(data[1])
                if data[1] == '带电芯充电宝' or data[1] == '不带电芯充电宝':
                    print(data)
                    for i in range(data.__len__()):
                        if i == 2:
                            f1.write(str(x - int(data[4])) + ' ')
                            continue
                        if i == 4:
                            f1.write(str(x - int(data[2])) + ' ')
                            continue
                        if i == 5:
                            f1.write(data[i])
                            continue
                        f1.write(data[i] + ' ')
                else:
                    # # print('1')
                    # # w = open(txtPath, 'w', encoding='utf-8')
                    # new_line = f.readline()
                    # f.write(new_line)
                    # # w.close()
                    print(data)
                    data[1] = '其他类别'
                    count += 1
                    for i in range(data.__len__()):
                        if i == 2:
                            f1.write(str(x - int(data[4])) + ' ')
                            continue
                        if i == 4:
                            f1.write(str(x - int(data[2])) + ' ')
                            continue
                        if i == 5:
                            f1.write(data[i])
                            continue
                        f1.write(data[i] + ' ')
        f1.close()
        f.close()
        newname = r"C:\Users\asus\Desktop\sample\core_500\Image" + '\\' + basename + str(curnum) + ".jpg"
        out.save(newname)


rootdir = r'C:\Users\asus\Desktop\sample\core_500\Image'   #读取文件夹位置
for parent, dirnames, filenames in os.walk(rootdir):      #垂直翻转
    curnum = 1500
    basename = 'core_battery0000'
    for filename in filenames:
        curnum += 1
        filename_txt = filename.split('.')[0] + '.txt'
        # print(filename_txt)
        currentPath = os.path.join(parent, filename)
        txtPath = r'C:\Users\asus\Desktop\sample\core_500\Annotation' + '\\' + filename_txt
        im = Image.open(currentPath)
        x = im.size[0]
        y = im.size[1]
        out = im.transpose(Image.FLIP_TOP_BOTTOM)    #垂直翻转
        with open(txtPath, 'r+', encoding='utf-8') as f:
            f1 = open(r'C:\Users\asus\Desktop\sample\core_500\Annotation' + '\\' + basename + str(curnum) + '.txt', 'w',encoding='utf-8')
            for line in f.readlines():
                data = line.split(' ')
                if data[1] == '带电芯充电宝' or data[1] == '不带电芯充电宝':
                    print(data)
                    for i in range(data.__len__()):
                        if i == 3:
                            f1.write(str(y - int(data[5])) + ' ')
                            continue
                        if i == 5:
                            f1.write(str(y - int(data[3])))
                            continue
                        f1.write(data[i] + ' ')
                    f1.write('\n')
                else:
                    print(data)
                    data[1] = '其他类别'
                    count += 1
                    for i in range(data.__len__()):
                        if i == 3:
                            f1.write(str(y - int(data[5])) + ' ')
                            continue
                        if i == 5:
                            f1.write(str(y - int(data[3])))
                            continue
                        f1.write(data[i] + ' ')
                    f1.write('\n')
        f1.close()
        f.close()
        newname = r"C:\Users\asus\Desktop\sample\core_500\Image" + '\\' + basename + str(curnum) + ".jpg"
        out.save(newname)
