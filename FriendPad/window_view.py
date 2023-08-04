from PySide6.QtWidgets import QMainWindow, QToolBar, QStatusBar, QComboBox, QLineEdit, QInputDialog, QTabWidget, QMessageBox
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6 import QtGui
from PySide6.QtCore import QSize, Qt
from text_environment import TextRegion
import time
import os

class WindowView(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("FriendPad")
        self.timeouts = 3000

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.setCentralWidget(self.tabWidget)
        self.tab_array = []

        self.boldToggle = False;
        self.underlineToggle = False;
        self.italicToggle = False;

        # icon
        image = QPixmap("Icons/star-of-david-solid.svg")
        window_icon = QIcon(image)
        self.setWindowIcon(window_icon)

        # menu and menubar
        menuBar = self.menuBar()
        menuBar.size
        menuBar.setNativeMenuBar(False)

        file = menuBar.addMenu(QIcon("Icons/File-regular.svg"), "&File")
        edit = menuBar.addMenu(
            QIcon("Icons/pen-to-square-regular.svg"), "&Edit")
        about = menuBar.addMenu(
            QIcon("Icons/question-solid.svg"), "&About")

        new_file_action = file.addAction("New")
        new_file_action.triggered.connect(self.create_new_file)

        open_action = file.addAction("Open")
        open_action.triggered.connect(self.open_file)

        save_action = file.addAction("Save")
        save_action.triggered.connect(self.save_file)

        rename_action = file.addAction("Rename")
        rename_action.triggered.connect(self.rename_file)

        quit_app_action = file.addAction("Quit")
        quit_app_action.triggered.connect(self.quit_app)

        cut_action = edit.addAction("Cut")
        cut_action.triggered.connect(self.cut_highlighted)

        copy_action = edit.addAction("Copy")
        copy_action.triggered.connect(self.copy_highlighted)

        paste_action = edit.addAction("Paste")
        paste_action.triggered.connect(self.paste_highlighted)
        undo_action = edit.addAction("Undo")
        undo_action.triggered.connect(self.undo_process)
        redo_action = edit.addAction("Redo")
        redo_action.triggered.connect(self.redo_process)

        info_action = about.addAction("Info")
        info_action.triggered.connect(self.display_info)

        # end of menubar and menus

        # toolbar, QAction and QCombobox
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)

        bold_action = QAction(
            QIcon("Icons/Bold-solid.svg"), "Bold", self)
        italic_action = QAction(
            QIcon("Icons/italic-solid.svg"), "Italics", self)
        underline_action = QAction(
            QIcon("Icons/onderline-solid.svg"), "Underline", self)

        left_align_action = QAction(
            QIcon("Icons/lign-left-solid.svg"), "Left-align", self)
        center_align_action = QAction(
            QIcon("Icons/lign-center-solid.svg"), "Center-align", self)
        right_align_action = QAction(
            QIcon("Icons/lign-right-solid.svg"), "Right-align", self)
        justify_align_action = QAction(
            QIcon("Icons/lign-justify-solid.svg"), "Justify-align", self)

        bold_action.triggered.connect(self.make_bold)
        italic_action.triggered.connect(self.make_italics)
        underline_action.triggered.connect(self.make_underline)

        left_align_action.triggered.connect(self.make_left_align)
        center_align_action.triggered.connect(self.make_center_align)
        right_align_action.triggered.connect(self.make_right_align)
        justify_align_action.triggered.connect(self.make_justify_align)

        self.familyFontComboBox = QComboBox()
        self.familyFontComboBox.addItem("Serif")
        self.familyFontComboBox.addItem("Sans Serif")
        self.familyFontComboBox.addItem("Calibri(body)")
        self.familyFontComboBox.addItem("Script")
        self.familyFontComboBox.addItem("Monospaced")

        # self.textStatusComboBox = QComboBox()
        # self.textStatusComboBox.addItem("Title")
        # self.textStatusComboBox.addItem("Heading1")
        # self.textStatusComboBox.addItem("Heading2")
        # self.textStatusComboBox.addItem("SubHeading1")
        # self.textStatusComboBox.addItem("SubHeading2")
        # self.textStatusComboBox.addItem("Body1")
        # self.textStatusComboBox.addItem("Body2")

        self.fontSizeComboBox = QComboBox()
        self.fontSizeComboBox.setEditable(True)

        for num in range(2, 21, 2):  # create font selection for jcombobox
            self.fontSizeComboBox.addItem(f"{num}")

        toolbar.addAction(bold_action)
        toolbar.addAction(italic_action)
        toolbar.addAction(underline_action)

        toolbar.addSeparator()

        toolbar.addAction(left_align_action)
        toolbar.addAction(center_align_action)
        toolbar.addAction(right_align_action)
        toolbar.addAction(justify_align_action)

        toolbar.addSeparator()

        toolbar.addWidget(self.familyFontComboBox)

        toolbar.addSeparator()

        # toolbar.addWidget(self.textStatusComboBox)
        # toolbar.addSeparator()
        toolbar.addWidget(self.fontSizeComboBox)

        self.addToolBar(toolbar)
        self.setStatusBar(QStatusBar(self))

    # menu trigger reactions
    def create_new_file(self):
        file_name, ok = QInputDialog.getText(self, "Create File",
                                             "File name:", QLineEdit.Normal)

        if file_name and ok:

            widget = TextRegion(file_name)

            self.tab_array.append([widget, file_name])

            self.tabWidget.addTab(self.tab_array[-1][0], file_name)

            self.statusBar().showMessage("'" + file_name + "'" + " created", self.timeouts)

        else:
            self.statusBar().showMessage("File aborted!", self.timeouts)

    def open_file(self):
        pass

    def save_file(self):
        if len(self.tab_array) > 0:
            tab_location = self.tabWidget.currentIndex()
            tab_area_text = self.tab_array[tab_location][0].text_area
            text_data = tab_area_text.toHtml()

            directory, ok = QInputDialog.getText(self, "Save File",
                                                 "Enter directory(full path):", QLineEdit.Normal)

            if ok and directory:

                file_name = self.tab_array[tab_location][1]

                complete_path_with_file = os.path.join(
                    directory, file_name + ".txt")

                try:
                    if directory and ok:
                        with open(complete_path_with_file, 'x') as f:
                            f.write(text_data)
                        self.statusBar().showMessage("File saved!", self.timeouts)

                except FileExistsError:

                    msgBox = QMessageBox(self)
                    msgBox.setWindowModality(Qt.NonModal)
                    msgBox.setWindowTitle("Save Error")
                    msgBox.setText(
                        "File already exists!\nWould to like to override file?")
                    msgBox.setIcon(QMessageBox.Warning)
                    msgBox.setStandardButtons(
                        QMessageBox.Ok | QMessageBox.Cancel)
                    msgBox.show()

                    ret = msgBox.exec()

                    if ret == QMessageBox.Ok:
                        with open(complete_path_with_file, 'w') as f:
                            f.write(text_data)
                            self.statusBar().showMessage("File overriden!", self.timeouts)
                    else:
                        self.rename_file()

                    msgBox.close()

                except:

                    msgBox = QMessageBox(self)
                    msgBox.setWindowModality(Qt.NonModal)
                    msgBox.setWindowTitle("Save Error")
                    msgBox.setText("Invalid directory!")
                    msgBox.setIcon(QMessageBox.Warning)
                    msgBox.show()

                    ret = msgBox.exec()

                    if ret == QMessageBox.Ok:
                        msgBox.close()
                        self.save_file()

            elif ok is not True:
                self.statusBar().showMessage("File save aborted!", self.timeouts)

            else:
                msgBox = QMessageBox(self)
                msgBox.setWindowModality(Qt.NonModal)
                msgBox.setWindowTitle("Save Error")
                msgBox.setText("No directory provided")
                msgBox.setIcon(QMessageBox.Warning)
                msgBox.show()

                ret = msgBox.exec()

                if ret == QMessageBox.Ok:
                    msgBox.close()
                    self.save_file()

        else:
            self.statusBar().showMessage("No file to save", self.timeouts)

    def rename_file(self):
        if len(self.tab_array) > 0:
            new_name, ok = QInputDialog.getText(self, "Rename file",
                                                "Enter new file name", QLineEdit.Normal)
            if new_name and ok:
                self.tabWidget.setTabText(
                    self.tabWidget.currentIndex(), new_name)
                self.tab_array[self.tabWidget.currentIndex()][1] = new_name

        else:
            self.statusBar().showMessage("No file to rename", self.timeouts)

    def quit_app(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setWindowTitle("Quit App")
        msgBox.setText("Do you want to quit?")
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.show()

        ret = msgBox.exec()

        if ret == QMessageBox.Ok:
            msgBox.close()
            self.app.quit()

        else:
            self.statusBar().showMessage("Quit aborted", self.timeouts)

    def cut_highlighted(self):
        if len(self.tab_array) > 0:
            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.cut()
            self.statusBar().showMessage("Cut done", self.timeouts)

    def copy_highlighted(self):
        if len(self.tab_array) > 0:
            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.copy()
            self.statusBar().showMessage("Copied", self.timeouts)

    def paste_highlighted(self):
        if len(self.tab_array) > 0:
            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.paste()
            self.statusBar().showMessage("Pasted", self.timeouts)

    def undo_process(self):
        if len(self.tab_array) > 0:
            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.undo()
            self.statusBar().showMessage("Undone", self.timeouts)

    def redo_process(self):
        if len(self.tab_array) > 0:
            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.redo()
            self.statusBar().showMessage("Redone", self.timeouts)

    def display_info(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setWindowTitle("About")
        msgBox.setText(
            "FriendPad v1. @2023\nBrought to you by David Adeshina Arungbemi\nDAA Ltd.")
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setStandardButtons(
            QMessageBox.Ok)
        msgBox.show()

    # toolbar actions and widget trigger reaction

    def make_bold(self):
        if(len(self.tab_array) > 0):
            tab_location = self.tabWidget.currentIndex()
           
            if self.boldToggle:
                self.boldToggle = False;
            else:
                self.boldToggle = True

            boldFont = QtGui.QFont()
            boldFont.setBold(self.boldToggle)

            self.tab_array[tab_location][0].text_area.setFont(boldFont)
            self.statusBar().showMessage("Boldened", self.timeouts)

    def make_italics(self):
        if(len(self.tab_array) > 0):
            tab_location = self.tabWidget.currentIndex()
            if self.italicToggle:
                self.italicToggle = False;
            else:
                self.italicToggle = True
                
            self.tab_array[tab_location][0].text_area.setFontItalic(self.italicToggle)
            self.statusBar().showMessage("Italicized", self.timeouts)

    def make_underline(self):
        if(len(self.tab_array) > 0):
            if self.underlineToggle:
                self.underlineToggle = False
            else:
                self.underlineToggle = True

            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.setFontUnderline(self.underlineToggle)
            self.statusBar().showMessage("Underlined", self.timeouts)

    def make_left_align(self):
        if(len(self.tab_array) > 0):
            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.setAlignment(Qt.AlignLeft)
            self.statusBar().showMessage("Left Aligned", self.timeouts)

    def make_right_align(self):
        if(len(self.tab_array) > 0):
            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.setAlignment(Qt.AlignRight)
            self.statusBar().showMessage("Left Aligned", self.timeouts)
            self.statusBar().showMessage("Right Aligned", self.timeouts)

    def make_center_align(self):
        if(len(self.tab_array) > 0):
            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.setAlignment(Qt.AlignCenter)
            self.statusBar().showMessage("Left Aligned", self.timeouts)
            self.statusBar().showMessage("Center Aligned", self.timeouts)

    def make_justify_align(self):
        if(len(self.tab_array) > 0):
            tab_location = self.tabWidget.currentIndex()
            self.tab_array[tab_location][0].text_area.setAlignment(Qt.AlignJustify);
            self.statusBar().showMessage("Left Aligned", self.timeouts)
            self.statusBar().showMessage("Justified", self.timeouts)

    # QTabWidget close function for tabs

    def close_tab(self):
        msgBox = QMessageBox(self)
        msgBox.setWindowModality(Qt.NonModal)
        msgBox.setWindowTitle("File Quit")
        msgBox.setText(
            "Ensure you have saved the file first.\nPress Ok to quit file.")
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setStandardButtons(
            QMessageBox.Ok | QMessageBox.Cancel)
        msgBox.show()

        ret = msgBox.exec();

        if ret == QMessageBox.Ok:
            tab_location = self.tabWidget.currentIndex()
            self.tabWidget.removeTab(tab_location)
            del self.tab_array[tab_location]
            self.statusBar().showMessage("File closed", self.timeouts)

        else:
            self.statusBar().showMessage("File close aborted!", self.timeouts)