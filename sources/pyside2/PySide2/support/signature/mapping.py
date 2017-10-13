#############################################################################
##
## Copyright (C) 2017 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of PySide2.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 3 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL3 included in the
## packaging of this file. Please review the following information to
## ensure the GNU Lesser General Public License version 3 requirements
## will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 2.0 or (at your option) the GNU General
## Public license version 3 or any later version approved by the KDE Free
## Qt Foundation. The licenses are as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-2.0.html and
## https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

from __future__ import print_function, absolute_import

"""
signature_mapping.py

This module has the mapping from the pyside C-modules view of signatures
to the Python representation.

The PySide modules are not loaded in advance, but only after they appear
in sys.modules. This minimises the loading overhead.
In principle, we need to re-load the module, when the imports change.
But it is much easier to do it on demand, when we get an exception.
See _resolve_value() in singature.py
"""

import sys
import collections
import struct
import PySide2

PY3 = sys.version_info >= (3,)
if PY3:
    from . import typing
    ellipsis = eval("...")
    Char = typing.Union[str, int]     # how do I model the limitation to 1 char?
    StringList = typing.List[str]
    Variant = typing.Union[str, int, float, Char, StringList, type(ellipsis)]
              # Much more, do we need that? Do we better kill it?
    ModelIndexList = typing.List[int]
    QImageCleanupFunction = typing.Callable[[bytes], None]
    FloatMatrix = typing.List[typing.List[float]]
else:
    ellipsis = "..."
    Char = str
    StringList = list
    Variant = object
    ModelIndexList = list
    QImageCleanupFunction = object
    FloatMatrix = list
Pair = collections.namedtuple('Pair', ['first', 'second'])
# ulong_max is only 32 bit on windows.
ulong_max = 2*sys.maxsize+1 if len(struct.pack("L", 1)) != 4 else 0xffffffff
ushort_max = 0xffff

GL_COLOR_BUFFER_BIT = 0x00004000
GL_NEAREST = 0x2600

WId = int

# from 5.9
GL_TEXTURE_2D = 0x0DE1
GL_RGBA = 0x1908

# Some types are abstract. They just show their name.
class Virtual(str):
    def __repr__(self):
        return "Virtual({})".format(self)

# Other types I simply could not find.
class Missing(str):
    def __repr__(self):
        return "Missing({})".format(self)

class Reloader(object):
    def __init__(self):
        self.sys_module_count = 0
        self.uninitialized = PySide2.__all__[:]

    def update(self):
        if self.sys_module_count == len(sys.modules):
            return
        self.sys_module_count = len(sys.modules)
        for mod_name in self.uninitialized[:]:
            if "PySide2." + mod_name in sys.modules:
                self.uninitialized.remove(mod_name)
                proc_name = "init_" + mod_name
                if proc_name in globals():
                    init_proc = globals()[proc_name]
                    globals().update(init_proc())

update_mapping = Reloader().update
type_map = {}

def init_QtCore():
    import PySide2.QtCore
    from PySide2.QtCore import Qt, QUrl, QDir, QGenericArgument
    from PySide2.QtCore import QRect, QSize, QPoint
    from PySide2.QtCore import QMarginsF # 5.9
    try:
        # seems to be not generated by 5.9 ATM.
        from PySide2.QtCore import Connection
    except ImportError:
        pass
    type_map.update({
        "str": str,
        "int": int,
        "QString": str,
        "bool": bool,
        "PyObject": object,
        "void": int, # be more specific?
        "char": Char,
        "'%'": "%",
        "' '": " ",
        "false": False,
        "double": float,
        "'g'": "g",
        "long long": int,
        "unsigned int": int, # should we define an unsigned type?
        "Q_NULLPTR": None,
        "long": int,
        "float": float,
        "short": int,
        "unsigned long": int,
        "unsigned long long": int,
        "unsigned short": int,
        "QStringList": StringList,
        "QList": list,
        "QChar": Char,
        "signed char": Char,
        "QVariant": Variant,
        "QVariant.Type": type, # not so sure here...
        "QStringRef": str,
        "QString()": None, # unclear: "" would be isEmpty(), but not isNull()
        "QModelIndexList": ModelIndexList,
        "QPair": Pair,
        "unsigned char": Char,
        "QSet": set, # seems _not_ to work
        "QVector": list,
        "QJsonObject": dict, # seems to work
        "QStringList()": [],
        "ULONG_MAX": ulong_max,
        "quintptr": int,
        "PyCallable": callable,
        "...": ellipsis, # no idea how this should be translated... maybe so?
        "PyTypeObject": type,
        "PySequence": list, # needs to be changed, QApplication for instance!
        "qptrdiff": int,
        "true": True,
        "Qt.HANDLE": int, # be more explicit with some consts?
        "list of QAbstractState": list, # how to use typing.List when we don't have QAbstractState?
        "list of QAbstractAnimation": list, # dto.
        "QVariant()": (ellipsis,), # no idea what to use here for "invalid Variant"?
        "QMap": dict,
        "PySide2.QtCore.bool": bool,
        "QHash": dict,
        "PySide2.QtCore.QChar": Char,
        "PySide2.QtCore.qreal": float,
        "PySide2.QtCore.float": float,
        "PySide2.QtCore.qint16": int,
        "PySide2.QtCore.qint32": int,
        "PySide2.QtCore.qint64": int,
        "PySide2.QtCore.qint8": int,
        "PySide2.QtCore.QString": str,
        "PySide2.QtCore.QStringList": StringList,
        "PySide2.QtCore.QVariant": Variant,
        "PySide2.QtCore.quint16": int,
        "PySide2.QtCore.quint32": int,
        "PySide2.QtCore.quint64": int,
        "PySide2.QtCore.quint8": int,
        "PySide2.QtCore.uchar": Char,
        "QGenericArgument(0)": QGenericArgument(None),
        "PySide2.QtCore.long": int,
        "PySide2.QtCore.QUrl.ComponentFormattingOptions":
            PySide2.QtCore.QUrl.ComponentFormattingOption, # mismatch option/enum, why???
        "QUrl.FormattingOptions(PrettyDecoded)": QUrl.FormattingOptions(QUrl.PrettyDecoded),
        # from 5.9
        "QDir.Filters(AllEntries | NoDotAndDotDot)": QDir.Filters(QDir.AllEntries |
                                                                  QDir.NoDotAndDotDot),
        "QGenericArgument(Q_NULLPTR)": QGenericArgument(None),
        "NULL": None, # 5.6, MSVC
        "QGenericArgument(NULL)": QGenericArgument(None), # 5.6, MSVC
        "QDir.SortFlags(Name | IgnoreCase)": QDir.SortFlags(QDir.Name | QDir.IgnoreCase),
        "PyBytes": bytes,
        "PyUnicode": str if PY3 else unicode,
        "signed long": int,
        "PySide2.QtCore.int": int,
        "PySide2.QtCore.char": StringList, # A 'char **' is a list of strings.
        "char[]": StringList, # 5.9
        "unsigned long int": int, # 5.6, RHEL 6.6
        "unsigned short int": int, # 5.6, RHEL 6.6
        "QGenericArgument((0))": None, # 5.6, RHEL 6.6. Is that ok?
        "4294967295UL": 4294967295, # 5.6, RHEL 6.6
        "PySide2.QtCore.int32_t": int, # 5.9
        "PySide2.QtCore.int64_t": int, # 5.9
        "UnsignedShortType": int, # 5.9
        "nullptr": None, # 5.9
        "uint64_t": int, # 5.9
        "PySide2.QtCore.uint32_t": int, # 5.9
        "float[][]": FloatMatrix, # 5.9
        "PySide2.QtCore.unsigned int": int, # 5.9 Ubuntu
        "PySide2.QtCore.long long": int, # 5.9, MSVC 15
        "QGenericArgument(nullptr)": QGenericArgument(None), # 5.10
    })
    try:
        type_map.update({
            "PySide2.QtCore.QMetaObject.Connection": PySide2.QtCore.Connection, # wrong!
        })
    except AttributeError:
        # this does not exist on 5.9 ATM.
        pass
    return locals()

def init_QtGui():
    import PySide2.QtGui
    from PySide2.QtGui import QPageLayout, QPageSize # 5.9
    type_map.update({
        "QVector< QTextLayout.FormatRange >()": [], # do we need more structure?
        "USHRT_MAX": ushort_max,
        "0.0f": 0.0,
        "1.0f": 1.0,
        "uint32_t": int,
        "uint8_t": int,
        "int32_t": int,
        "GL_COLOR_BUFFER_BIT": GL_COLOR_BUFFER_BIT,
        "GL_NEAREST": GL_NEAREST,
        "WId": WId,
        "PySide2.QtGui.QPlatformSurface": Virtual("PySide2.QtGui.QPlatformSurface"), # hmm...
        "QList< QTouchEvent.TouchPoint >()": list,
        "QPixmap()": lambda:QPixmap(), # we cannot create this without qApp
    })
    return locals()

def init_QtWidgets():
    import PySide2.QtWidgets
    from PySide2.QtWidgets import QWidget, QMessageBox, QStyleOption, QStyleHintReturn, QStyleOptionComplex
    from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem # 5.9
    if PY3:
        GraphicsItemList = typing.List[QGraphicsItem]
        StyleOptionGraphicsItemList = typing.List[QStyleOptionGraphicsItem]
    else:
        GraphicsItemList = list
        StyleOptionGraphicsItemList = list
    type_map.update({
        "QMessageBox.StandardButtons(Yes | No)": QMessageBox.StandardButtons(
            QMessageBox.Yes | QMessageBox.No),
        "QWidget.RenderFlags(DrawWindowBackground | DrawChildren)": QWidget.RenderFlags(
            QWidget.DrawWindowBackground | QWidget.DrawChildren),
        "static_cast<Qt.MatchFlags>(Qt.MatchExactly|Qt.MatchCaseSensitive)": (
            Qt.MatchFlags(Qt.MatchExactly | Qt.MatchCaseSensitive)),
        "QVector< int >()": [],
        # from 5.9
        "Type": PySide2.QtWidgets.QListWidgetItem.Type,
        "SO_Default": QStyleOption.SO_Default,
        "SH_Default": QStyleHintReturn.SH_Default,
        "SO_Complex": QStyleOptionComplex.SO_Complex,
        "QGraphicsItem[]": GraphicsItemList,
        "QStyleOptionGraphicsItem[]": StyleOptionGraphicsItemList,
    })
    return locals()

def init_QtSql():
    import PySide2.QtSql
    from PySide2.QtSql import QSqlDatabase
    type_map.update({
        "QLatin1String(defaultConnection)": QSqlDatabase.defaultConnection,
        "QVariant.Invalid": -1, # not sure what I should create, here...
    })
    return locals()

def init_QtNetwork():
    import PySide2.QtNetwork
    type_map.update({
        "QMultiMap": typing.DefaultDict(list) if PY3 else {},
    })
    return locals()

def init_QtXmlPatterns():
    import PySide2.QtXmlPatterns
    from PySide2.QtXmlPatterns import QXmlName
    type_map.update({
        "QXmlName.PrefixCode": Missing("PySide2.QtXmlPatterns.QXmlName.PrefixCode"),
        "QXmlName.NamespaceCode": Missing("PySide2.QtXmlPatterns.QXmlName.NamespaceCode")
    })
    return locals()

def init_QtMultimedia():
    import PySide2.QtMultimedia
    import PySide2.QtMultimediaWidgets
    type_map.update({
        "QVariantMap": dict,
        "QGraphicsVideoItem": PySide2.QtMultimediaWidgets.QGraphicsVideoItem,
        "QVideoWidget": PySide2.QtMultimediaWidgets.QVideoWidget,
    })
    return locals()

def init_QtOpenGL():
    import PySide2.QtOpenGL
    type_map.update({
        "GLuint": int,
        "GLenum": int,
        "GLint": int,
        "GLbitfield": int,
        "PySide2.QtOpenGL.GLint": int,
        "PySide2.QtOpenGL.GLuint": int,
        "GLfloat": float, # 5.6, MSVC 15
    })
    return locals()

def init_QtQml():
    import PySide2.QtQml
    type_map.update({
        "QJSValueList()": [],
        "PySide2.QtQml.bool volatile": bool,
        # from 5.9
        "QVariantHash()": {},
    })
    return locals()

def init_QtQuick():
    import PySide2.QtQuick
    type_map.update({
        "PySide2.QtQuick.QSharedPointer": int,
        "PySide2.QtCore.uint": int,
        "T": int,
    })
    return locals()

def init_QtScript():
    import PySide2.QtScript
    type_map.update({
        "QScriptValueList()": [],
    })
    return locals()

def init_QtTest():
    import PySide2.QtTest
    type_map.update({
        "PySide2.QtTest.QTouchEventSequence": PySide2.QtTest.QTest.QTouchEventSequence,
    })
    return locals()

# from 5.9
def init_QtWebEngineWidgets():
    import PySide2.QtWebEngineWidgets
    type_map.update({
        "PySide2.QtTest.QTouchEventSequence": PySide2.QtTest.QTest.QTouchEventSequence,
    })
    return locals()

# from 5.6, MSVC
def init_QtWinExtras():
    import PySide2.QtWinExtras
    type_map.update({
        "QList< QWinJumpListItem* >()": [],
    })
    return locals()

# Here was testbinding, actually the source of all evil.

# end of file
