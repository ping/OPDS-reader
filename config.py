#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__   = 'GPL v3'
__copyright__ = '2015, Steinar Bang ; 2020, un_pogaz <un.pogaz@gmail.com>'
__docformat__ = 'restructuredtext en'

try:
    load_translations()
except NameError:
    pass # load_translations() added in calibre 1.9

try:
    from qt.core import QWidget, QGridLayout, QLabel, QComboBox, QCheckBox
except ImportError:
    from PyQt5.Qt import QWidget, QGridLayout, QLabel, QComboBox, QCheckBox

from calibre import prints
from .common_utils import debug_print, get_icon, PLUGIN_NAME, PREFS_json

PLUGIN_ICON = 'images/plugin.png'

class KEY:
    OPDS_URL = 'opds_url'
    HIDE_NEWSPAPERS = 'hideNewspapers'
    HIDE_BOOK = 'hideBooksAlreadyInLibrary'

class TEXT:
    OPDS_URL = _('OPDS URL:')
    HIDE_NEWSPAPERS = _('Hide Newspapers')
    HIDE_BOOK = _('Hide books already in library')

PREFS = PREFS_json()

PREFS.defaults[KEY.OPDS_URL] = ['http://localhost:8080/opds']
PREFS.defaults[KEY.HIDE_NEWSPAPERS] = True
PREFS.defaults[KEY.HIDE_BOOK] = True

if PREFS.defaults[KEY.OPDS_URL][0] not in PREFS[KEY.OPDS_URL]:
    PREFS[KEY.OPDS_URL] = PREFS[KEY.OPDS_URL] + PREFS.defaults[KEY.OPDS_URL]

def saveOpdsUrlCombobox(opdsUrlEditor):
    opdsUrls = []
    debug_print('item count: {:d}'.format(opdsUrlEditor.count()))
    for i in range(opdsUrlEditor.count()):
        debug_print('item {:d}: {:s}'.format(i, opdsUrlEditor.itemText(i)))
        opdsUrls.append(opdsUrlEditor.itemText(i))
    # Move the selected item first in the list
    currentSelectedUrlIndex = opdsUrlEditor.currentIndex()
    if currentSelectedUrlIndex > 0:
        currentUrl = opdsUrls[currentSelectedUrlIndex]
        del opdsUrls[currentSelectedUrlIndex]
        opdsUrls.insert(0, currentUrl)
    return opdsUrls

class ConfigWidget(QWidget):
    def __init__(self, plugin_action):
        QWidget.__init__(self)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        labelColumnWidths = []
        
        self.opdsUrlLabel = QLabel(TEXT.OPDS_URL)
        self.layout.addWidget(self.opdsUrlLabel, 0, 0)
        labelColumnWidths.append(self.layout.itemAtPosition(0, 0).sizeHint().width())
        
        self.opdsUrlEditor = QComboBox(self)
        self.opdsUrlEditor.addItems(PREFS[KEY.OPDS_URL])
        self.opdsUrlEditor.setEditable(True)
        self.opdsUrlEditor.setInsertPolicy(QComboBox.InsertAtTop)
        self.layout.addWidget(self.opdsUrlEditor, 0, 1)
        self.opdsUrlLabel.setBuddy(self.opdsUrlEditor)
        
        self.hideNewsCheckbox = QCheckBox(TEXT.HIDE_NEWSPAPERS, self)
        self.hideNewsCheckbox.setChecked(PREFS[KEY.HIDE_NEWSPAPERS])
        self.layout.addWidget(self.hideNewsCheckbox, 1, 0)
        labelColumnWidths.append(self.layout.itemAtPosition(1, 0).sizeHint().width())
        
        self.hideBooksAlreadyInLibraryCheckbox = QCheckBox(TEXT.HIDE_BOOK, self)
        self.hideBooksAlreadyInLibraryCheckbox.setChecked(PREFS[KEY.HIDE_BOOK])
        self.layout.addWidget(self.hideBooksAlreadyInLibraryCheckbox, 2, 0)
        labelColumnWidths.append(self.layout.itemAtPosition(2, 0).sizeHint().width())
        
        labelColumnWidth = max(labelColumnWidths)
        self.layout.setColumnMinimumWidth(1, labelColumnWidth * 2)
    
    def save_settings(self):
        PREFS[KEY.HIDE_NEWSPAPERS] = self.hideNewsCheckbox.isChecked()
        PREFS[KEY.HIDE_BOOK] = self.hideBooksAlreadyInLibraryCheckbox.isChecked()
        PREFS[KEY.OPDS_URL] = saveOpdsUrlCombobox(self.opdsUrlEditor)
