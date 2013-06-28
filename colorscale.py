#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# ColorScale algorithm and B&W image colorize example.
# Copyright (C) 2013  Gonzalo Exequiel Pedone
#
# This Program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with This Program.  If not, see <http://www.gnu.org/licenses/>.
#
# Email   : hipersayan TOD x TA gmail TOD com
# Web-Site: https://github.com/hipersayanX/ColorScale/

import os, sys

from PyQt4 import QtCore, QtGui

def createTransformTable(colorTable=[]):
    j = 0
    diff = 255 / (len(colorTable) - 1)
    lower = 0
    upper = round(diff)
    transformTable = []

    for i in range(256):
        if lower == upper:
            colorTransform = colorTable[len(colorTable) - 1]
        else:
            k = (i - lower) / (upper - lower)

            colorDiff = [colorTable[j + 1][0] - colorTable[j][0],
                        colorTable[j + 1][1] - colorTable[j][1],
                        colorTable[j + 1][2] - colorTable[j][2]]

            colorTransform = [int(k * colorDiff[0] + colorTable[j][0]),
                            int(k * colorDiff[1] + colorTable[j][1]),
                            int(k * colorDiff[2] + colorTable[j][2])]

        transformTable += [colorTransform]

        if i + 1 >= upper:
            lower = upper
            upper = round((j + 2) * diff)
            upper = 255 if upper > 255 else upper
            j += 1

    return transformTable

def sortByLuma(colorTable=[]):
    lumaMap = {}

    for color in colorTable:
        r = color & 0xff
        g = (color >> 8) & 0xff
        b = (color >> 16) & 0xff
        lumaMap[color] = (r + g + b) / 3

    lumaTable = []

    for color in lumaMap:
        lumaTable.append([lumaMap[color], color])

    lumaTable.sort()

    sortedColorTable = []

    for i in range(len(lumaTable)):
        color = lumaTable[i][1]
        sortedColorTable.append([(color >> 16) & 0xff,
                                 (color >> 8) & 0xff,
                                 color & 0xff])

    return sortedColorTable

def createColorTable(image=None, nColors=256):
    mostUsed = {}

    for y in range(image.height()):
        for x in range(image.width()):
            pixel = image.pixel(x, y)

            if pixel in mostUsed:
                mostUsed[pixel] += 1
            else:
                mostUsed[pixel] = 0

    mostUsedTable = []

    for color in mostUsed:
        mostUsedTable.append([mostUsed[color], color])

    mostUsedTable.sort()
    mostUsedTable.reverse()

    usedColors = min(len(mostUsedTable), nColors)
    colorTable = []

    for i in range(usedColors):
        colorTable.append(mostUsedTable[i][1])

    return sortByLuma(colorTable)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # Replace the grey color by orange.
    #colorTable = [[  0,   0,   0],
                  #[225, 127,   0],
                  #[255, 255, 255]]

    Rainbow
    colorTable = [[255,   0, 255],
                  [  0,   0, 255],
                  [  0, 255, 255],
                  [  0, 255,   0],
                  [255, 255,   0],
                  [255,   0,   0]]

    # Hot colors.
    #colorTable = [[  0,   0,   0],
                  #[255,   0,   0],
                  #[255, 255,   0],
                  #[255, 255, 255]]

    # Soft colors
    #colorTable = [[127,   0, 127],
                  #[255, 191, 255]]

    # Printing blue
    #colorTable = [[  0,   0,   0],
                  #[  0,   0,   0],
                  #[  0, 127, 255],
                  #[  0, 127, 255],
                  #[127, 191, 255],
                  #[127, 191, 255]]

    # Wrong luminance sorting
    #colorTable = [[  0,   0,   0],
                  #[  0, 255, 255],
                  #[  0,   0, 255],
                  #[255, 255, 255]]

    size = QtCore.QSize(800, 600)
    image = QtGui.QImage('someimage.jpg')
    image = image.scaled(size, QtCore.Qt.KeepAspectRatio)

    #colorTable = createColorTable(image, 256)
    transformTable = createTransformTable(colorTable)

    for y in range(image.height()):
        for x in range(image.width()):
            pixel = image.pixel(x, y)
            r = pixel & 0xff
            g = (pixel >> 8) & 0xff
            b = (pixel >> 16) & 0xff
            color = round((r + g + b) / 3.0)

            newColor = transformTable[color][0] << 16 | \
                       transformTable[color][1] << 8 | \
                       transformTable[color][2]

            pixel = image.setPixel(x, y, newColor)

    label = QtGui.QLabel()
    label.resize(size)
    label.setScaledContents(True)
    label.setPixmap(QtGui.QPixmap.fromImage(image))
    label.show()
    app.exec_()
