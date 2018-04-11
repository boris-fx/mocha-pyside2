############################################################################
##
## Copyright (C) 2016 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of the examples of the Qt for Python project.
##
## $QT_BEGIN_LICENSE:BSD$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## BSD License Usage
## Alternatively, you may use this file under the terms of the BSD license
## as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
############################################################################

//! [0]
from PySide2.QtGui import *
//! [0]

//! [1]
def __init__(self):
    textEdit =  QTextEdit()
    setCentralWidget(textEdit)

    createActions()
    createMenus()
    createToolBars()
    createStatusBar()
    createDockWindows()

    setWindowTitle(tr("Dock Widgets"))

    Letter()
    setUnifiedTitleAndToolBarOnMac(True)
//! [1]

//! [2]
def Letter(self)
    textEdit.clear()

    cursor = QTextCursor(textEdit.textCursor())
    cursor.movePosition(QTextCursor.Start)
    topFrame = cursor.currentFrame()
    topFrameFormat = topFrame.frameFormat()
    topFrameFormat.setPadding(16)
    topFrame.setFrameFormat(topFrameFormat)

    textFormat = QTextCharFormat()
    boldFormat = QTextCharFormat()
    boldFormat.setFontWeight(QFont.Bold)
    italicFormat = QTextCharFormat()
    italicFormat.setFontItalic(True)

    tableFormat = QTextTableFormat()
    tableFormat.setBorder(1)
    tableFormat.setCellPadding(16)
    tableFormat.setAlignment(Qt.AlignRight)
    cursor.insertTable(1, 1, tableFormat)
    cursor.insertText("The Firm", boldFormat)
    cursor.insertBlock()
    cursor.insertText("321 City Street", textFormat)
    cursor.insertBlock()
    cursor.insertText("Industry Park")
    cursor.insertBlock()
    cursor.insertText("Some Country")
    cursor.setPosition(topFrame.lastPosition())
    cursor.insertText(QDate.currentDate().toString("d MMMM yyyy"), textFormat)
    cursor.insertBlock()
    cursor.insertBlock()
    cursor.insertText("Dear ", textFormat)
    cursor.insertText("NAME", italicFormat)
    cursor.insertText(",", textFormat)
    for i in range(3):
        cursor.insertBlock()
    cursor.insertText(tr("Yours sincerely,"), textFormat)
    for i in range(3):
        cursor.insertBlock()
    cursor.insertText("The Boss", textFormat)
    cursor.insertBlock()
    cursor.insertText("ADDRESS", italicFormat)
//! [2]

//! [3]
def print(self)
    document = textEdit.document()
    printer = QPrinter()

    dlg =  QPrintDialog(&printer, self)
    if dlg.exec() != QDialog.Accepted:
        return

    document.print(printer)
    statusBar().showMessage(tr("Ready"), 2000)
//! [3]

//! [4]
def save(self):
    fileName = QFileDialog.getSaveFileName(self,
                        tr("Choose a file name"), ".",
                        tr("HTML (*.html *.htm)"))
    if fileName.isEmpty():
        return
    file = QFile(fileName)
    if !file.open(QFile.WriteOnly | QFile::Text):
        QMessageBox.warning(self, tr("Dock Widgets"),
                             tr("Cannot write file %1:\n%2.")
                             .arg(fileName)
                             .arg(file.errorString()))
        return
    

    out = QTextStream(file)
    QApplication.setOverrideCursor(Qt::WaitCursor)
    out << textEdit.toHtml()
    QApplication.restoreOverrideCursor()

    statusBar().showMessage(tr("Saved '%1'").arg(fileName), 2000)

//! [4]

//! [5]
def undo(self):
    document = textEdit.document()
    document.undo()

//! [5]

//! [6]
def insertCustomer(self, customer):
    if customer.isEmpty():
        return

    customerList = customer.split(", ")
    document = textEdit.document()
    cursor = document.find("NAME")
    if not cursor.isNull():
        cursor.beginEditBlock()
        cursor.insertText(customerList.at(0))
        oldcursor = cursor
        cursor = document.find("ADDRESS")
        if not cursor.isNull():
            for i in range(customerList.size()):
                cursor.insertBlock()
                cursor.insertText(customerList.at(i))
            
            cursor.endEditBlock()
        else:
            oldcursor.endEditBlock()
//! [6]

//! [7]
def addParagraph(self, paragraph):
    if (paragraph.isEmpty())
        return

    document = textEdit.document()
    cursor = document.find(tr("Yours sincerely,"))
    if cursor.isNull():
        return
    cursor.beginEditBlock()
    cursor.movePosition(QTextCursor.PreviousBlock, QTextCursor.MoveAnchor, 2)
    cursor.insertBlock()
    cursor.insertText(paragraph)
    cursor.insertBlock()
    cursor.endEditBlock()

//! [7]


//! [8]
def createStatusBar(self):
    statusBar().showMessage(tr("Ready"))

//! [8]

//! [9]
def createDockWindows(self):
    dock =  QDockWidget(tr("Customers"), self)
    dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
    customerList =  QListWidget(dock)
    customerList.addItems(QStringList()
            << "John Doe, Harmony Enterprises, 12 Lakeside, Ambleton"
            << "Jane Doe, Memorabilia, 23 Watersedge, Beaton"
            << "Tammy Shea, Tiblanka, 38 Sea Views, Carlton"
            << "Tim Sheen, Caraba Gifts, 48 Ocean Way, Deal"
            << "Sol Harvey, Chicos Coffee, 53 New Springs, Eccleston"
            << "Sally Hobart, Tiroli Tea, 67 Long River, Fedula")
    dock.setWidget(customerList)
    addDockWidget(Qt.RightDockWidgetArea, dock)
    viewMenu.addAction(dock.toggleViewAction())

    dock =  QDockWidget(tr("Paragraphs"), self)
    paragraphsList =  QListWidget(dock)
    paragraphsList.addItems(QStringList()
            << "Thank you for your payment which we have received today."
            << "Your order has been dispatched and should be with you "
               "within 28 days."
            << "We have dispatched those items that were in stock. The "
               "rest of your order will be dispatched once all the "
               "remaining items have arrived at our warehouse. No "
               "additional shipping charges will be made."
            << "You made a small overpayment (less than $5) which we "
               "will keep on account for you, or return at your request."
            << "You made a small underpayment (less than $1), but we have "
               "sent your order anyway. We'll add self underpayment to "
               "your next bill."
            << "Unfortunately you did not send enough money. Please remit "
               "an additional $. Your order will be dispatched as soon as "
               "the complete amount has been received."
            << "You made an overpayment (more than $5). Do you wish to "
               "buy more items, or should we return the excess to you?")
    dock.setWidget(paragraphsList)
    addDockWidget(Qt.RightDockWidgetArea, dock)
    viewMenu.addAction(dock.toggleViewAction())

    connect(customerList, SIGNAL("currentTextChanged(const QString &)"),
            self, SLOT("insertCustomer(const QString &)"))
    connect(paragraphsList, SIGNAL("currentTextChanged(const QString &)"),
            self, SLOT("addParagraph(const QString &)"))
//! [9]
