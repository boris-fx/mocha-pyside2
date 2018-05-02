#############################################################################
##
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the test suite of Qt for Python.
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

from PySide2.QtCore import *
from PySide2.QtWidgets import *
import unittest

class MyModel (QAbstractListModel):

    stupidLine = QLine(0, 0, 10, 10)

    def rowCount(self, parent):
        return 1

    def data(self, index, role):
        return self.stupidLine

class TestBug693(unittest.TestCase):
    def testIt(self):
        app = QApplication([])
        model = MyModel()
        view = QListView()
        view.setModel(model)
        view.show()

        # This must NOT throw the exception:
        # RuntimeError: Internal C++ object (PySide2.QtCore.QLine) already deleted.
        MyModel.stupidLine.isNull()



if __name__ == "__main__":
    unittest.main()
