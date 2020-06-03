from PyQt5.QtWidgets import QMainWindow, QMenuBar, QApplication, QAction, QWidget, QPushButton, QLabel, QLineEdit,\
    QComboBox, QDialog, QDesktopWidget
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sys
import json
from os import path, getcwd


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        # -- 基础设置 -- #
        self.cp = QDesktopWidget().availableGeometry().center()
        qr = self.frameGeometry()
        qr.moveCenter(self.cp)
        self.move(qr.topLeft())
        self.resize(340, 150)
        self.setMinimumSize(340, 150)
        self.setMaximumSize(340, 150)
        self.setWindowTitle('pdf转长图助手')
        self.setWindowIcon(QIcon('tools.png'))
        # --字体设置--#
        # 字体8号
        self.font_8 = QFont()
        self.font_8.setPointSize(8)
        # 字体9号
        self.font_9 = QFont()
        self.font_9.setPointSize(9)

        # --菜单控件设置 -- #
        self.menubar = QMenuBar()  # 这里暂时不设置父类
        self.menubar.setFont(self.font_8)
        menu = self.menubar.addMenu('&菜单')
        self.menu_about = self.menubar.addMenu('&关于')
        self.action4 = QAction('版本号', self)
        self.action4.setFont(self.font_8)
        self.menu_about.addAction(self.action4)
        self.action4.triggered.connect(self.about_dialog)  # 菜单栏4触发器
        self.action1 = QAction('使用说明', self)
        self.action1.setFont(self.font_8)
        self.action2 = QAction('更新记录', self)
        self.action2.setFont(self.font_8)
        self.action3 = QAction('我要反馈', self)
        self.action3.setFont(self.font_8)
        menu.addAction(self.action1)
        menu.addAction(self.action2)
        menu.addAction(self.action3)

        # -- 菜单控制连接器
        self.action1.triggered.connect(self.notice_dialog)  # 菜单栏1触发器
        self.action2.triggered.connect(self.update_dialog)  # 菜单栏2触发器
        self.action3.triggered.connect(self.feedback_dialog)  # 菜单栏3触发器

        # -- 窗口1
        self.frame1 = None
        self.line_edit1_1 = None  # 窗口1的文件夹路径
        self.pdf_path = None  # 窗口1的pdf路径
        self.push_button1_1 = QPushButton()  # 按钮1_1,选择文件
        self.push_button1_2 = QPushButton()  # 按钮1_2,pdf转png
        self.push_button1_3 = QPushButton()  # 按钮1_3,我要退出

        # --窗口2
        self.frame2 = None
        self.line_edit2_1 = None  # 输入框
        self.pdf_dir1 = None  # pdf转成图片后的文件夹
        self.push_button2_1 = QPushButton()  # 按钮2_1：自定义路径
        self.push_button2_2 = QPushButton()  # 按钮2_2：一键长图
        self.push_button2_3 = QPushButton()  # 按钮2_3:自定义拼接

        # --窗口3
        self.frame3 = None
        self.pdf_dir2 = None
        self.line_edit3_1 = None  # 输入框
        self.combo_box3_1 = None  # 多选框3_1
        self.combo_box3_2 = None  # 多选框3_2
        self.line_edit3_2 = None  # 输入框百分比
        self.push_button3_1 = QPushButton()  # 自定义路径
        self.push_button3_2 = QPushButton()  # 一键压缩
        self.push_button3_3 = QPushButton()  # 退出软件

        # --- dialog会话 --
        self.dialog_line_edit1 = None  # 会话输入框1：拼接数量
        self.dialog_line_edit2 = None  # 会话输入框2：拼接列数
        self.dialog_line_edit3 = None  # 会话输入框3：拼接行数
        self.dialog_line_edit4 = None  # 会话输入框4：拼接间隙
        self.dialog_push_button1 = None  # 会话按钮1：开始单列拼接
        self.dialog_push_button2 = None  # 会话按钮1：开始矩阵拼接
        self.dialog1 = None  # 单列拼接
        self.dialog2 = None  # 矩阵拼接

        # --运行主界面--#
        self.init_ui()

    def init_ui(self):
        self.show_frame1()
        self.show()

    def show_frame1(self):
        self.frame1 = QWidget(self)
        super(QWidget, self.frame1).__init__()
        # --按钮标签1：格式转换，用来代替按钮1
        button_label1 = QLabel(self.frame1)
        button_label1.setGeometry(90, 0, 80, 24)
        button_label1.setFont(self.font_8)
        button_label1.setText('格式转换')
        button_label1.setAlignment(Qt.AlignCenter)
        # 转换按键
        # --按钮2：图片拼接
        push_button2 = QPushButton(self.frame1)
        push_button2.setGeometry(170, 0, 80, 24)
        push_button2.setFont(self.font_8)
        push_button2.setText('图片拼接')
        push_button2.clicked.connect(self.show_frame2)  # 连接件显示窗口2
        # --按钮3：图片压缩
        push_button3 = QPushButton(self.frame1)
        push_button3.setGeometry(250, 0, 80, 24)
        push_button3.setFont(self.font_8)
        push_button3.setText('图片压缩')
        push_button3.clicked.connect(self.show_frame3)  # 连接件显示窗口3

        # --标签1：pdf路径
        label1_1 = QLabel(self.frame1)
        label1_1.setText('pdf路径')
        label1_1.setFont(self.font_8)
        label1_1.setAlignment(Qt.AlignCenter)
        label1_1.setGeometry(15, 40, 69, 20)

        # --路径1：pdf路径
        self.line_edit1_1 = QLineEdit(self.frame1)
        self.line_edit1_1.setFont(self.font_8)
        self.line_edit1_1.setGeometry(90, 40, 220, 26)
        # 加入上次的路径保留
        pdf_path = self.read_data_dict('pdf_path')
        if pdf_path is not None:
            self.line_edit1_1.setText(pdf_path)

        # -- 按钮1_1：选择pdf文件
        self.push_button1_1 = QPushButton(self.frame1)
        self.push_button1_1.setGeometry(10, 95, 93, 29)
        self.push_button1_1.setText('选择文件')
        self.push_button1_1.setFont(self.font_9)
        # -- 按钮1_2：pdf转png
        self.push_button1_2 = QPushButton(self.frame1)
        self.push_button1_2.setGeometry(115, 95, 93, 29)
        self.push_button1_2.setText('pdf转png')
        self.push_button1_2.setFont(self.font_9)
        # -- 按钮1_3：我要退出
        self.push_button1_3 = QPushButton(self.frame1)
        self.push_button1_3.setGeometry(220, 95, 93, 29)
        self.push_button1_3.setText('退出软件')
        self.push_button1_3.setFont(self.font_9)

        # 移动其它控件
        self.menubar.setParent(self.frame1)  # 设置菜单栏依赖于窗口1
        self.setCentralWidget(self.frame1)  # 设置主窗口的当前窗口为窗口1
        self.frame1.setVisible(True)

    def show_frame2(self):
        # 重新定义构件
        self.frame2 = QWidget(self)
        super(QWidget, self.frame2).__init__()
        # --按钮1：格式转换
        push_button1 = QPushButton(self.frame2)
        push_button1.setGeometry(90, 0, 80, 24)
        push_button1.setFont(self.font_8)
        push_button1.setText('格式转换')
        push_button1.clicked.connect(self.show_frame1)

        # --按钮标签2：格式转换，用来代替按钮2
        button_label2 = QLabel(self.frame2)  # 暂时不设置父标签
        button_label2.setGeometry(170, 0, 80, 24)
        button_label2.setFont(self.font_8)
        button_label2.setText('图片拼接')
        button_label2.setAlignment(Qt.AlignCenter)
        # --按钮3：图片压缩
        push_button3 = QPushButton(self.frame2)
        push_button3.setGeometry(250, 0, 80, 24)
        push_button3.setFont(self.font_8)
        push_button3.setText('图片压缩')
        push_button3.clicked.connect(self.show_frame3)  # 连接件显示窗口3

        # -- 标签2_1:文件夹路径
        label2_1 = QLabel(self.frame2)
        label2_1.setGeometry(15, 40, 80, 20)
        label2_1.setText('文件夹路径')
        label2_1.setFont(self.font_8)

        # -- 输入框2_1:文件夹路径
        self.line_edit2_1 = QLineEdit(self.frame2)
        self.line_edit2_1.setGeometry(90, 40, 220, 26)
        self.line_edit2_1.setFont(self.font_8)

        # 加入默认路径
        pdf_path = self.read_data_dict('pdf_path')
        if pdf_path is not None:
            dir1 = path.split(pdf_path)[0]
            self.pdf_dir1 = dir1 + '/导出图片'
            self.line_edit2_1.setText(self.pdf_dir1)

        # -- 按钮2_1：自定义路径
        self.push_button2_1 = QPushButton(self.frame2)
        self.push_button2_1.setGeometry(10, 95, 93, 29)
        self.push_button2_1.setText('自定义路径')
        self.push_button2_1.setFont(self.font_9)
        # -- 按钮2_2：一键长图
        self.push_button2_2 = QPushButton(self.frame2)
        self.push_button2_2.setGeometry(115, 95, 93, 29)
        self.push_button2_2.setText('一键长图')
        self.push_button2_2.setFont(self.font_9)
        # -- 按钮2_3：自定义拼接
        self.push_button2_3 = QPushButton(self.frame2)
        self.push_button2_3.setGeometry(220, 95, 93, 29)
        self.push_button2_3.setText('自定义拼接')
        self.push_button2_3.setFont(self.font_9)
        self.push_button2_3.clicked.connect(self.show_dialog)
        # -- 移动其它控件
        self.menubar.setParent(self.frame2)  # 设置菜单栏依赖于窗口2
        self.setCentralWidget(self.frame2)
        self.frame2.setVisible(True)

    def show_frame3(self):
        self.frame3 = QWidget(self)
        super(QWidget, self.frame3).__init__()
        # --按钮1：格式转换
        push_button1 = QPushButton(self.frame3)
        push_button1.setGeometry(90, 0, 80, 24)
        push_button1.setFont(self.font_8)
        push_button1.setText('格式转换')
        push_button1.clicked.connect(self.show_frame1)

        # --按钮2：图片拼接
        push_button2 = QPushButton(self.frame3)
        push_button2.setGeometry(170, 0, 80, 24)
        push_button2.setFont(self.font_8)
        push_button2.setText('图片拼接')
        push_button2.clicked.connect(self.show_frame2)  # 连接件显示窗口2
        # -- 设置主窗口
        self.setCentralWidget(self.frame3)

        # -- 标签3：图片压缩
        button_label3 = QLabel(self.frame3)
        button_label3.setGeometry(250, 0, 80, 24)
        button_label3.setFont(self.font_8)
        button_label3.setText('图片压缩')
        button_label3.setAlignment(Qt.AlignCenter)
        # -- 标签3_1：文件夹路径
        label3_1 = QLabel(self.frame3)
        label3_1.setGeometry(15, 40, 80, 20)
        label3_1.setText('文件夹路径')
        label3_1.setFont(self.font_8)
        # -- 输入框3_1:文件夹路径
        self.line_edit3_1 = QLineEdit(self.frame3)
        self.line_edit3_1.setFont(self.font_8)
        self.line_edit3_1.setGeometry(90, 40, 220, 26)
        # 加入默认路径
        pdf_path = self.read_data_dict('pdf_path')
        if pdf_path is not None:
            dir1 = path.split(pdf_path)[0]
            self.pdf_dir2 = dir1 + '/单列长图'
            self.line_edit3_1.setText(self.pdf_dir2)
        # -- 标签3_2：宽度
        label3_2 = QLabel(self.frame3)
        label3_2.setGeometry(10, 80, 35, 20)
        label3_2.setText('宽度')
        label3_2.setFont(self.font_8)
        # -- 多选框3_1
        self.combo_box3_1 = QComboBox(self.frame3)
        self.combo_box3_1.setGeometry(45, 80, 60, 25)
        self.combo_box3_1.addItems(['普通', '720p', '1080p'])
        self.combo_box3_1.setFont(self.font_8)
        # -- 多选框3_2
        self.combo_box3_2 = QComboBox(self.frame3)
        self.combo_box3_2.setGeometry(155, 80, 50, 25)
        self.combo_box3_2.addItems(['jpg', 'png'])
        self.combo_box3_2.setFont(self.font_8)
        # -- 标签3_3
        label3_3 = QLabel(self.frame3)
        label3_3.setGeometry(120, 80, 40, 20)
        label3_3.setText('格式')
        label3_3.setFont(self.font_8)
        # -- 标签3_4
        label3_4 = QLabel(self.frame3)
        label3_4.setGeometry(220, 80, 51, 20)
        label3_4.setText('压缩比')
        label3_4.setFont(self.font_8)
        # -- 输入框3_2：压缩百分比
        self.line_edit3_2 = QLineEdit(self.frame3)
        self.line_edit3_2.setGeometry(265, 80, 25, 25)
        self.line_edit3_2.setFont(self.font_8)
        # -- 标签3_5
        label3_4 = QLabel(self.frame3)
        label3_4.setGeometry(295, 80, 14, 20)
        label3_4.setText('%')
        label3_4.setFont(self.font_8)
        # -- 按键3_1：自定义路径
        self.push_button3_1 = QPushButton(self.frame3)
        self.push_button3_1.setGeometry(10, 115, 93, 29)
        self.push_button3_1.setText('自定义路径')
        self.push_button3_1.setFont(self.font_9)
        # -- 按键3_2：一键压缩
        self.push_button3_2 = QPushButton(self.frame3)
        self.push_button3_2.setGeometry(115, 115, 93, 29)
        self.push_button3_2.setText('一键压缩')
        self.push_button3_2.setFont(self.font_9)
        # -- 按键3_3：退出软件
        self.push_button3_3 = QPushButton(self.frame3)
        self.push_button3_3.setGeometry(220, 115, 93, 29)
        self.push_button3_3.setText('我要退出')
        self.push_button3_3.setFont(self.font_9)
        # -- 设置其它依赖转移过来
        self.menubar.setParent(self.frame3)  # 设置菜单栏依赖于窗口3
        self.frame3.setVisible(True)

    def show_dialog(self):
        self.show_dialog1()

    def show_dialog1(self):
        if self.dialog2 is not None:
            self.dialog2.close()
        self.dialog1 = QDialog(self)
        self.dialog1.resize(340, 150)
        self.dialog1.setMinimumSize(340, 150)
        self.dialog1.setMaximumSize(340, 150)
        self.dialog1.setWindowIcon(QIcon('tools.png'))
        self.dialog1.setWindowTitle('自定义拼接')
        self.dialog1.setFont(self.font_8)

        # -- 设置标签1---
        label1 = QLabel(self.dialog1)
        label1.setGeometry(40, 10, 70, 29)
        label1.setText('单列拼接')
        label1.setAlignment(Qt.AlignCenter)
        # -- 设置按键2 ---
        push_button2 = QPushButton(self.dialog1)
        push_button2.setGeometry(40, 70, 70, 29)
        push_button2.setText('矩阵拼接')
        push_button2.clicked.connect(self.show_dialog2)

        # -- 标签2：拼接数量
        label2 = QLabel(self.dialog1)
        label2.setText('拼接数量')
        label2.setGeometry(150, 20, 51, 20)

        # -- 输入框：单列拼接数量
        self.dialog_line_edit1 = QLineEdit(self.dialog1)
        self.dialog_line_edit1.setGeometry(210, 20, 30, 20)
        self.dialog_push_button1 = QPushButton(self.dialog1)
        self.dialog_push_button1.setGeometry(150, 60, 93, 25)
        self.dialog_push_button1.setText('开始单列拼接')

    def show_dialog2(self):
        if self.dialog1 is not None:
            self.dialog1.close()  # 关闭会话1
        self.dialog2 = QDialog(self)
        self.dialog2.resize(340, 150)
        self.dialog2.setFont(self.font_8)
        self.dialog2.setMinimumSize(340, 150)
        self.dialog2.setMaximumSize(340, 150)
        self.dialog2.setWindowIcon(QIcon('tools.png'))
        self.dialog2.setWindowTitle('矩阵拼接')
        # -- 设置按键1---
        push_button1 = QPushButton(self.dialog2)
        push_button1.setGeometry(40, 10, 70, 29)
        push_button1.setText('单列拼接')
        push_button1.clicked.connect(self.show_dialog1)

        # -- 设置标签2---
        label1 = QLabel(self.dialog2)
        label1.setGeometry(40, 70, 70, 29)
        label1.setText('矩阵拼接')
        label1.setAlignment(Qt.AlignCenter)

        # -- 标签2：拼接列数
        label2 = QLabel(self.dialog2)
        label2.setText('拼接行数')
        label2.setGeometry(160, 20, 51, 20)
        # -- 标签3：拼接行数
        label3 = QLabel(self.dialog2)
        label3.setText('拼接列数')
        label3.setGeometry(160, 45, 51, 20)
        # -- 标签4：拼接行数
        label4 = QLabel(self.dialog2)
        label4.setText('拼接间隙')
        label4.setGeometry(160, 70, 51, 20)

        # -- 标签5：行数
        label4 = QLabel(self.dialog2)
        label4.setText('行')
        label4.setGeometry(260, 20, 41, 20)

        # -- 标签6：列数
        label4 = QLabel(self.dialog2)
        label4.setText('列')
        label4.setGeometry(260, 50, 41, 20)

        # -- 标签7：px像素
        label4 = QLabel(self.dialog2)
        label4.setText('px')
        label4.setGeometry(260, 70, 41, 20)

        # -- 输入框：拼接列数
        self.dialog_line_edit2 = QLineEdit(self.dialog2)
        self.dialog_line_edit2.setGeometry(220, 20, 30, 20)
        # -- 输入框：拼接行数
        self.dialog_line_edit3 = QLineEdit(self.dialog2)
        self.dialog_line_edit3.setGeometry(220, 45, 30, 20)
        # -- 输入框：拼接间隙
        self.dialog_line_edit4 = QLineEdit(self.dialog2)
        self.dialog_line_edit4.setGeometry(220, 70, 30, 20)

        self.dialog_push_button2 = QPushButton(self.dialog2)
        self.dialog_push_button2.setGeometry(160, 100, 93, 25)
        self.dialog_push_button2.setText('开始矩阵拼接')

    def notice_dialog(self):
        dialog = QDialog(self)
        dialog.resize(500, 450)
        dialog.setMinimumSize(340, 150)
        text = """\
<b>使用说明</b>：
主要功能有格式转换、图片拼接，图片压缩三项<br>
<b>格式转换</b>：目前只支持pdf转png<br>
<b>图片拼接</b>：<br>
1.支持自定义拼接路径。<br>
2.默认路径是你转成png图片后的路径。<br>
3.可以设置为一键拼接成一张长图。<br>
4.自定义拼接还可以按单列拼成长图，或者按矩阵进行拼接。<br>
5.单列拼接指的是按多张图拼接成一张图，比如15张图，<br>
  可以按5张图拼成一张长图，这样就获得了3张长图。<br>
6.矩阵拼接类似微信的九宫格，比如3行三列为一张长图，<br>
  中间可以设置10像素的间隙，然后可以获得多张这样的长图。<br>
7.矩阵拼接兼容单列拼接，即列为1，间隙为0时即为矩阵拼接。<br>
<b>图片压缩</b>：<br>
1.关于宽度<br>
  普通模式即自动压缩成1M以内，<br>
  720p和1080p则自动压缩图片为这个宽度<br>
2.关于格式<br>
  即压缩后图片的格式是jpg还是png<br>
3.关于压缩比<br>
  即压缩成jpg格式时，图片的质量百分比。
        """
        dialog.setWindowTitle('使用说明')
        label = QLabel(text, dialog)
        label.setFont(self.font_9)
        dialog.show()

    def update_dialog(self):
        """
        更新记录
        """
        dialog = QDialog(self)
        dialog.resize(500, 450)
        dialog.setMinimumSize(340, 150)
        text = """\
<b>V1.1版更新记录：</b><br>
1.增加窗口抽屉功能,将图片转换、图片拼接、图片压缩功能拆分。<br>
2.增加更多自定义功能,可以自定义图片文件夹来源,<br>
还可以自定义拼接方式了。<br>
3.优化了压缩图片算法的一个小bug,增加了压缩图片的最终格式自定义，<br>
可以选择压缩为jpg或者png。<br>
4.自定义拼接中，单列拼接与矩阵拼接多了一个翻转的过度动画。<br>
5.加入操作历史记录保留，自动保留上次的操作的方式<br>
注意，只会保留你的最后一次转图片、拼接图片、压缩图片的记录，<br>
选择文件的记录不在此列<br>
6.导出路径更改为与原pdf路径同级<br>
7.导出图片时自动删除上次导出的图片<br>
7.其他更新请阅读使用说明<br>
<br>
<b>V1.0版更新记录：</b><br>
1.使用PyQt5重构了界面<br>
2.增加了进度条，减少等待时间<br>
3.选择pdf文件时，默认上次的路径<br>
4.增加了二次确认操作<br>
5.使用多线程，提高了软件速度<br>
6.美化了GUI，变得好看了<br>
        """

        dialog.setWindowTitle('更新记录')
        label = QLabel(text, dialog)
        label.setFont(self.font_9)
        dialog.show()

    def feedback_dialog(self):
        """
        我要反馈
        """
        dialog = QDialog(self)
        dialog.resize(500, 50)
        dialog.setMinimumSize(340, 150)
        text = """\
qq群：<b>974759263</b><br>
        """

        dialog.setWindowTitle('我要反馈')
        label = QLabel(text, dialog)
        label.setFont(self.font_9)
        dialog.show()

    def about_dialog(self):
        dialog = QDialog(self)
        dialog.resize(500, 50)
        dialog.setMinimumSize(340, 150)
        text = """\
        版本号：<b>V1.1</b><br>
        编译日期：2020年6月3日<br>
                """
        dialog.setWindowTitle('关于')
        label = QLabel(text, dialog)
        label.setFont(self.font_9)
        dialog.show()

    # 公用读取字典
    @staticmethod
    def read_data_dict(key, data_path='./data.json'):
        """
        根据索引读取data.json的内容
        :param key: 索引
        :param data_path: json所在路径
        :return: data：读取到的值
        """
        with open(data_path, 'rt', encoding='utf-8') as f1:
            data_dict1 = json.load(f1)
        data = data_dict1.get(key, None)  # 没有内容则为None
        return data

    # 公用写入字典
    @staticmethod
    def write_data_dict(key, value2, data_path='./data.json'):
        """
        根据索引读取data.json的内容
        :param key: 写入键
        :return: value2：写入值
        :param data_path: json所在路径
        """
        f1 = open(data_path, 'rt', encoding='utf-8')
        data_dict1 = json.load(f1)
        f1.close()
        with open(data_path, 'wt', encoding='utf-8') as f2:
            data_dict1[key] = value2
            json.dump(data_dict1, f2)


if __name__ == '__main__':
    # 创建一个data.json文件，用于储存变量参数
    if not path.exists('data.json'):
        data_dict = {}
        with open('data.json', 'wt', encoding='utf-8') as f:
            json.dump(data_dict, f)
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())


