#!/usr/bin/env python
# -- coding: utf-8 --

'''Interface for Gapalion'''
import sys
# from PySide6.QtWidgets import QApplication, QWidget, QDialog, QLineEdit, QPushButton, QTabBar, QTabWidget
# from PySide6.QtGui import QIcon, QStylePainter, QStyleOptionTab
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

class ParameterForm(QWidget):
    def __init__(self, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.line_edit.textChanged.connect(self.line_edit_text_changed)

        self.show()

    def line_edit_text_changed(self, text):
        self.label.setText(text)


class TabBar(QTabBar):
    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        # print(s)
        s.setHeight(100)
        s.setWidth(100)
        # s.transpose()
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()

class MainTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QTabWidget.West)

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Gapalion")
        img_path = "D:\\creative seed\\script\\Gapalion\\img\\"

        w = MainTabWidget(self)
        w.addTab(QWidget(),QIcon(img_path + "User.png"), "Utilisateurs") # gérer les utilisateurs, leurs logins, et adresses mails
        w.addTab(QWidget(),QIcon(img_path + "Project.png"), "Projets") # nom du projet, chemins, + examens à faire passer et thèmes à appliquer
        w.addTab(QWidget(),QIcon(img_path + "Mail.png"), "Mail") # Gestion des examen à faire passer au mail reçu en fonction de l'objet du mail
        w.addTab(QWidget(),QIcon(img_path + "Exam.png"), "éxamens") # Creation d'examens comportent plusieur épreuves. Et assignement de quelles épreuves pour quelle fichier (ex: asset/*/rig/*.ma)
        w.addTab(QWidget(),QIcon(img_path + "Trial.png"), "épreuves") # Créations d'épreuves en fonctions des soft et des tags de selection ou listage des tests
        w.addTab(QWidget(),QIcon(img_path + ".png"), "Programation") # Quand executer le script
        w.addTab(QWidget(),QIcon(img_path + ".png"), "Thèmes") # gestion des thèmes
        w.addTab(ParameterForm(),QIcon(img_path + ".png"), "Paramètre") # ? gestion du thème de l'interface? definition du chemin du dossier resources? definition du mayapy?
        

def show():
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())


if __name__ == "__main__":
    show()