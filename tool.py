from os import path, mkdir, getcwd, listdir, remove
from PIL import Image
import fitz
from PyQt5.QtCore import pyqtSignal, QThread
from math import ceil, sqrt


class PdfInit(object):
    """
    pdf初始化
    """

    def __init__(self, file_path):
        self.file_path = file_path  # 图片路径
        self.out_put_dir = None  # 输出路径
        self.file_name = None  # 文件名
        self.page_num = None
        self.doc = None
        self.get_page_num()  # 初始化

    def get_page_num(self):
        """
        此方法用于获取pdf页面数量,并且计算导出路径
        :param
        """
        dir_path = path.split(self.file_path)[0]  # 获取路径所在文件夹
        b = path.join(dir_path, '导出图片')
        self.out_put_dir = b
        if not path.exists(b):  # 如果路径不存在
            mkdir(b)
        #  打开PDF文件，生成一个对象
        self.doc = fitz.open(self.file_path)
        self.page_num = self.doc.pageCount


class Pdf2Png(QThread):
    """
    这个类用于将pdf转成png图片
    """
    trigger = pyqtSignal(int, int)  # 创建信号池,共发射两个信号

    def __init__(self, pdf_init):
        super(Pdf2Png, self).__init__()
        self.file_path = pdf_init.file_path
        self.doc = pdf_init.doc
        self.page_num = pdf_init.page_num
        self.output_dir = pdf_init.out_put_dir
        # 设置窗口

    def run(self):
        for pg in range(self.page_num):
            # print('正在导出第{}张图片'.format(pg))
            page = self.doc[pg]
            rotate = int(0)
            # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高四倍的图像。
            zoom_x = 2.0
            zoom_y = 2.0
            trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pm = page.getPixmap(matrix=trans, alpha=False)
            pm.writePNG('%s/page_%s.png' % (self.output_dir, pg))  # 保存图片
            self.trigger.emit(pg, self.page_num)  # 发射信号
        print('图片导出成功')


class GenLongPng(QThread):
    """
    这个类用于将单张png转成长图
    :param
    """
    trigger = pyqtSignal(int, int)  # 构建触发器，用于后面发送消息.第一个信号为当前进度，第二个信号为总进度

    def __init__(self, png_num, png_dir, out_dir):
        """
        :param png_num: 拼接的图片数量
        :param png_dir: 图片所在路径
        :param out_dir: 导出图片路径
        """
        super(GenLongPng, self).__init__()
        self.png_num = png_num
        self.png_dir = png_dir  # 图片地址
        self.out_dir = out_dir  # 导出的长图地址
        self.long_png_path = None  # 长图路径

    def run(self):
        """
        用于图片拼接
        :return:
        """
        if not path.exists(self.out_dir):
            mkdir(self.out_dir)
        else:
            list1 = listdir(self.out_dir)
            data = [remove(self.out_dir + '/' + li) for li in list1]  # 清空原有文件
        self.long_png_path = self.out_dir + '/' + 'page_{}.png'  # 长图地址
        png_list = listdir(self.png_dir)  # 获取所有图片
        try:  # 尝试排序
            png_list.sort(key=lambda m: int(m[5: len(m) - 4]))
        except Exception as err:
            print('排序失败')
            print(err)
        ims = [Image.open(path.join(self.png_dir, fn)) for fn in png_list if fn.endswith('.png')]  # 获取所有图片信息
        number = ceil(len(ims) / self.png_num)  # 向上取整，判断可以分成的长图的个数
        remain = len(ims) % self.png_num  # 余数，判断最后一张长图剩余数
        for x in range(number):  # 开始循环生成长图
            if remain > 0:  # 如果余数大于0
                if x < number - 1:  # 如果不是最后一张图
                    self.paste_png(ims, self.png_num, x)  # 按最大拼接拼接图片
                else:  # 如果是最后一张图
                    self.paste_png(ims, remain, x)  # 按余数拼接图片
            elif remain == 0:  # 如果余数为零
                self.paste_png(ims, self.png_num, x)  # 按最大拼接图片，不用考虑最后一张图
            self.trigger.emit(x, number)  # 发射信号

    def paste_png(self, ims, n1, x):
        """
        此方法用于粘贴单个长图
        :param ims: 所有图片的信息
        :param n1: 本次预计拼接的图片数量
        :param x: x为当前图片的页码数减1
        """
        width, height = ims[0].size  # 获取单张图片大小
        whiter_picture1 = Image.new(ims[0].mode, (width, height * n1))  # 创建空白图，长度为n1的长度
        for y, im in enumerate(ims[x * self.png_num: self.png_num * x + n1]):
            whiter_picture1.paste(im, box=(0, y * height))  # 图片粘贴拼凑
        whiter_picture1.save(self.long_png_path.format(x))  # 长图保存


class GenLongPng2(QThread):
    """
    这个类用于将单张png转成长图,包含矩阵算法
    :param
    """
    trigger = pyqtSignal(int, int)  # 构建触发器，用于后面发送消息.第一个信号为当前进度，第二个信号为总进度

    def __init__(self, png_row, png_column, png_interval, png_dir, out_dir):
        """
        :param png_row: 拼接的图片的行数
        :param png_column: 拼接图片的列数
        :param png_interval：凭借图片的间隙
        :param png_dir: 图片的路径
        :param out_dir: 导出图片路径
        """
        super(GenLongPng2, self).__init__()
        self.png_row = png_row
        self.png_column = png_column
        self.png_interval = png_interval
        self.png_dir = png_dir  # 图片地址
        self.out_dir = out_dir  # 导出的长图地址
        self.long_png_path = None  # 长图路径

    def run(self):
        """
        用于图片拼接
        :return:
        """
        if not path.exists(self.out_dir):
            mkdir(self.out_dir)
        else:
            list1 = listdir(self.out_dir)
            data = [remove(self.out_dir + '/' + li) for li in list1]  # 清空原有文件
        self.long_png_path = self.out_dir + '/' + 'page_{}.png'  # 长图地址
        png_list = listdir(self.png_dir)  # 获取所有图片
        try:  # 尝试排序
            png_list.sort(key=lambda m: int(m[5: len(m) - 4]))
        except Exception as err:
            print('排序失败')
            print(err)
        ims = [Image.open(path.join(self.png_dir, fn)) for fn in png_list if fn.endswith('.png')]  # 获取所有图片信息
        if len(ims) > (self.png_row * self.png_column):
            number = ceil(len(ims) / (self.png_row * self.png_column))  # 向上取整，判断可以分成的长图的个数
            if number > 1:
                remain = len(ims) % (self.png_row * self.png_column)  # 余数，判断最后一张长图剩余数
            else:
                remain = 0
        else:
            number = 1
            remain = len(ims)
        for x in range(number):  # 开始循环生成长图
            if remain > 0:  # 如果余数大于0
                if x < number - 1:  # 如果不是最后一张图
                    self.paste_png(ims, self.png_row * self.png_column, x)  # 按最大拼接拼接图片
                else:  # 如果是最后一张图
                    self.paste_png(ims, remain, x)  # 按余数拼接图片
            elif remain == 0:  # 如果余数为零
                self.paste_png(ims, self.png_row * self.png_column, x)  # 按最大拼接图片，不用考虑最后一张图
            self.trigger.emit(x, number)  # 发射信号

    def paste_png(self, ims, n1, x):
        """
        此方法用于粘贴单个长图
        :param ims: 所有图片的信息
        :param n1: 本次预计拼接的图片数量
        :param x: x为当前图片的页码数减1
        """
        width, height = ims[0].size  # 获取单张图片大小
        # 创建空白白图备用
        whiter_picture2 = Image.new("RGB", (width, height), "#FFFFFF")
        # 判断本次是否会产生空白图
        # -- 如果没有空白 -- #
        if n1 == self.png_column * self.png_row:
            new_width = width * self.png_column + (self.png_column - 1) * self.png_interval
            new_height = height * self.png_row + (self.png_row - 1) * self.png_interval
        else:
            # 如果只有一行图
            if n1 <= self.png_column:
                new_width = width * n1 + (n1 - 1) * self.png_interval
                new_height = height
            else:
                rows = ceil(n1 / self.png_column)  # 计算总行数
                new_width = width * self.png_column + (self.png_column - 1) * self.png_interval
                new_height = height * rows + (rows - 1) * self.png_interval
                if self.png_column != 1:  # 如果存在多余空白框
                    #  -- 用于填充---
                    need_n = self.png_column * self.png_row - n1
                    n1 = self.png_column * self.png_row
                    # 批量插入白图
                    for i in range(need_n):
                        ims.append(whiter_picture2)
        print(len(ims))
        # 创建透明大图
        big_picture = Image.new(ims[0].mode, (new_width, new_height))
        for y, im in enumerate(ims[x * self.png_row * self.png_column: self.png_row * self.png_column * x + n1]):
            p = y + 1
            row = int(y / self.png_column) + 1
            p = p - self.png_column * (row - 1)
            big_picture.paste(im, box=((p-1) * (width + self.png_interval), (row-1) * (height + self.png_interval)))
        big_picture.save(self.long_png_path.format(x))  # 长图保存


class ZipPng(QThread):
    trigger = pyqtSignal(int, int)  # 设定信号发送器

    def __init__(self, width_model, picture_type, zip_num, png_dir):
        """
        初始化构造函数
        :param width_model: 图片宽度模式,普通样式还是720p/1080p
        :param zip_num: 保存图片压缩率
        :param picture_type: 图片格式，png/jpg
        :param png_dir：待压缩图片来源
        """
        super().__init__()
        self.width_model = width_model
        self.picture_type = picture_type
        self.zip_num = zip_num
        self.png_dir = png_dir

    def run(self):
        """
        用于压缩文件
        :return:
        """
        parent_dir = path.split(self.png_dir)[0]  # 找到图片的父路径
        if self.picture_type == '720p':
            c = parent_dir + '/' + '720P图(压缩后)'
        elif self.picture_type == '1080p':
            c = parent_dir + '/' + '1080P图(压缩后)'
        else:  # 如果是普通图片
            c = parent_dir + '/' + '普通图(压缩后)'
        if not path.exists(c):
            mkdir(c)
        else:
            list1 = listdir(c)
            for li in list1:
                remove(c + '/' + li)
        png_list = listdir(self.png_dir)
        zip_picture = c + '/' + 'page_{}.' + self.picture_type  # 压缩图输出路径
        png_list = listdir(self.png_dir)  # 计算未压缩的长图路径里面的图片数量
        try:
            png_list.sort(key=lambda m: int(m[5: len(m) - 4]))  # 文件排序
        except Exception as err:
            print('排序失败')
            print(err)
        png_0 = self.png_dir + '/' + png_list[0]
        png_file_size = path.getsize(png_0)  # 第一张图片文件大小
        e = round(sqrt(png_file_size / (1024 ** 2)), 4)  # 计算要压缩的倍数,平方根，取3位小数，这里取这里根据图片数量自动计算压缩倍数
        print(e)
        # 获取所有图片信息
        ims = [Image.open(self.png_dir + '/' + fn) for fn in png_list if fn.endswith('.png') or fn.endswith('jpg')]
        i = 0
        for im in ims:
            w, h = im.size  # 获取文件的宽、高
            if self.picture_type == '720p':
                w1 = 720
                h1 = 720 * h / w
            elif self.picture_type == '1080p':
                w1 = 1080
                h1 = 1080 * h / w
            else:  # 如果是普通模式
                w1 = w / e
                h1 = h / e
            im.thumbnail((int(w1), int(h1)))  # 缩放并取整
            im.save(zip_picture.format(i), quality=int(self.zip_num))  # 保存缩放后的图片,保存质量92%
            i += 1
            self.trigger.emit(i, len(png_list))  # 发送信号


if __name__ == '__main__':
    pass
