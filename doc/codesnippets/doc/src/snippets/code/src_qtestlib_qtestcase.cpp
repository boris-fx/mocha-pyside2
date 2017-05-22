/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the documentation of PySide2.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

//! [0]
QVERIFY(1 + 1 == 2)
//! [0]


//! [1]
QVERIFY2(1 + 1 == 2, "A breach in basic arithmetic occured.")
//! [1]


//! [2]
QCOMPARE(QString("hello").toUpper(), QString("HELLO"))
//! [2]


//! [3]
void TestQString.toInt_data()
{
    QTest.addColumn<QString>("aString")
    QTest.addColumn<int>("expected")

    QTest.newRow("positive value") << "42" << 42
    QTest.newRow("negative value") << "-42" << -42
    QTest.newRow("zero") << "0" << 0
}
//! [3]


//! [4]
void TestQString.toInt()
{
     QFETCH(QString, aString)
     QFETCH(int, expected)

     QCOMPARE(aString.toInt(), expected)
}
//! [4]


//! [5]
if (sizeof(int) != 4)
    QFAIL("This test has not been ported to this platform yet.")
//! [5]


//! [6]
QFETCH(QString, myString)
QCOMPARE(QString("hello").toUpper(), myString)
//! [6]


//! [7]
QTEST(QString("hello").toUpper(), "myString")
//! [7]


//! [8]
if (!QSqlDatabase.drivers().contains("SQLITE"))
    QSKIP("This test requires the SQLITE database driver", SkipAll)
//! [8]


//! [9]
QEXPECT_FAIL("", "Will fix in the next release", Continue)
QCOMPARE(i, 42)
QCOMPARE(j, 43)
//! [9]


//! [10]
QEXPECT_FAIL("data27", "Oh my, this is soooo broken", Abort)
QCOMPARE(i, 42)
//! [10]


//! [11]
class TestQString: public QObject { ... }
QTEST_MAIN(TestQString)
//! [11]


//! [12]
#ifdef Q_WS_X11
    QTEST_MAIN(MyX11Test)
#else
    // do nothing on non-X11 platforms
    QTEST_NOOP_MAIN
#endif
//! [12]


//! [13]
QTest.keyClick(myWidget, 'a')
//! [13]


//! [14]
QTest.keyClick(myWidget, Qt.Key_Escape)

QTest.keyClick(myWidget, Qt.Key_Escape, Qt.ShiftModifier, 200)
//! [14]


//! [15]
QTest.keyClicks(myWidget, "hello world")
//! [15]


//! [16]
namespace QTest {
    template<>
    char *toString(const MyPoint &point)
    {
        QByteArray ba = "MyPoint("
        ba += QByteArray.number(point.x()) + ", " + QByteArray.number(point.y())
        ba += ")"
        return qstrdup(ba.data())
    }
}
//! [16]


//! [17]
int i = 0
while (myNetworkServerNotResponding() && i++ < 50)
    QTest.qWait(250)
//! [17]


//! [18]
MyFirstTestObject test1
QTest.qExec(&test1)

MySecondTestObject test2
QTest.qExec(&test2)
//! [18]


//! [19]
QDir dir

QTest.ignoreMessage(QtWarningMsg, "QDir.mkdir: Empty or null file name(s)")
dir.mkdir("")
//! [19]


//! [20]
void myTestFunction_data()
{
    QTest.addColumn<QString>("aString")
    QTest.newRow("just hello") << QString("hello")
    QTest.newRow("a null string") << QString()
}
//! [20]


//! [21]
void myTestFunction_data() {
    QTest.addColumn<int>("intval")
    QTest.addColumn<QString>("str")
    QTest.addColumn<double>("dbl")

    QTest.newRow("row1") << 1 << "hello" << 1.5
}
//! [21]


//! [22]
void MyTestClass.cleanup()
{
    if (qstrcmp(currentTestFunction(), "myDatabaseTest") == 0) {
        // clean up all database connections
        closeAllDatabases()
    }
}
//! [22]


//! [23]
QTest.qSleep(250)
//! [23]

//! [24]
widget = QWidget()
widget.show()
QTest.qWaitForWindowShown(widget)
//! [24]
