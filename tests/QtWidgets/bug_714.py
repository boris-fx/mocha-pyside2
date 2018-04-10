#############################################################################
##
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the test suite of the Qt for Python project.
##
## $QT_BEGIN_LICENSE:GPL-EXCEPT$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 3 as published by the Free Software
## Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

import unittest
import sys
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QLabel, QApplication

class TestLabelPixmap(unittest.TestCase):
    def testReference(self):
        l = QLabel()
        p = QPixmap()
        l.setPixmap(p) # doesn't increment pixmap ref because this makes a copy
        self.assertEqual(sys.getrefcount(p), 2)

        p = l.pixmap()
        # this used to increment the reference because this is
        # an internal pointer, but not anymore since we don't create
        # a copy
        # self.assertEqual(sys.getrefcount(p), 3)
        self.assertEqual(sys.getrefcount(p), 2)

        p2 = l.pixmap()
        self.assertEqual(p, p2)

if __name__ == '__main__':
    app = QApplication([])
    unittest.main()

