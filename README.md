## 环境依赖

1. python3.X
2. Pillow:主要用于拼接图片，修改图片分辨率

```python
pip install Pillow
```

3. pymupdf:用于将pdf转成图片

```python
pip install pymupdf
```

4. PyQt5：用于GUI代码编写

```python
pip install PyQt5
```

5. PyQt5-tools：GUI配套工具

```python
pip install PyQt5-tools
```

6. Pyinstaller：用于打包python到应用程序

```python
pip install pyinstaller
```

-  一键安装依赖(上面单个安装和下面一键安装都行)

```python
pip -r requirements.txt
```

## 目录结构

```shell
- main.py   主程序入口
- png.ico   windows打包用的图标
- README.md  使用说明文档
- requirements.txt  依赖记录文件
- tools.ico  Mac打包用的图标，可忽略
- tools.py   主要为pdf与图片操作的后端源代码，核心所在
- tools.png  主程序菜单栏的图标，不可删除
- ui.py  UI设计界面
```

## 软件打包

- 直接使用Pyinstaller打包主程序

```python
pyinstaller -i png.ico -F -w main.py
```

## 不算bug的bug

- 打包后的程序需要和tools.png放到一起，不然菜单栏图标会消失，后期看看怎么解决

## 其它建议

- 如果对软件有更好的建议，可以直接给我发邮件371043382@qq.com
- 如果你也是python的学习爱好者，欢迎加群一起学习：974759263
- Python个人博客，不定期更新python学习教程：https://www.vbahome.cn/

