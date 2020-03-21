#!usr/bin/env python3
#
#
# todo: make popup send game ID to metadata
# todo: add suggested player count
# todo: make image scale


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QGridLayout
import boardgamegeek
from urllib.request import urlopen
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 470)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 10, 261, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(240, 40, 341, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(self.enter)
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(450, 90, 300, 300))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setText("")
        self.imageLabel.setPixmap(QtGui.QPixmap(
            "./no-image.png"))
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setObjectName("imageLabel")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 140, 321, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 170, 321, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(50, 200, 321, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(50, 230, 321, 16))
        self.label_6.setObjectName("label_6")
        self.label_65 = QtWidgets.QLabel(self.centralwidget)
        self.label_65.setGeometry(QtCore.QRect(50, 260, 321, 16))
        self.label_65.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(50, 290, 321, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(50, 320, 321, 16))
        self.label_8.setObjectName("label_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate(
            "MainWindow", "Enter Game Name or Search Query"))
        self.label_3.setText(_translate("MainWindow", "Name: "))
        self.label_4.setText(_translate("MainWindow", "BGG Rank: "))
        self.label_5.setText(_translate("MainWindow", "Average Rating: "))
        self.label_6.setText(_translate("MainWindow", "Rated Weight: "))
        self.label_65.setText(_translate("MainWindow", "Play Time: "))
        self.label_7.setText(_translate("MainWindow", "Player Count: "))
        self.label_8.setText(_translate("MainWindow", "Best Player Count: "))

    def enter(self):
        self.query = self.lineEdit.text()
        self.idcheck = self.search(self.query)
        try:
            self.g.id
            self.metadata = self.lookup(self.idcheck)
        except:
            pass

    def search(self, z):
        try:
            self.bgg = boardgamegeek.BGGClient()
            self.g = self.bgg.game(z)
            return(self.g.id)
        except:
            self.bgg = boardgamegeek.BGGClient()
            self.search = self.bgg.search(z)
            self.g = self.popup(self.search)

    def popup(self, searchItem):
        self.exPopup = searchPopup(searchItem)
        self.exPopup.show()

    def lookup(self, y):
        self.bgg = boardgamegeek.BGGClient()
        self.g = self.bgg.game(game_id=y)
        self.lineEdit.setText('')
        self.label_3.setText(f"{self.g.name} ({self.g.year})")
        self.label_4.setText(f"BGG Rank: {self.g.bgg_rank}")
        self.label_5.setText(
            f"Average Rating: {round(self.g.rating_average,2)}")
        self.label_6.setText(
            f"Rated Weight: {round(self.g.rating_average_weight, 2)}/5")
        if self.g.min_playing_time != self.g.max_playing_time:
            self.label_65.setText(
                f"Play Time: {self.g.min_playing_time} - {self.g.max_playing_time} Minutes")
        else:
            self.label_65.setText(
                f"Play Time: {self.g.min_playing_time} Minutes")
        if self.g.min_players != self.g.max_players:
            self.label_7.setText(
                f"Player Count: {self.g.min_players} - {self.g.max_players}")
        else:
            self.label_7.setText(f"Player Count: {self.g.min_players}")
        # self.label_8.setText(f"Best Player Count: {self.g.PlayerSuggestion()}")

        self.imageData = urlopen(self.g.image).read()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self.imageData)
        self.imageLabel.setPixmap(QtGui.QPixmap(pixmap))

        # players = g.player_suggestions
        # for x in players:
        #     print(boardgamegeek.utils.DictObject.data(x))


class searchPopup(QWidget):
    def __init__(self, results):
        super().__init__()

        self.results = results

        QWidget.__init__(self)
        layout = QGridLayout()
        self.setLayout(layout)
        self.listwidget = QListWidget()
        index = 0
        for x in results:
            self.listwidget.insertItem(index, (f"{x.name} ({x.year})"))
            # self.listwidget.insertItem(index, x.name)
            index += 1
        self.listwidget.clicked.connect(self.clicked)
        layout.addWidget(self.listwidget)

    def clicked(self, qmodelindex):
        self.item = self.listwidget.currentItem()
        print(self.item.text())
        self.row = self.listwidget.currentRow()
        self.selection = self.results[self.row]
        print(self.selection.id)
        self.hide()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
