from os import path, mkdir, getcwd, listdir
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
        file_name = path.split(self.file_path)[-1]
        name, ext = path.splitext(file_name)
        self.file_name = name
        a = getcwd()  # 获取当前路径
        b = path.join(a, '导出路径')
        c = path.join(b, self.file_name)
        self.out_put_dir = c
        if not path.exists(b):  # 如果路径不存在
            mkdir(b)
        if not path.exists(c):  # 如果路径不存在
            mkdir(c)
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

    def __init__(self, file_name, png_num, out_put_dir):
        """
        :param file_name: 文件名
        :param png_num: 拼接的图片数量
        :param out_put_dir: 第一次导出图片的文件路径
        """
        super(GenLongPng, self).__init__()
        self.file_name = file_name
        self.png_num = png_num
        self.out_put_dir = out_put_dir
        self.long_png_path = None

    def run(self):
        """
        用于图片拼接
        :return:
        """
        a = getcwd()  # 获取当前路径
        b1 = path.join(a, '导出路径')
        b = path.join(b1, self.file_name + '_长图')
        if not path.exists(b):
            mkdir(b)
        self.long_png_path = path.join(b, 'page_{}.png')
        png_list = listdir(self.out_put_dir)  # 获取所有png
        png_list.sort(key=lambda m: int(m[5: len(m) - 4]))
        ims = [Image.open(path.join(self.out_put_dir, fn)) for fn in png_list if fn.endswith('.png')]  # 获取所有图片信息
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


class ZipPng(QThread):
    trigger = pyqtSignal(int, int)  # 设定信号发送器

    def __init__(self, file_name, n, png_type):
        """
        初始化构造函数
        :param file_name: 文件名
        :param n: 保存图片质量
        :param png_type: 图片样式，普通样式还是720p/1080p
        """
        super().__init__()
        self.file_name = file_name
        self.n = n
        self.png_type = png_type

    def run(self):
        """
        用于压缩文件
        :param n: 图片压缩比例
        :return:
        """
        a = path.join(getcwd(), '导出路径')
        b = path.join(a, self.file_name + '_长图')  # 长图所在路径
        if self.png_type == '720p':
            c = path.join(a, self.file_name + '_720P长图(压缩后)')
        elif self.png_type == '1080p':
            c = path.join(a, self.file_name + '_1080P长图(压缩后)')
        else:  # 如果是普通图片
            c = path.join(a, self.file_name + '_普通长图(压缩后)')
        long_png_path = path.join(b, 'page_{}.png')
        if not path.exists(c):  # 如果c不存在
            mkdir(c)
        long_zip_png = path.join(c, 'page_{}.jpg')
        long_png_list = listdir(b)  # 计算未压缩的长图路径里面的图片数量
        long_png_list.sort(key=lambda m: int(m[5: len(m) - 4]))  # 文件排序
        long_png_0 = path.join(b, long_png_list[0])  # 第一张长图完整路径
        long_png_file_size = path.getsize(long_png_0)  # 第一张图片文件大小
        e = round(sqrt(long_png_file_size / (1024 ** 2)), 4)  # 计算要压缩的倍数,平方根，取3位小数，这里取这里根据图片数量自动计算压缩倍数
        print(e)
        ims = [Image.open(path.join(b, fn)) for fn in long_png_list if fn.endswith('.png')]  # 获取所有图片信息
        i = 0
        for im in ims:
            w, h = im.size  # 获取文件的宽、高
            if self.png_type == '720p':
                w1 = 720
                h1 = 720 * h / w
            elif self.png_type == '1080p':
                w1 = 1080
                h1 = 1080 * h / w
            else:  # 如果是普通模式
                w1 = w / e
                h1 = h / e
            im.thumbnail((int(w1), int(h1)))  # 缩放并取整
            im.save(long_zip_png.format(i), quality=int(self.n))  # 保存缩放后的图片,保存质量92%
            i += 1
            self.trigger.emit(i, len(long_png_list))  # 发送信号


if __name__ == '__main__':
    pdf_init = PdfInit('E:/浏览器下载/2020年第一季度报告(复稿1.03）.pdf')
    # my_dia = Pdf2Png(pdf_init)
    # my_dia.run()
    # long = GenLongPng('2020年第一季度报告(复稿1.03）', 6,
    #            r'E:\PycharmProjects\Pyqt5_Tools\Pdf_tools\导出路径\2020年第一季度报告(复稿1.03）')
    # long.run()
    zip_png = ZipPng('2020年第一季度报告(复稿1.03）', 0.92, '720p')
    zip_png.run()
