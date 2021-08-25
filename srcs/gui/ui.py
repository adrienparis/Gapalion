#!/usr/bin/env python
# -- coding: utf-8 --

'''Interface for Gapalion'''

__author__      = "Adrien PARIS"
__email__       = "a.paris.cs@gmail.com"

import sys
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *

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


class MyWindow( QMainWindow ):
    
    def __init__ ( self ) :
        QMainWindow.__init__( self )
        self.setWindowTitle( 'First steps With PySide2 and Python3' )
        self.setWindowIcon( QIcon('icon.png') )
        self.resize(400, 300)

        self.__button1 = QPushButton( "First button", self )
        self.__button1.setGeometry(10, 10, 200, 35)
    
        self.__button2 = QPushButton( "Second button", self )
        self.__button2.setGeometry(20, 50, 200, 35)
        self.__buttonPlop = QPushButton( "third button", self )
        self.__buttonPlop.setGeometry(30, 90, 200, 35)
        img = r"D:\creative seed\script\verificator\images\eye.png"
        img_path = "D:\\creative seed\\script\\Gapalion\\img\\"
        
        w = MainTabWidget()
        w.addTab(QWidget(),QIcon(img_path + "User.png"), "Utilisateurs") # gérer les utilisateurs, leurs logins, et adresses mails
        w.addTab(QWidget(),QIcon(img_path + "Project.png"), "Projets") # nom du projet, chemins, + examens à faire passer et thèmes à appliquer
        w.addTab(QWidget(),QIcon(img_path + "Mail.png"), "Mail") # Gestion des examen à faire passer au mail reçu en fonction de l'objet du mail
        w.addTab(QWidget(),QIcon(img_path + "Exam.png"), "éxamens") # Creation d'examens comportent plusieur épreuves. Et assignement de quelles épreuves pour quelle fichier (ex: asset/*/rig/*.ma)
        w.addTab(QWidget(),QIcon(img_path + "Trial.png"), "épreuves") # Créations d'épreuves en fonctions des soft et des tags de selection ou listage des tests
        w.addTab(QWidget(),QIcon(img_path + ".png"), "Programation") # Quand executer le script
        w.addTab(QWidget(),QIcon(img_path + ".png"), "Thèmes") # gestion des thèmes
        w.addTab(QWidget(),QIcon(img_path + ".png"), "Paramètre") # ? gestion du thème de l'interface? definition du chemin du dossier resources? definition du mayapy?
        self.__tab = w
        self.__tab.setGeometry(10, 140, 800, 800)
        self.__tab.show()
        

if __name__ == "__main__" :
    app = QApplication( sys.argv )

    myWindow = MyWindow()
    myWindow.show()
    
    sys.exit( app.exec_() )