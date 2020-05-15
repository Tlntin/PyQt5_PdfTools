from PyQt5.QtWidgets import QMainWindow, QLabel,\
    QApplication, QLineEdit, QComboBox, QPushButton, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QRect
import sys


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        self.line_edit2 = QLineEdit(self)  #
        self.label_4 = QLabel(self)
        self.com_box2 = QComboBox(self)
        self.label_3 = QLabel(self)
        self.action2 = QAction('更新记录', self)
        self.menu = self.menuBar()  # 开启菜单栏
        self.menu2 = self.menu.addMenu('&菜单')
        self.action1 = QAction('使用说明', self)  # 创建在当前界面下的动作
        self.button3 = QPushButton(self)
        self.button2 = QPushButton(self)
        self.button1 = QPushButton(self)
        self.com_box = QComboBox(self)
        self.label_2 = QLabel(self)
        self.label_1 = QLabel(self)  # label标签
        self.line_edit = None
        self.file_path = None  # 文件路径
        self.progress = None  # 进度条会话
        self.progress2 = None
        self.timer = None  # 步数
        self.check_zip = 0  # 是否压缩
        self.check_720p = 0  # 720p
        self.png_num = 2  # 拼接长图数量
        self.png_type = '普通'  # png图片质量
        self.pdf_png = None  # pdf转png
        self.gen_long = None  # 生成长图
        self.init_ui()

    def init_ui(self):
        # 设置基本页面
        self.setGeometry(300, 300, 310, 150)
        self.setMaximumSize(QSize(310, 150))  # 设定最大尺寸
        self.setMinimumSize(QSize(310, 150))   # 设置最小尺寸
        self.setLayoutDirection(Qt.LeftToRight)  # 设置从左往右
        self.setStyleSheet("font-size:12px; font-weight:normal")  #
        self.setWindowTitle('PDF转长图v1.0')
        self.setWindowIcon(QIcon('tools.png'))

        # --设置主界面--#
        # label_1
        self.label_1.setText('文件路径')
        self.label_1.setGeometry(QRect(10, 30, 50, 25))  # label布局
        # line_edit
        self.line_edit = QLineEdit(self)  #
        self.line_edit.setGeometry(QRect(70, 30, 220, 25))  # 设置绝对布局

        # label2拼接数量
        self.label_2.setGeometry(QRect(10, 60, 54, 20))
        self.label_2.setText('拼接数量')
        # 拼接数量选择
        self.com_box.setGeometry(QRect(60, 60, 35, 20))
        self.com_box.addItem('2')
        self.com_box.addItem('3')
        self.com_box.addItem('4')
        self.com_box.addItem('5')
        self.com_box.addItem('6')
        self.com_box.addItem('7')
        # label3图片宽度
        self.label_3.setGeometry(110, 60, 54, 20)
        self.label_3.setText('压缩宽度')

        # label4图片质量
        self.label_4.setGeometry(230, 60, 54, 20)
        self.label_4.setText('压缩率')

        # 图片宽度选择
        self.com_box2.setGeometry(QRect(160, 60, 55, 20))
        self.com_box2.addItem('普通')
        self.com_box2.addItem('720p')
        self.com_box2.addItem('1080p')

        # line_edit
        self.line_edit2.setGeometry(QRect(270, 60, 21, 20))  # 设置绝对布局
        self.line_edit2.setText('92')
        label5 = QLabel(self)
        label5.setGeometry(292, 60, 20, 20)
        label5.setText('%')
        # com_box.activated[str].connect(self.com_box_select)
        # 选择文件
        self.button1.setGeometry(QRect(10, 90, 81, 30))
        self.button1.setText('选择文件')
        # button1.clicked.connect(self.file_select)
        # 开始转换
        self.button2.setGeometry(QRect(112, 90, 81, 30))
        self.button2.setText('开始转换')
        # button2.clicked.connect(self.do_action)
        # 我要退出
        self.button3.setGeometry(QRect(215, 90, 81, 30))
        self.button3.setText('我要退出')
        # button3.clicked.connect(qApp.quit)
        # ---显示主界面----
        self.statusBar()  # 开启状态栏
        # 菜单下的按钮1
        # action1.triggered.connect(self.notice_dialog)  # 设定触发器
        self.menu2.addAction(self.action1)
        # 菜单下的按钮2
        # action2.triggered.connect(self.update_dialog)
        self.menu2.addAction(self.action2)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())
