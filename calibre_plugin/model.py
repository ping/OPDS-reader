from PyQt5.Qt import Qt, QAbstractTableModel
from calibre.ebooks.metadata.book.base import Metadata

class OpdsBooksModel(QAbstractTableModel):
    column_headers = [_('Title'), _('Author(s)'), _('Updated')]
    column_keys = [u'title', u'author', u'updated']
    filterBooksThatAreNewspapers = False
    filterBooksThatAreAlreadyInLibrary = False

    def __init__(self, parent, books = [], db = None):
        QAbstractTableModel.__init__(self, parent)
        self.db = db
        self.books = books
        self.filterBooks()

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Vertical:
            return section + 1
        if section >= len(self.column_headers):
            return None
        return self.column_headers[section]

    def rowCount(self, parent):
        return len(self.filteredBooks)

    def columnCount(self, parent):
        return len(self.column_keys)

    def data(self, index, role):
        if role != Qt.DisplayRole:
            return None
        row, col = index.row(), index.column()
        if row >= len(self.filteredBooks):
            return None
        opdsBook = self.filteredBooks[row]
        if col >= len(self.column_keys):
            return None
        return opdsBook[self.column_keys[col]]

    def setFilterBooksThatAreAlreadyInLibrary(self, value):
        if value != self.filterBooksThatAreAlreadyInLibrary:
            self.filterBooksThatAreAlreadyInLibrary = value
            self.filterBooks()

    def setFilterBooksThatAreNewspapers(self, value):
        if value != self.filterBooksThatAreNewspapers:
            self.filterBooksThatAreNewspapers = value
            self.filterBooks()

    def filterBooks(self):
        self.beginResetModel()
        self.filteredBooks = []
        for i in range(0, len(self.books)):
            book = self.books[i]
            if (not self.isFilteredNews(book)) and (not self.isFilteredAlreadyInLibrary(book)):
                self.filteredBooks.append(book)
        self.endResetModel()

    def isFilteredNews(self, book):
        if self.filterBooksThatAreNewspapers:
            tags = self.findTags(book)
            if u'News' in tags:
                return True
        return False

    def findTags(self, book):
        tags = []
        summary = book.get(u'summary', u'')
        summarylines = summary.splitlines()
        for lineno in range(0, len(summarylines)):
            if summarylines[lineno].startswith(u'TAGS: '):
                tagsline = summarylines[lineno].replace(u'TAGS: ', u'')
                tagsline = tagsline.replace(u'<br />',u'')
                tagsline = tagsline.replace(u', ', u',')
                tags = tagsline.split(u',')
        return tags

    def isFilteredAlreadyInLibrary(self, book):
        if self.filterBooksThatAreAlreadyInLibrary:
            bookmetadata = Metadata(book['title'], book['author'])
            print bookmetadata
            return self.db.has_book(bookmetadata)
        return False