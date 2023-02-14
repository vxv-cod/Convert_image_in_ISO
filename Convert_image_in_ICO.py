'''Программа предназначена для конвертации изображения в файлы формата "ico".
Данный формат позволяет из файлов "png" с прозрачным фоном делать кнопки для NanoCada'''

import os
import sys
import threading
from PIL import Image
from PyQt5 import QtCore, QtWidgets
from okno_ui import Ui_Form

app = QtWidgets.QApplication(sys.argv)
Form = QtWidgets.QWidget()
ui = Ui_Form()
ui.setupUi(Form)
Form.show()

def on_change_err(s):
    '''Сообщение об ошибке'''
    QtWidgets.QMessageBox.information(Form, 'Ошибка !!!', s)


'''Отслеживаем сигнал в plainTextEdit на изменение данных и удаляем не нужный текст'''
def ChangedPT(plainTextEdit):
    '''Удаления ненужного текста в plainTextEdit'''
    directory = plainTextEdit.toPlainText()
    if "file:///" in directory:
        xxx = directory.rfind("file:///")
        directory = directory[xxx + 8:]
        try:
            directory = directory.replace("/", "\\")
        except:
            pass
        plainTextEdit.setPlainText(rf"{directory}")
ui.plainTextEdit.textChanged.connect(lambda : ChangedPT(ui.plainTextEdit))


def handle_updateRequest(rect=QtCore.QRect(), dy=0):
    '''Изменение высоты plainTextEdit и окна'''
    for widgetX in widgetList:
        doc = widgetX.document()
        tb = doc.findBlockByNumber(doc.blockCount() - 1)
        h = widgetX.blockBoundingGeometry(tb).bottom() + 2 * doc.documentMargin()
        widgetX.setFixedHeight(h)
    '''Корректируем высоту формы'''
    Form.resize(Form.minimumWidth(), Form.minimumHeight())

widgetList = [ui.plainTextEdit]
for widget in widgetList:
    widget.updateRequest.connect(handle_updateRequest)


def thread(my_func):
    '''Обертка функции в потопк (декоратор)'''
    def wrapper():
        threading.Thread(target=my_func, daemon=True).start()
    return wrapper


def GO():
    Fullfilename = ui.plainTextEdit.toPlainText()
    if Fullfilename == '':
        on_change_err('Не указан файл с картинкой')
        return
    '''Разделить путь на имя файла и его расширение'''
    failnamesave = os.path.splitext(Fullfilename)[0] + '.ico'

    try:
        img = Image.open(Fullfilename)
    except:
        on_change_err('По указанному пути картинки файл не найден')
        return
    if ui.comboBox.currentIndex() == 0:
        img.save(failnamesave,format = 'ICO', sizes=[(128, 128)])
    if ui.comboBox.currentIndex() == 1:
        img.save(failnamesave,format = 'ICO', sizes=[(64, 64)])
    if ui.comboBox.currentIndex() == 2:
        img.save(failnamesave,format = 'ICO', sizes=[(48, 48)])
    if ui.comboBox.currentIndex() == 3:
        img.save(failnamesave,format = 'ICO', sizes=[(32, 32)])
    if ui.comboBox.currentIndex() == 4:
        img.save(failnamesave,format = 'ICO', sizes=[(16, 16)])

'''Чистим "plainTextEdit" для отображения текста по умолчанию'''
ui.plainTextEdit.clear()

@thread
def start():
    try:
        GO()
    except:
        pass


ui.pushButton.clicked.connect(GO)
if __name__ == "__main__":
    sys.exit(app.exec_())