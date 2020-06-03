from ui import UI
import sys
from tool import *
from os import path, listdir
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox, QProgressDialog, QLabel, qApp
from PyQt5.QtGui import QIcon
import json
import base64
from tools_png import img


class PdfMain(UI):
    def __init__(self):
        super(PdfMain, self).__init__()
        # --- 窗口1 --- #
        self.my_dialog1_1 = None  # 会话1，展示pdf转png进度
        self.pdf_path = None

        # --- 窗口2 --- #
        self.pdf_dir1 = None
        self.my_dialog2_1 = None  # 会话2_1,用于单列转长图
        self.my_dialog2_2 = None  # 会话2_2，用于转矩阵长图
        self.dialog_line_edit1_value = None  # 拼接数量
        self.dialog_line_edit2_value = None  # 拼接行数
        self.dialog_line_edit3_value = None  # 拼接列数
        self.dialog_line_edit4_value = None  # 拼接间隙

        # --- 窗口3 --- #
        self.pdf_dir2 = None  # 文件夹路径
        self.width_model = '普通'  # 图片宽度模式
        self.picture_type = 'jpg'  # 图片格式
        self.zip_num = None  # 图片压缩率
        self.my_dialog3 = None  # 会话3，用于压缩图片

        # -- 运行窗口 -- #
        self.init_action()

    def init_action(self):
        self.show_frame1()

    def show_frame1(self):
        """
        重写窗口1的方法，加入按钮监控
        :return:
        """
        super(PdfMain, self).show_frame1()
        self.push_button1_1.clicked.connect(self.file_select)  # 连接选择文件
        self.push_button1_2.clicked.connect(self.do_convert)  # 连接开始转换
        self.push_button1_3.clicked.connect(qApp.quit)  # 连接退出软件

    def show_frame2(self):
        super(PdfMain, self).show_frame2()
        self.push_button2_1.clicked.connect(self.dir1_select)  # 连接选择文件夹
        self.push_button2_2.clicked.connect(self.one_step2long)  # 连接一键长图

    def show_frame3(self):
        super(PdfMain, self).show_frame3()

        # 加入上次的输入框
        width_model = self.read_data_dict('width_model')
        picture_type = self.read_data_dict('picture_type')
        pdf_dir2 = self.read_data_dict('pdf_dir2')
        zip_num = self.read_data_dict('zip_num')
        if pdf_dir2 is not None:
            self.line_edit3_1.setText(pdf_dir2)
            self.pdf_dir2 = pdf_dir2
        if zip_num is not None:
            self.line_edit3_2.setText(zip_num)
            self.zip_num = zip_num
        else:
            self.line_edit3_2.setText('92')
            self.zip_num = '92'
        if width_model is not None:
            self.width_model = width_model
            self.combo_box3_1.setCurrentText(width_model)
        if picture_type is not None:
            self.picture_type = picture_type
            self.combo_box3_2.setCurrentText(picture_type)
        # 监控按键3-1：自定义路径
        self.push_button3_1.clicked.connect(self.dir2_select)
        # 检测下拉框：压缩宽度
        self.combo_box3_1.activated[str].connect(self.combo_box3_1_select)  # 图片宽度模式
        self.combo_box3_2.activated[str].connect(self.combo_box3_2_select)  # 图片格式
        self.line_edit3_2.textEdited.connect(self.line_edit3_2_change)  # 压缩比
        # 连接一键压缩
        self.push_button3_2.clicked.connect(self.one_step_zip)  # 连接一键压缩

    # 公用进度条
    def show_process_bar(self, label_text):
        """
        显示进度条
        """
        self.progress = QProgressDialog()  # 设定窗口
        # self.progress.setGeometry(320, 190, 250, 100)
        self.progress.resize(250, 100)
        self.progress.setWindowIcon(QIcon('tools.png'))
        self.progress.setMinimumSize(250, 100)
        label = QLabel(label_text, self.progress)
        label.move(12, 18)
        label.setStyleSheet("font-size:12px; font-weight:normal")
        self.progress.setWindowTitle('进度条')
        self.progress.setRange(0, 100)
        self.progress.show()

# ----- 以下方法用于窗口1------------- #
    def file_select(self):
        """
        文件选择,用于窗口1
        """
        f_dialog = QFileDialog()
        # f_dialog.setGeometry(350, 350, 300, 150)
        f_dialog.setWindowIcon(QIcon('tools.png'))
        f_dialog.setWindowTitle('选择文件')
        file = f_dialog.getOpenFileName()
        if bool(file[0]):
            self.line_edit1_1.setText(file[0])
            self.pdf_path = file[0]

    def do_convert(self):
        """
        进度条, main Process
        :param
        """
        if self.pdf_path is None:
            pdf_path = self.read_data_dict('pdf_path')
            if pdf_path is None:
                text = '亲，你还没有选择文件路径'
                QMessageBox.warning(self, '错误', text,
                                    QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            else:
                text = '亲，确认使用上次的路径？'
                replay = QMessageBox.warning(self, '错误', text,
                                    QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
                if replay != 65536:
                    self.pdf_path = pdf_path
                    self.pdf2png()

        else:
            file_name0 = path.split(self.pdf_path)[1]
            # pdf_name = path.splitext(file_name0)[0]
            file_type = path.splitext(file_name0)[1]
            if file_type.upper() != '.PDF':
                text = '亲，你选择的不是pdf文件'
                QMessageBox.warning(self, '错误', text,
                                    QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            else:
                self.write_data_dict('pdf_path', self.pdf_path)  # 将pdf路径保存到字典
                self.pdf2png()

    def pdf2png(self):
        """
        用于pdf转png
        :return:
        """
        pdf = PdfInit(self.pdf_path)  # 处理pdf
        self.show_process_bar('正在将pdf转成单张图片, 请稍后')
        self.my_dialog1_1 = Pdf2Png(pdf)
        self.my_dialog1_1.start()
        self.my_dialog1_1.trigger.connect(self.process_pdf2png)

    def process_pdf2png(self, int1, int2):
        print(int1, int2)
        value = int((int1 + 1) * 100 / int2)  # 这里的页面数量需要加1
        self.progress.setValue(value)

# ----- 以下方法用于窗口2------------- #
    def dir1_select(self):
        """
        自定义路径
        :return:
        """
        f_dialog2 = QFileDialog()
        # f_dialog.setGeometry(350, 350, 300, 150)
        f_dialog2.setWindowIcon(QIcon('tools.png'))
        f_dialog2.setWindowTitle('选择文件夹')
        dir1 = f_dialog2.getExistingDirectory()
        if bool(dir1):
            self.line_edit2_1.setText(dir1)
            self.pdf_dir1 = dir1

    def one_step2long(self):
        """
        一键生成长图
        :return:
        """
        text_list = listdir(self.pdf_dir1)
        text_list2 = [fn for fn in text_list if fn.endswith('.png') or fn.endswith('jpg')]
        if len(text_list2) == 0:
            text = "你当前路径下没有任何png或者jpg图片"
            QMessageBox.warning(self, '警告', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
        else:
            if self.pdf_dir1 is not None:
                png_list = listdir(self.pdf_dir1)
                png_num = len(png_list)  # 获取图片数量
                parent_path = path.split(self.pdf_dir1)[0]  # 获取父目录
                out_path = parent_path + '/一键长图'
                my_dialog2_1 = GenLongPng(png_num, self.pdf_dir1, out_path)
                my_dialog2_1.run()
                text = "长图生成成功，请到pdf同路径的”一键长图“文件夹查看"
                QMessageBox.warning(self, '恭喜', text,
                                    QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)

            else:
                text = "亲！你还没有选择图片所在文件夹"
                QMessageBox.warning(self, '警告', text,
                                    QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
    
    def show_dialog1(self):
        """
        重写会话1系统，用于单列拼接
        :return: 
        """
        super(PdfMain, self).show_dialog1()
        # 加入上次的输入框
        dialog_line_edit1_value = self.read_data_dict('dialog_line_edit1_value')
        if dialog_line_edit1_value is not None:
            self.dialog_line_edit1.setText(dialog_line_edit1_value)
            self.dialog_line_edit1_value = dialog_line_edit1_value
        # 监控输入框变化
        self.dialog_line_edit1.textEdited.connect(self.dialog_line_edit1_change)
        # 检测按钮：一键转换单列长图
        self.dialog_push_button1.clicked.connect(self.customize_one_column_long_png)
        self.dialog1.show()

    def customize_one_column_long_png(self):
        text_list = listdir(self.pdf_dir1)
        text_list2 = [fn for fn in text_list if fn.endswith('.png') or fn.endswith('jpg')]
        if len(text_list2) == 0:
            text = "你当前路径下没有任何png或者jpg图片"
            QMessageBox.warning(self, '警告', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
        else:
            if self.dialog_line_edit1_value is None:
                png_list = listdir(self.pdf_dir1)
                png_num = len(png_list)  # 获取图片数量
                text = "亲！还没有输入<b>”拼接数量“</b>呢？最大不能超过图片总数<b>{}</b>哦".format(png_num)
                QMessageBox.warning(self, '警告', text,
                                    QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            else:
                parent_path = path.split(self.pdf_dir1)[0]  # 获取父目录
                out_path = parent_path + '/单列长图'
                self.write_data_dict('dialog_line_edit1_value', self.dialog_line_edit1_value)  # 存入字典
                self.show_process_bar('正在将图片拼接成多张长图, 请稍后')
                self.my_dialog2_1 = GenLongPng(int(self.dialog_line_edit1_value), self.pdf_dir1, out_path)
                self.my_dialog2_1.start()
                self.my_dialog2_1.trigger.connect(self.process_pdf2png)

    def dialog_line_edit1_change(self, value):
        if self.is_number(value) and '.' not in value:  # 如果属于数字并且为整数
            png_list = listdir(self.pdf_dir1)
            png_num = len(png_list)  # 获取图片数量
            if int(float(value)) > png_num:
                text = "亲！最大不能超过图片数量，当前文件夹只有{}张图片。".format(png_num)
                QMessageBox.warning(self, '警告', text,
                                    QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
                self.dialog_line_edit1.setText(None)
            else:
                self.dialog_line_edit1_value = str(value)
        else:
            text = "亲！只能输入整数"
            QMessageBox.warning(self, '警告', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            self.dialog_line_edit1.setText(None)

    @staticmethod
    def is_number(s):
        """
        检测是否为数字
        :param s:
        :return:
        """
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def show_dialog2(self):
        """
        重写会话2系统，用于矩阵拼接
        :return:
        """
        super(PdfMain, self).show_dialog2()
        # 加入上次的输入框
        dialog_line_edit2_value = self.read_data_dict('dialog_line_edit2_value')
        dialog_line_edit3_value = self.read_data_dict('dialog_line_edit3_value')
        dialog_line_edit4_value = self.read_data_dict('dialog_line_edit4_value')
        if dialog_line_edit2_value is not None:
            self.dialog_line_edit2.setText(dialog_line_edit2_value)
            self.dialog_line_edit2_value = dialog_line_edit2_value
        if dialog_line_edit3_value is not None:
            self.dialog_line_edit3.setText(dialog_line_edit3_value)
            self.dialog_line_edit3_value = dialog_line_edit3_value
        else:
            self.dialog_line_edit3.setText('1')
            self.dialog_line_edit3_value = '1'
        if dialog_line_edit4_value is not None:
            self.dialog_line_edit4.setText(dialog_line_edit4_value)
            self.dialog_line_edit4_value = dialog_line_edit4_value
        else:
            self.dialog_line_edit4.setText('0')
            self.dialog_line_edit4_value = '0'
        # 监控输入框变化
        self.dialog_line_edit2.textEdited.connect(self.dialog_line_edit2_change)  # 检测行数
        self.dialog_line_edit3.textEdited.connect(self.dialog_line_edit3_change)  # 检测列数
        self.dialog_line_edit4.textEdited.connect(self.dialog_line_edit4_change)  # 检测px像素
        self.dialog_push_button2.clicked.connect(self.matrix_long_png)  # 矩阵拼图
        self.dialog2.show()

    def dialog_line_edit2_change(self, value):
        """
        检测列数量
        :param value:
        :return:
        """
        if self.is_number(value) and '.' not in value:  # 如果属于数字并且为整数
            png_list = listdir(self.pdf_dir1)
            png_num = len(png_list)  # 获取图片数量
            if int(float(value)) > png_num:
                text = "亲！最大不能超过图片数量，当前文件夹只有{}张图片。".format(png_num)
                QMessageBox.warning(self, '警告', text,
                                    QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
                self.dialog_line_edit2.setText(None)
            else:
                self.dialog_line_edit2_value = str(value)
        else:
            text = "亲！只能输入整数"
            QMessageBox.warning(self, '警告', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            self.dialog_line_edit2.setText(None)

    def dialog_line_edit3_change(self, value):
        """
        检测行数量
        :param value:
        :return:
        """
        if self.is_number(value) and '.' not in value:  # 如果属于数字并且为整数
            png_list = listdir(self.pdf_dir1)
            png_num = len(png_list)  # 获取图片数量
            if int(float(value)) > png_num:
                text = "亲！最大不能超过图片数量，当前文件夹只有{}张图片。".format(png_num)
                QMessageBox.warning(self, '警告', text,
                                    QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
                self.dialog_line_edit3.setText(None)
            else:
                self.dialog_line_edit3_value = str(value)
        else:
            text = "亲！只能输入整数"
            QMessageBox.warning(self, '警告', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            self.dialog_line_edit3.setText(None)

    def dialog_line_edit4_change(self, value):
        """
        检测像素间隔px值
        :param value:
        :return:
        """
        if self.is_number(value) and '.' not in value:  # 如果属于数字并且为整数
            self.dialog_line_edit4_value = str(value)
        else:
            text = "亲！只能输入整数"
            QMessageBox.warning(self, '警告', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            self.dialog_line_edit4.setText(None)

    def matrix_long_png(self):
        """
        自定义拼图之矩阵拼图
        :return:
        """
        text_list = listdir(self.pdf_dir1)
        text_list2 = [fn for fn in text_list if fn.endswith('.png') or fn.endswith('jpg')]
        if len(text_list2) == 0:
            text = "你当前路径下没有任何png或者jpg图片"
            QMessageBox.warning(self, '警告', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
        else:
            result = False
            png_list = listdir(self.pdf_dir1)
            png_num = len(png_list)  # 获取图片数量
            if self.dialog_line_edit2_value is None or self.dialog_line_edit3_value is None or \
                    self.dialog_line_edit3_value is None:
                text = "亲！还有三个空没填全，没法开始"
                QMessageBox.warning(self, '警告', text,
                                    QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            elif int(float(self.dialog_line_edit2_value)) * int(float(self.dialog_line_edit3_value)) > png_num:
                text = "行与列之积大于总图片数量，将会产生较多空白，是否继续？"
                replay = QMessageBox.warning(self, '警告', text,
                                             QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
                if replay != 65536:  # 如果选择”yes“
                    result = True
            else:
                result = True
            if bool(result):
                self.write_data_dict('dialog_line_edit2_value', self.dialog_line_edit2_value)
                self.write_data_dict('dialog_line_edit3_value', self.dialog_line_edit3_value)
                self.write_data_dict('dialog_line_edit4_value', self.dialog_line_edit4_value)
                row = int(self.dialog_line_edit2_value)
                column = int(self.dialog_line_edit3_value)
                interval = int(self.dialog_line_edit4_value)
                parent_path = path.split(self.pdf_dir1)[0]  # 获取父目录
                out_path = parent_path + '/矩阵长图'
                self.show_process_bar('正在将图片拼接成多张长图, 请稍后')
                self.my_dialog2_2 = GenLongPng2(row, column, interval, self.pdf_dir1, out_path)
                self.my_dialog2_2.start()
                self.my_dialog2_2.trigger.connect(self.process_pdf2png)

# --- 以下代码用于窗口3 --- #
    def dir2_select(self):
        """
        自定义路径
        :return:
        """
        f_dialog2 = QFileDialog()
        # f_dialog.setGeometry(350, 350, 300, 150)
        f_dialog2.setWindowIcon(QIcon('tools.png'))
        f_dialog2.setWindowTitle('选择文件夹')
        dir2 = f_dialog2.getExistingDirectory()
        if bool(dir2):
            self.line_edit3_1.setText(dir2)
            self.pdf_dir2 = dir2

    def combo_box3_1_select(self, text):
        """
        此方法用于选择图片宽度
        :param text: 接收的文本
        :return:
        """
        self.width_model = str(text)
        print(text)

    def combo_box3_2_select(self, text):
        """
        此方法用于选择图片格式
        :param text: 接收的文本
        :return:
        """
        self.picture_type = str(text)
        print(text)

    def line_edit3_2_change(self, value):
        if self.is_number(value) and '.' not in value:  # 如果属于数字并且为整数
            self.zip_num = str(value)
        else:
            text = "亲！只能输入整数"
            QMessageBox.warning(self, '警告', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            self.line_edit3_2.setText(None)

    def one_step_zip(self):
        # 查看一下路径里面有没有图片
        text_list = listdir(self.pdf_dir2)
        text_list2 = [fn for fn in text_list if fn.endswith('.png') or fn.endswith('jpg')]
        if len(text_list2) == 0:
            text = "你当前路径下没有任何png或者jpg图片"
            QMessageBox.warning(self, '警告', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
        else:
            text = "你的当前配置是：宽度模式：<b>”{}“</b>, 格式: <b>”{}“</b>， 压缩比：<b>”{}%“</b><br>路径：<b>”{}“</b><br>是否确认？"\
                .format(self.width_model, self.picture_type, self.zip_num, self.pdf_dir2)
            replay = QMessageBox.warning(self, '提示', text,
                                QMessageBox.Yes | QMessageBox.Yes, QMessageBox.No)
            print(replay)
            if replay != 65536:
                # -- 保存相关配置到字典中 -- #
                self.write_data_dict('width_model', self.width_model)
                self.write_data_dict('picture_type', self.picture_type)
                self.write_data_dict('zip_num', self.zip_num)
                self.write_data_dict('pdf_dir2', self.pdf_dir2)
                # -- 保存完毕 --- #
                self.show_process_bar('正在压缩图片, 请稍后')
                # print(self.width_model, self.picture_type, self.zip_num, self.pdf_dir2)
                self.my_dialog3 = ZipPng(self.width_model, self.picture_type, int(self.zip_num), self.pdf_dir2)
                self.my_dialog3.start()
                self.my_dialog3.trigger.connect(self.process_pdf2png)


if __name__ == '__main__':
    # 创建一个data.json文件，用于储存变量参数
    if not path.exists('data.json'):
        data_dict = {}
        with open('data.json', 'wt', encoding='utf-8') as f:
            json.dump(data_dict, f)
    if not path.exists('tools.png'):
        img_data = base64.b64decode(img)
        f = open('tools.png', 'wb')
        f.write(img_data)
        f.close()
    app = QApplication(sys.argv)
    pdf_main = PdfMain()
    sys.exit(app.exec_())