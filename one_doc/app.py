import re
import os
import sys
import pandas as pd
from typing import List, Set, Dict, Tuple, Optional

#from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QLabel
#from PyQt5.QtWidgets import QAction, QTabWidget, QVBoxLayout, QTableView
#from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtSlot
#from PyQt5.QtGui import QIcon

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

def load_file(one_doc: str) -> Tuple[str, str, List]:
    
    with open(one_doc, "r") as f: file = f.read()
        
    doc = file.split("\n\n# Spreadsheet\n\n")[0].replace("# Document\n\n", "")
    tbl = file.split("\n\n# Spreadsheet\n\n")[1].split("\n\n# Slides")[0]
    slides = file.split("\n\n# Slides\n\n")[1]
    tbl_df = md_tbl_to_csv(tbl)
    slides_list = ['## ' + x for x in re.split('## ', slides)[1:]]
    slides_list = '\n'.join(slides_list)
    result = (doc, tbl_df, slides_list)
    
    return(result)

def md_tbl_to_csv(md_tbl: str) -> pd.DataFrame:
    
    remove_empty_strs = lambda row: [val.strip() for val in row if val != ""]
    
    rows_as_list = [
        remove_empty_strs(line.split("|"))
        for line in md_tbl.split("\n") 
        if "--" not in line
    ]
    
    result = pd.DataFrame(rows_as_list)
    result.columns = result.iloc[0]
    result = result[1:]
    
    return(result)

def get_tbl_data(md_tbl: str) -> str:
    
    remove_empty_strs = lambda row: [val.strip() for val in row if val != ""]
    
    rows_as_list = [
        remove_empty_strs(line.split("|"))
        for line in md_tbl.split("\n") 
        if "--" not in line
    ]
    
    result = pd.DataFrame(rows_as_list)
    result.columns = result.iloc[0]
    result = result[1:]
    
    return(result)
       
'''
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "One Doc"
        self.left = 0
        self.top = 0
        self.width = 1024
        self.height = 768
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()
'''

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.title = "One Doc"
        self.left = 0
        self.top = 0
        self.width = 1024
        self.height = 768
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #self.table_widget = MyTableWidget(self)
        #ex.table_widget.l1.setText(doc)
        #ex.table_widget.l2.setModel(pandasModel(tbl))
        #ex.table_widget.l3.setText(slides[0])
        #    doc, tbl, slides = load_file("1doc.md")

        layout = QVBoxLayout()

        self.editor = MyTableWidget(self) #QPlainTextEdit()  # Could also use a QTextEdit and set self.editor.l1.setAcceptRichText(False)
        # Setup the QTextEdit editor configuration
        #fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        #fixedfont.setPointSize(12)
        #self.editor.l1.setFont(fixedfont)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(QIcon(os.path.join('images', 'arrow-curve-180-left.png')), "Undo", self)
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.l1.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction(QIcon(os.path.join('images', 'arrow-curve.png')), "Redo", self)
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.l1.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join('images', 'scissors.png')), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.l1.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(QIcon(os.path.join('images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.l1.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join('images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.l1.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join('images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.l1.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join('images', 'arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        self.update_title()
        self.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")

        if path:
            try:
                text = load_file(path)

            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.editor.l1.setPlainText(text[0])
                self.editor.l2.setModel(pandasModel(text[1]))
                self.editor.l3.setPlainText(text[2])
                self.update_title()

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        text = "# Document\n\n" + self.editor.l1.toPlainText() + \
               #"\n\n# Spreadsheet\n\n" +  self.editor.l2.toPlainText() + \
               "\n\n# Slides\n\n" +  self.editor.l3.toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.l1.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - No2Pads" % (os.path.basename(self.path) if self.path else "Untitled"))

    def edit_toggle_wrap(self):
        self.editor.l1.setLineWrapMode( 1 if self.editor.l1.lineWrapMode() == 0 else 0 )
    
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)
        
        # Add tabs
        self.tabs.addTab(self.tab1, "Doc")
        self.tabs.addTab(self.tab2, "Sheet")
        self.tabs.addTab(self.tab3, "Slides")
        
        # Tab 1
        self.tab1.layout = QVBoxLayout(self)
        self.l1 = QPlainTextEdit()
        self.tab1.layout.addWidget(self.l1)
        self.tab1.setLayout(self.tab1.layout)
        
        # Tab 2
        self.tab2.layout = QVBoxLayout(self)
        self.l2 = QTableView()
        self.tab2.layout.addWidget(self.l2)
        self.tab2.setLayout(self.tab2.layout)
        
         # Tab 3
        self.tab3.layout = QVBoxLayout(self)
        self.l3 = QPlainTextEdit()
        self.tab3.layout.addWidget(self.l3)
        self.tab3.setLayout(self.tab3.layout)
        
        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent = None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_()) 
    
    
    
