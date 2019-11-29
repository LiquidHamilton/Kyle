#!/usr/bin/env python3
# My Home Library
# Version 1.1.0
# 2019, Kyle Carroll
#
# todo: resize table when main window resized
# todo: left/right click options for listWidget
# todo: create widgets for remiaining buttons
# todo: make generic 'no image' show up when GR has no result
# todo: find a way to get hi-res GR covers
# todo: in settings, display columns, backup/restore database
# todo: create csv import
# todo: create config file for saveing state of columns and preferences
# todo: make search bar work
# todo: refresh table on booksearch Add
# todo: fix deleting rows (currently deletes all rows?)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtSql
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMessageBox, QLabel, QPushButton, QApplication, QMainWindow, QTableView, QAbstractItemView, QWidget
from urllib.request import urlopen
import xml.etree.ElementTree as ET
import re
import sys
import os
import datetime
from playsound import playsound


class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 740)
        MainWindow.setFixedSize(MainWindow.size())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.createConnection()
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(10, 40, 221, 341))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.addItem("Library")
        self.listWidget.addItem("Owned")
        self.listWidget.addItem("Wishlist")
        self.listWidget.addItem("On Loan")
        self.pushButton03 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton03.setGeometry(QtCore.QRect(225, 5, 113, 31))
        self.pushButton03.setObjectName("pushButton03")
        self.pushButton04 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton04.setGeometry(QtCore.QRect(335, 5, 113, 31))
        self.pushButton04.setObjectName("pushButton04")
        self.pushButton04.clicked.connect(self.removeClicked)
        self.pushButton05 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton05.setGeometry(QtCore.QRect(445, 5, 113, 31))
        self.pushButton05.setObjectName("pushButton05")
        self.pushButton06 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton06.setGeometry(QtCore.QRect(555, 5, 113, 31))
        self.pushButton06.setObjectName("pushButton06")
        self.pushButton07 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton07.setGeometry(QtCore.QRect(665, 5, 113, 31))
        self.pushButton07.setObjectName("pushButton07")
        self.pushButton07.clicked.connect(self.settingsClicked)
        self.imageBox = QtWidgets.QLabel(self.centralwidget)
        self.imageBox.setGeometry(QtCore.QRect(10, 390, 221, 291))
        self.imageBox.setText("")
        self.imageBox.setPixmap(QtGui.QPixmap("./no-image.png"))
        self.imageBox.setScaledContents(True)
        self.imageBox.setObjectName("imageBox")
        self.pushButton01 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton01.setGeometry(QtCore.QRect(5, 5, 113, 31))
        self.pushButton01.setObjectName("pushButton01")
        self.pushButton01.clicked.connect(self.openSearch)
        self.pushButton02 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton02.setGeometry(QtCore.QRect(115, 5, 113, 31))
        self.pushButton02.setObjectName("pushButton02")
        self.summaryBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.summaryBox.setGeometry(QtCore.QRect(650, 530, 421, 171))
        self.summaryBox.setObjectName("summaryBox")
        self.summaryBox.setReadOnly(True)
        self.summaryBox.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.summaryBox.viewport().setCursor(QCursor(QtCore.Qt.ArrowCursor))
        self.searchBar = QtWidgets.QTextEdit(self.centralwidget)
        self.searchBar.setGeometry(QtCore.QRect(850, 10, 220, 20))
        self.searchBar.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.searchBar.setObjectName("searchBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 540, 401, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(240, 560, 401, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(240, 580, 401, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(240, 600, 401, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(240, 620, 401, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(240, 640, 401, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(240, 660, 401, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(240, 680, 401, 16))
        self.label_8.setObjectName("label_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1080, 22))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusLabel = QtWidgets.QLabel(self.centralwidget)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statusbar.addWidget(self.statusLabel, 1)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My Home Library"))
        self.pushButton03.setText(_translate("MainWindow", "Edit Book"))
        self.pushButton04.setText(_translate("MainWindow", "Delete Book"))
        self.pushButton05.setText(_translate("MainWindow", "Loan/Return"))
        self.pushButton06.setText(_translate("MainWindow", "Statistics"))
        self.pushButton07.setText(_translate("MainWindow", "Settings"))
        self.pushButton01.setText(_translate("MainWindow", "Book Lookup"))
        self.pushButton02.setText(_translate("MainWindow", "Manual Add"))
        self.statusLabel.setText(_translate(
            "MainWindow", "0 Books | 0 On Loan"))
        self.searchBar.setText(_translate("MainWindow", ""))
        self.label.setText(_translate("MainWindow", "Title: "))
        self.label_2.setText(_translate("MainWindow", "Series: "))
        self.label_3.setText(_translate("MainWindow", "Author: "))
        self.label_4.setText(_translate("MainWindow", "Publisher: "))
        self.label_5.setText(_translate(
            "MainWindow", "Original Publish Year: "))
        self.label_6.setText(_translate("MainWindow", "Pages: "))
        self.label_7.setText(_translate("MainWindow", "ISBN: "))
        self.label_8.setText(_translate("MainWindow", "On Loan To: "))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def createConnection(self):
        if not os.path.exists('./test.db'):
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("test.db")
            db.open()
            if not db.open():
                print("Cannot establish a database connection")
                return False
            self.fillTable()
            self.createModel()
            self.initUI()
        else:
            db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("test.db")
            db.open()
            if not db.open():
                print("Cannot establish a database connection")
                return False
            self.createModel()
            self.initUI()

    def fillTable(self):
        q = QtSql.QSqlQuery()

        q.exec_("DROP TABLE IF EXISTS Books;")
        q.exec_(
            "CREATE TABLE Books (Title TEXT, Author TEXT, Series TEXT, Year INT, Publisher TEXT, Pages INT, Isbn TEXT, Summary TEXT, Owned BOOL, Rating INT, tbr BOOL, addeddate DATE, readdate DATE, readcount INT );")
        q.exec_(
            "INSERT INTO Books VALUES ('The Final Empire', 'Brandon Sanderson', 'Mistborn [1]', 2006, 'TEST', 234, 'ISBNNO', 'Summary', 1, 0, 0, NULL, NULL, NULL);")

    def createModel(self):
        self.model = QtSql.QSqlTableModel()
        self.model.setTable("Books")
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "Title")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Author")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Series")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Year")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "Publisher")
        self.model.setHeaderData(5, QtCore.Qt.Horizontal, "Page Count")
        self.model.setHeaderData(6, QtCore.Qt.Horizontal, "ISBN")
        self.model.setHeaderData(7, QtCore.Qt.Horizontal, "Summary")
        self.model.setHeaderData(8, QtCore.Qt.Horizontal, "Owned")
        self.model.setHeaderData(9, QtCore.Qt.Horizontal, "Rating")
        self.model.setHeaderData(10, QtCore.Qt.Horizontal, "TBR")
        self.model.setHeaderData(11, QtCore.Qt.Horizontal, "Date Added")
        self.model.setHeaderData(12, QtCore.Qt.Horizontal, "Last Read")
        self.model.setHeaderData(13, QtCore.Qt.Horizontal, "Read Count")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model.select()

    def initUI(self):
        self.tableView.setModel(self.model)
        self.tableView.setGeometry(QtCore.QRect(240, 40, 831, 481))
        self.tableView.setObjectName("tableView")
        self.tableView.setSortingEnabled(True)
        self.tableView.setDropIndicatorShown(True)
        self.tableView.setSelectionBehavior(self.tableView.SelectRows)
        self.tableView.setSelectionMode(self.tableView.SingleSelection)
        self.tableView.horizontalHeader().setSectionsMovable(True)

        # self.tableView.setColumnHidden(1, True)

    def settingsClicked(self):
        self.model.submit()
        self.model.select()

    def removeClicked(self):
        self.model.removeRow(self.tableView.currentIndex().row())
        self.model.submit()
        self.model.select()

    def openSearch(self):
        self.booksearch = QtWidgets.QMainWindow()
        self.ui = bookSearch(MainWindow)
        self.ui.setupUi(self.booksearch)
        self.booksearch.show()

    def aboutPopup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('About')
        msg.setText("""
        My Home Library
        Created by Kyle Carroll
        kyle.carroll@icloud.com
        Copyright 2019
        Version 1.1.0""")
        x = msg.exec_()

    def closeEvent(self, e):
        if (self.db.open()):
            self.db.close()


class bookSearch(QMainWindow):
    def __init__(self, parent):
        super(bookSearch, self).__init__(parent)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 500)
        MainWindow.setFixedSize(MainWindow.size())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(40, 80, 421, 16))
        self.titleLabel.setObjectName("titleLabel")
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(490, 80, 271, 371))
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
        self.seriesLabel = QtWidgets.QLabel(self.centralwidget)
        self.seriesLabel.setGeometry(QtCore.QRect(40, 100, 421, 16))
        self.seriesLabel.setObjectName("seriesLabel")
        self.authorLabel = QtWidgets.QLabel(self.centralwidget)
        self.authorLabel.setGeometry(QtCore.QRect(40, 120, 421, 16))
        self.authorLabel.setObjectName("authorLabel")
        self.yearLabel = QtWidgets.QLabel(self.centralwidget)
        self.yearLabel.setGeometry(QtCore.QRect(40, 160, 421, 16))
        self.yearLabel.setObjectName("yearLabel")
        self.publisherLabel = QtWidgets.QLabel(self.centralwidget)
        self.publisherLabel.setGeometry(QtCore.QRect(40, 140, 421, 16))
        self.publisherLabel.setObjectName("publisherLabel")
        self.pagesLabel = QtWidgets.QLabel(self.centralwidget)
        self.pagesLabel.setGeometry(QtCore.QRect(40, 180, 421, 16))
        self.pagesLabel.setObjectName("pagesLabel")
        self.summaryLabel = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.summaryLabel.setGeometry(QtCore.QRect(40, 230, 421, 220))
        self.summaryLabel.setObjectName("summaryLabel")
        self.summaryLabel.setReadOnly(True)
        self.ISBNLabel = QtWidgets.QLabel(self.centralwidget)
        self.ISBNLabel.setGeometry(QtCore.QRect(40, 200, 421, 16))
        self.ISBNLabel.setObjectName("ISBNLabel")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(180, 30, 171, 25))
        self.label_10.setObjectName("label_10")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(360, 30, 241, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.returnPressed.connect(self.enter)
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(650, 30, 110, 25))
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.addClicked)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Book Lookup"))
        self.titleLabel.setText(_translate("MainWindow", "Title: "))
        self.seriesLabel.setText(_translate("MainWindow", "Series: "))
        self.authorLabel.setText(_translate("MainWindow", "Author: "))
        self.yearLabel.setText(_translate(
            "MainWindow", "Original Publish Year: "))
        self.publisherLabel.setText(_translate("MainWindow", "Publisher: "))
        self.pagesLabel.setText(_translate("MainWindow", "Page Count: "))
        self.summaryLabel.setPlainText(
            _translate("MainWindow", ""))
        self.ISBNLabel.setText(_translate("MainWindow", "ISBN: "))
        self.addButton.setText(_translate("MainWindow", "Add to Library"))
        self.label_10.setText(_translate(
            "MainWindow", "Enter ISBN or Search Query"))

    def enter(self):
        self.lineEditText = self.lineEdit.text()
        self.query = self.urlSafe(self.lineEditText)
        self.metadataURL = self.getQuery(self.query)
        if self.metadataURL == None:
            self.lineEdit.setText("")
            return
        else:
            self.metadataDict = self.getMetadata(self.metadataURL)
            self.prettyPrint(self.metadataDict)

    def urlSafe(self, x):
        self.query = re.sub(r"'", '%27', x)
        self.query = re.sub(r'!', '%21', self.query)
        self.query = re.sub(r'&', '%26', self.query)
        self.query = re.sub(r"#", '%23', self.query)
        self.query = re.sub(r"\s+", '+', self.query)
        # self.query = re.sub(r"?", "%3F", self.query)
        return self.query

    def getQuery(self, y):
        noResult = False
        queryURL = urlopen(
            f'https://www.goodreads.com/search.xml?key=hrMPgTDm40OGEaq5tLNw7Q&q={y}')
        tree = ET.parse(queryURL)
        root = tree.getroot()
        for result in root.findall('./search/total-results'):
            if result.text == '0':
                self.popup()
                noResult = True
            else:
                for book in root.findall('./search/results/work/best_book/id'):
                    bookID = (book.text)
                    break
        if noResult == True:
            self.metadataURL = None
            return self.metadataURL
        else:
            self.metadataURL = urlopen(
                f'https://www.goodreads.com/book/show/{bookID}?format=xml&key=hrMPgTDm40OGEaq5tLNw7Q')
            return self.metadataURL

    def getMetadata(self, z):
        tree2 = ET.parse(z)
        root2 = tree2.getroot()
        author = []
        title = None
        coverImageURL = None
        year = None
        month = None
        pages = None
        summary = None
        seriesTitle = None
        seriesIndex = None
        isbn = None
        publisher = None
        series = None

        for t in root2.findall('./book/title'):
            title = t.text
        for a in root2.findall('./book/authors/author/name'):
            author.append(a.text)
        for i in root2.findall('./book/image_url'):
            coverImageURL = i.text
        for y in root2.findall('./book/work/original_publication_year'):
            year = y.text
        for m in root2.findall('./book/work/original_publication_month'):
            month = m.text
        for p in root2.findall('./book/num_pages'):
            pages = p.text
        for d in root2.findall('./book/description'):
            rawSummary = d.text
            if rawSummary != None:
                cleanr = re.compile('<.*?>')
                summary = re.sub(cleanr, ' ', rawSummary)
            else:
                summary = rawSummary
        for s in root2.findall('./book/series_works/series_work/series/title'):
            seriesTitle = s.text
            seriesTitle = seriesTitle.strip()
            break
        for x in root2.findall('./book/series_works/series_work/user_position'):
            seriesIndex = x.text
            break
        for n in root2.findall('./book/isbn13'):
            isbn = n.text
        for u in root2.findall('./book/publisher'):
            publisher = u.text
        if seriesTitle != None and seriesIndex != None:
            series = f'{seriesTitle} [{seriesIndex}]'
        elif seriesTitle != None and seriesIndex == None:
            series = seriesTitle

        openLibraryCoverURL = f'http://covers.openlibrary.org/b/isbn/{isbn}-L.jpg'
        openLibraryCoverData = urlopen(openLibraryCoverURL).read()
        goodreadsCoverData = urlopen(coverImageURL).read()

        if sys.getsizeof(openLibraryCoverData) > 1000:
            self.imageData = openLibraryCoverData
        else:
            self.imageData = goodreadsCoverData

        self.metadataDict = {
            'title': title,
            'author': ', '.join(author),
            'summary': summary,
            'pages': (pages),
            'coverImageURL': coverImageURL,
            'year': (year),
            'month': (month),
            'series': series,
            'isbn': isbn,
            'publisher': publisher,
        }
        return self.metadataDict

    def prettyPrint(self, inDict):
        self.lineEdit.setText('')
        self.titleLabel.setText(f'Title: {inDict["title"]}')
        self.seriesLabel.setText(f'Series: {inDict["series"]}')
        self.authorLabel.setText(f'Author: {inDict["author"]}')
        self.pagesLabel.setText(f'Page Count: {inDict["pages"]}')
        self.publisherLabel.setText(f'Publisher: {inDict["publisher"]}')
        self.yearLabel.setText(f'Original Publication Year: {inDict["year"]}')
        self.ISBNLabel.setText(f'ISBN: {inDict["isbn"]}')
        self.summaryLabel.setPlainText(inDict["summary"])
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(self.imageData)
        self.imageLabel.setPixmap(QtGui.QPixmap(pixmap))

    def popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle('Error')
        msg.setText('No results found')
        x = msg.exec_()

    def addClicked(self):
        getTimestamp = datetime.date.today()
        timestamp = getTimestamp.strftime("%Y-%m-%d")
        newDict = {}
        newDict = self.metadataDict
        for k, v in newDict.items():
            if v is None:
                newDict[k] = 'NULL'
        q = QtSql.QSqlQuery()
        q.exec_(
            f"INSERT INTO Books VALUES ('{newDict['title']}', '{newDict['author']}', '{newDict['series']}', {newDict['year']}, '{newDict['publisher']}', {newDict['pages']}, '{newDict['isbn']}', 'SUMMARY', 0, 0, 0, {timestamp}, NULL, NULL);")
        # Trigger model.select() here
        playsound('ding.wav')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
