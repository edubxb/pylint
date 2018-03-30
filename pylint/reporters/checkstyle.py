# Copyright (c) 2018 Eduardo Bellido Bellido <edubxb@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Checkstyle reporter"""
from __future__ import absolute_import, print_function

import sys
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from xml.sax.saxutils import escape

from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter


class CheckstyleReporter(BaseReporter):
    """Report messages and layouts in Checkstyle XML format.
    Checkstyle project web: http://checkstyle.sourceforge.net/"""

    __implements__ = IReporter
    name = 'checkstyle'
    extension = 'xml'

    _SEVERITY = {
        'C': 'info',
        'R': 'warning',
        'W': 'warning',
        'E': 'error',
        'F': 'error'
    }

    def __init__(self, output=sys.stdout):
        BaseReporter.__init__(self, output)
        self._paths = {}
        self._xml = Element('checkstyle', {'version': '0.0.0'})

    def handle_message(self, msg):
        """Manage message of different type and in the context of path."""
        path = self._paths.get(msg.path)
        if not path:
            path = SubElement(self._xml, 'file', {'name': msg.path})
            self._paths[msg.path] = path
        SubElement(path, 'error', {
            'column': str(msg.column),
            'line': str(msg.line),
            'message': msg.msg_id + ': ' + escape(msg.msg),
            'severity': CheckstyleReporter._SEVERITY[msg.msg_id[0]],
            'source': 'pylint'
        })

    def display_messages(self, layout):
        """Launch layouts display"""
        if self._paths:
            xml = parseString(tostring(self._xml, encoding='utf-8')).toprettyxml(indent="  ")
            print(xml, file=self.out)

    def display_reports(self, layout):  # pylint: disable=arguments-differ
        """Don't do nothing in this reporter."""

    def _display(self, layout):
        """Don't do nothing."""


def register(linter):
    """Register the reporter classes with the linter."""
    linter.register_reporter(CheckstyleReporter)
