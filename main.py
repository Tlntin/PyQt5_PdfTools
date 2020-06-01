from ui import UI
from tool import *
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, qApp, QLabel, QDialog, QPushButton, QProgressDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from os import path


class PdfMain(UI):

    def __init__(self):
        super(PdfMain, self).__init__()
        self.init_action()
        self.my_dialog1 = None  # 我的第一个会话， 用于pdf转png
        self.my_dialog2 = None  # 我的第二个会话, 用于png拼接长图
        self.my_dialog3 = None  # 我的第三个会话，用于压缩长图
        self.progress = None  # 进度条
        self.file_name = None  # 文件名
        self.line_value = '92'

    def init_action(self):
        """
        此函数用于初始化动作
        """
        self.action1.triggered.connect(self.notice_dialog)  # 菜单栏1触发器
        self.action2.triggered.connect(self.update_dialog)  # 菜单栏2触发器
        self.com_box.activated[str].connect(self.com_box_select)  # 连接拼接数量
        self.com_box2.activated[str].connect(self.com_box_select2)  # 连接压缩宽度
        self.button1.clicked.connect(self.file_select)  # 连接选择文件
        self.button2.clicked.connect(self.do_action)  # 连接开始转换
        self.button3.clicked.connect(qApp.quit)
        self.line_edit2.textEdited.connect(self.line_value_change)

    def com_box_select(self, text):
        self.png_num = int(text)
        print(text)

    def com_box_select2(self, text):
        self.png_type = str(text)
        print(text)

    def line_value_change(self, value):
        self.line_value = str(value)
        print(value)

    def file_select(self):
        """
        文件选择
        """
        f_dialog = QFileDialog()
        f_dialog.setGeometry(350, 350, 300, 150)
        f_dialog.setWindowIcon(QIcon('tools.png'))
        f_dialog.setWindowTitle('选择文件')
        file = f_dialog.getOpenFileName()
        if bool(file[0]):
            self.line_edit.setText(file[0])
            self.file_path = file[0]

    @staticmethod
    def dialog(size, title, text):
        dialog = QDialog()
        dialog.setStyleSheet("font-size:12px; font-weight:normal")
        dialog.setGeometry(*size)
        dialog.setWindowTitle(title)
        dialog.setWindowIcon(QIcon('tools.png'))
        label = QLabel(text, dialog)
        # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def notice_dialog(self):
        text = """\
使用说明：
1.点击选择文件，选择好你的pdf文件
2.选择好拼接数量
3.点击开始转换，根据需求依次选择三个按钮
备注：
1.拼接长度指的是多少张图拼接成一张
2.压缩质量值得是压缩后的长图分辨率，
  普通模式即自动压缩成1M以内，
  720p和1080p则自动压缩图片为这个宽度
        """
        self.dialog((330, 330, 300, 160), '使用说明', text)

    def update_dialog(self):
        text = """\
V1.0版更新记录：
1.使用PyQt5重构了界面
2.增加了进度条，减少等待时间
3.选择pdf文件时，默认上次的路径
4.增加了二次确认操作
5.使用多线程，提高了软件速度
6.美化了GUI，变得好看了
        """
        self.dialog((350, 350, 300, 160), '更新记录', text)

    def do_action(self):
        """
        进度条, main Process
        :param
        """
        print(self.file_path)

        if self.file_path is None:
            text = '亲，你还没有选择文件路径'
            replay = QMessageBox.warning(self, '提示', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        else:
            file_name0 = path.split(self.file_path)[1]
            self.file_name = path.splitext(file_name0)[0]
            file_type = path.splitext(file_name0)[1]
            if file_type.upper() != '.PDF':
                text = '亲，你选择的不是pdf文件'
                replay = QMessageBox.warning(self, '提示', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            else:
                self.button_dialog()

    def button_dialog(self):
        """
        这个主要用于选择会话
        """
        dialog = QDialog()
        dialog.setStyleSheet("font-size:12px; font-weight:normal")
        dialog.setGeometry(300, 330, 300, 88)
        dialog.setWindowIcon(QIcon('tools.png'))
        dialog.setWindowTitle('请选择')
        button1 = QPushButton('pdf转png', dialog)
        button1.clicked.connect(self.pdf2png)  # pdf转png
        button1.setGeometry(10, 30, 81, 30)
        button2 = QPushButton('png拼接', dialog)
        button2.clicked.connect(self.twice_confirm)  # 生成长图
        button2.setGeometry(110, 30, 81, 30)
        button3 = QPushButton('长图压缩', dialog)
        button3.setGeometry(210, 30, 81, 30)
        button3.clicked.connect(self.twice_confirm2)  # 压缩长图
        dialog.exec_()

    def twice_confirm(self):
        """
        用于生成长图的二次确认
        """
        pdf = PdfInit(self.file_path)
        list1 = listdir(pdf.out_put_dir)
        if len(list1) == 0:  # 如果路径不1存在
            replay = QMessageBox.warning(self, '错误', '亲，你还没有将pdf导出成图片，请选择"pdf转png"',
                                         QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        else:
            replay = QMessageBox.warning(self, '请确认', '你当前准备将"{}"张图片拼接成一张图片，是否确认？'.format(self.png_num),
                                         QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if replay == 16384:
                print('yes')
                self.gen_long_png()
            elif replay == 65536:
                print('No')

    def twice_confirm2(self):
        """
        用于压缩长图的二次确认
        """
        file_name0 = path.split(self.file_path)[1]
        file_name = path.splitext(file_name0)[0]
        long_out_dir = path.join(getcwd(), '导出路径', file_name+'_长图')
        if not path.exists(long_out_dir):
            replay = QMessageBox.warning(self, '错误', '亲，压缩图片需要将png转成长图后才能操作，请选择"长图压缩"',
                                         QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        else:
            list1 = listdir(long_out_dir)
            if len(list1) == 0:  # 如果路径不存在
                replay = QMessageBox.warning(self, '错误', '亲，压缩图片需要将png转成长图后才能操作，请选择"长图压缩"',
                                             QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            else:
                replay = QMessageBox.warning(self, '请确认',
                                             '你当前设置的图片压缩质量为："{}", 压缩率为："{}%", 是否确认'.\
                                             format(self.png_type, self.line_value),
                                             QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
                if replay == 16384:
                    print('yes')
                    self.zip_png()  # 压缩图片
                elif replay == 65536:
                    print('No')

    def pdf2png(self):
        pdf = PdfInit(self.file_path)  # 处理pdf
        self.show_process_bar('正在将pdf转成单张图片, 请稍后')
        self.my_dialog1 = Pdf2Png(pdf)
        self.my_dialog1.start()
        self.my_dialog1.trigger.connect(self.process_pdf2png)

    def gen_long_png(self):
        pdf = PdfInit(self.file_path)  # 处理pdf
        self.show_process_bar('正在拼接长图, 请稍后')
        # print(self.file_name, self.png_num, pdf.out_put_dir)
        self.my_dialog2 = GenLongPng(self.file_name, self.png_num, pdf.out_put_dir)
        self.my_dialog2.start()
        self.my_dialog2.trigger.connect(self.process_pdf2png)

    def zip_png(self):
        """
        压缩图片
        """
        file_name0 = path.split(self.file_path)[1]
        file_name = path.splitext(file_name0)[0]  # 获取文件名
        self.show_process_bar('正在压缩长图, 请稍后')
#         print(file_name, float(self.line_value), self.png_type)
        self.my_dialog3 = ZipPng(file_name, float(self.line_value), self.png_type)
        self.my_dialog3.start()
        self.my_dialog3.trigger.connect(self.process_pdf2png)  # 连接处理压缩进度函数，可以和之前的长图一样的

    def show_process_bar(self, label_text):
        """
        显示进度条
        """
        self.progress = QProgressDialog()  # 设定窗口
        self.progress.setGeometry(320, 190, 250, 100)
        self.progress.setWindowIcon(QIcon('tools.png'))
        self.progress.setMinimumSize(250, 100)
        label = QLabel(label_text, self.progress)
        label.move(12, 18)
        label.setStyleSheet("font-size:12px; font-weight:normal")
        self.progress.setWindowTitle('进度条')
        self.progress.setRange(0, 100)
        self.progress.show()

    def process_pdf2png(self, int1, int2):
        # print(int1, int2)
        value = int((int1 + 1) * 100 / int2)  # 这里的页面数量需要加1
        self.progress.setValue(value)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    pdf_main = PdfMain()
    sys.exit(app.exec_())
