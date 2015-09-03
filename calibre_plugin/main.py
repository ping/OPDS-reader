import sys
from PyQt5.Qt import QDialog, QGridLayout, QPushButton, QCheckBox, QMessageBox, QLabel, QAbstractItemView, QTableView, QHeaderView
from calibre.web.feeds import feedparser

from calibre_plugins.opds_client.model import OpdsBooksModel
from calibre_plugins.opds_client.config import prefs

class OpdsDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config

        self.db = gui.current_db

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.opds_url = QLabel(prefs['opds_url'])

        self.setWindowTitle('OPDS Client')
        self.setWindowIcon(icon)

        self.library_view = QTableView(self)
        self.model = self.dummy_books()
        self.library_view.setModel(OpdsBooksModel(None, self.model, self.db))
        self.library_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.library_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.library_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.library_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        rowHeight = self.library_view.horizontalHeader().height()
        for rowNumber in range (0, self.library_view.model().rowCount(None)):
            self.library_view.setRowHeight(rowNumber, rowHeight)
        self.library_view.resizeColumnsToContents()
        buttonRowColumnNumber = 9
        self.layout.addWidget(self.library_view, 0, 0, 3, buttonRowColumnNumber + 1)

        self.hideNewsCheckbox = QCheckBox('Hide Newspapers', self)
        self.hideNewsCheckbox.clicked.connect(self.setHideNewspapers)
        self.hideNewsCheckbox.setChecked(True)
        self.layout.addWidget(self.hideNewsCheckbox, 3, 0)

        self.hideBooksAlreadyInLibraryCheckbox = QCheckBox('Hide books already in library', self)
        self.hideBooksAlreadyInLibraryCheckbox.clicked.connect(self.setHideBooksAlreadyInLibrary)
        self.hideBooksAlreadyInLibraryCheckbox.setChecked(True)
        self.layout.addWidget(self.hideBooksAlreadyInLibraryCheckbox, 4, 0)

        buttonColumnWidths = []
        self.about_button = QPushButton('About', self)
        self.about_button.clicked.connect(self.about)
        self.layout.addWidget(self.about_button, 3, buttonRowColumnNumber)
        buttonColumnWidths.append(self.layout.itemAtPosition(3, buttonRowColumnNumber).sizeHint().width()) 

        self.download_opds_button = QPushButton('Download OPDS', self)
        self.download_opds_button.clicked.connect(self.download_opds)
        self.layout.addWidget(self.download_opds_button, 4, buttonRowColumnNumber)
        buttonColumnWidths.append(self.layout.itemAtPosition(4, buttonRowColumnNumber).sizeHint().width()) 

        self.conf_button = QPushButton('Plugin configuration', self)
        self.conf_button.clicked.connect(self.config)
        self.layout.addWidget(self.conf_button, 5, buttonRowColumnNumber)
        buttonColumnWidths.append(self.layout.itemAtPosition(5, buttonRowColumnNumber).sizeHint().width()) 

        # Make all columns of the grid layout the same width as the button column
        buttonColumnWidth = max(buttonColumnWidths)
        for columnNumber in range(0, buttonRowColumnNumber):
            self.layout.setColumnMinimumWidth(columnNumber, buttonColumnWidth)

        self.resize(self.sizeHint())

    def setHideNewspapers(self, checked):
        self.model.setFilterBooksThatAreNewspapers(checked)

    def setHideBooksAlreadyInLibrary(self, checked):
        self.model.setFilterBooksThatAreAlreadyInLibrary(checked)

    def about(self):
        text = get_resources('about.txt')
        QMessageBox.about(self, 'About the OPDS Client plugin', text.decode('utf-8'))

    def download_opds(self):
        feed = feedparser.parse(prefs['opds_url'])
        print feed
        newest_url = feed['entries'][0]['links'][0]['href']
        print newest_url
        newest_feed = feedparser.parse(newest_url)
        self.model = OpdsBooksModel(None, newest_feed['entries'], self.db)
        self.model.setFilterBooksThatAreNewspapers(self.hideNewsCheckbox.isChecked())
        self.model.setFilterBooksThatAreAlreadyInLibrary(self.hideBooksAlreadyInLibraryCheckbox.isChecked())
        self.library_view.setModel(self.model)
        self.library_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.library_view.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.library_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.resize(self.sizeHint())

    def config(self):
        self.do_user_config(parent=self)
        self.opds_url.setText(prefs['opds_url'])

    def dummy_books(self):
        dummy_author = ' ' * 40
        dummy_title = ' ' * 60
        dummy_updated = ' ' * 20
        books_list = []
        for line in range (1, 10):
            book = {}
            book[u'author'] = dummy_author
            book[u'title'] = dummy_title
            book[u'updated'] = dummy_updated
            books_list.append(book)
        return books_list