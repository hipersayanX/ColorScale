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

def calculateSector(color=0, nColors=0):
    diff = 256 / (nColors - 1)

    return int(color / diff)

def calculateGreyLimits(color=0, nColors=0):
    diff = 255 / (nColors - 1)
    sector = calculateSector(color, nColors)

    lower = int(diff * sector)
    upper = int(diff * (sector + 1))

    return (lower, upper)

def calculateColorLimits(colorTable=[], sector=0):
    lower = colorTable[sector]
    upper = colorTable[sector + 1]

    return (lower, upper)

def calcualateFactor(color=0, lower=0, upper=0):
    return (color - lower) / (upper - lower)

def calculateColor(k=0, lower=[], upper=[]):
    color = []

    for i in range(len(lower)):
        color.append(int(k * (upper[i] - lower[i]) + lower[i]))

    return color

def transformColor(colorTable=[], color=0):
    lower, upper = calculateGreyLimits(color, len(colorTable))
    k = calcualateFactor(color, lower, upper)
    sector = calculateSector(color, len(colorTable))
    lowerColor, upperColor = calculateColorLimits(colorTable, sector)

    return calculateColor(k, lowerColor, upperColor)

def createTransformTable(colorTable=[]):
    transformTable = []

    for i in range(256):
        transformTable.append(transformColor(colorTable, i))

    return transformTable

def sortByLuma(colorTable=[]):
    # colorTable = [int0, int1, int2, ..., intN]
    lumaTable = []

    # lumaTable = [[luma0, int0],
    #              [luma1, int1],
    #              [luma2, int2],
    #                   ...     ,
    #              [lumaN, intN]]
    for color in colorTable:
        r = color & 0xff
        g = (color >> 8) & 0xff
        b = (color >> 16) & 0xff
        lumaTable.append([(r + g + b) / 3, color])

    lumaTable.sort()

    sortedColorTable = []

    # lumaTable = [[r0, g0, b0],
    #              [r1, g1, b1],
    #              [r2, g2, b2],
    #                   ...     ,
    #              [rN, gN, bN]]
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
            # Get a new pixel
            pixel = image.pixel(x, y)

            # Calculate the number of times that this
            # color has been used in the image
            if pixel in mostUsed:
                mostUsed[pixel] += 1
            else:
                mostUsed[pixel] = 0

    mostUsedTable = []

    # Sort colors by usage.
    for color in mostUsed:
        mostUsedTable.append([mostUsed[color], color])

    mostUsedTable.sort()

    # Cut it to show only the nColors most used colors or less.
    mostUsedTable.reverse()

    usedColors = min(len(mostUsedTable), nColors)
    colorTable = []

    for i in range(usedColors):
        colorTable.append(mostUsedTable[i][1])

    # Returns the colors sorted by luminance.
    return sortByLuma(colorTable)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    # Replace the grey color by orange.
    #colorTable = [[  0,   0,   0],
                  #[225, 127,   0],
                  #[255, 255, 255]]

    # Rainbow
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
    image = QtGui.QImage('/home/hipersayan_x/Imagenes/varios/ecchi_halloween.jpg')
    image = image.scaled(size, QtCore.Qt.KeepAspectRatio)

    #colorTable = createColorTable(image, 256)
    transformTable = createTransformTable(colorTable)

    for y in range(image.height()):
        for x in range(image.width()):
            # Get a pixel from the image.
            pixel = image.pixel(x, y)
            r = pixel & 0xff
            g = (pixel >> 8) & 0xff
            b = (pixel >> 16) & 0xff

            # Calculate the color luminance
            color = round((r + g + b) / 3.0)

            # and transform it to the new color.
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
