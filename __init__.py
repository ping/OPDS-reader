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

from calibre.customize import InterfaceActionBase

class ActionOpdsReader(InterfaceActionBase):
    '''
    This class is a simple wrapper that provides information about the actual
    plugin class. The actual interface plugin class is called InterfacePlugin
    and is defined in the ui.py file, as specified in the actual_plugin field
    below.
    
    The reason for having two classes is that it allows the command line
    calibre utilities to run without needing to load the GUI libraries.
    '''
    name = 'OPDS Reader'
    description = _('Import the books from a OPDS catalog')
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'Steinar Bang & un_pogaz'
    version = (2, 2, 0)
    minimum_calibre_version = (2, 0, 0)
    
    actual_plugin = __name__+'.action:OpdsReaderAction'
    
    DEBUG_PRE = 'OPDSreader'
    
    def is_customizable(self):
        '''
        This method must return True to enable customization via
        Preferences->Plugins
        '''
        return True
    
    def config_widget(self):
        '''
        Implement this method and :meth:`save_settings` in your plugin to
        use a custom configuration dialog.
        
        This method, if implemented, must return a QWidget. The widget can have
        an optional method validate() that takes no arguments and is called
        immediately after the user clicks OK. Changes are applied if and only
        if the method returns True.
        
        If for some reason you cannot perform the configuration at this time,
        return a tuple of two strings (message, details), these will be
        displayed as a warning dialog to the user and the process will be
        aborted.
        
        The base class implementation of this method raises NotImplementedError
        so by default no user configuration is possible.
        '''
        # It is important to put this import statement here rather than at the
        # top of the module as importing the config class will also cause the
        # GUI libraries to be loaded, which we do not want when using calibre
        # from the command line
        if self.actual_plugin_:
            from .config import ConfigWidget
            return ConfigWidget(self.actual_plugin_)
    
    def save_settings(self, config_widget):
        '''
        Save the settings specified by the user with config_widget.
        
        :param config_widget: The widget returned by :meth:`config_widget`.
        '''
        config_widget.save_settings()
