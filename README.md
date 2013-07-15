ColorScale
==========

Color scale algorithm and B&amp;W image coloring.

Description
===========

_(Draft)_

The algorithm consists in dividing a gray scale by sectors, replace every sector by a new color gradient, and then converting a gray scale image to the new scale. The user defines the contol points by it's colors, and the algorithm redistribute to control points arround the grey scale. The grey scale is divided in nControlPoints - 1.  
Also, this algorithm can be used for reconstructing the color of a grey scaled image by using it's most representative colors.

Implementation
==============

Supposing a RGBA space with {Rbits, Gbits, Bbits[, Abits]} components, the luminance of a color can be calculated as:

    Luma = (R + G + B) / 3

The resolution of the luminance value can be calculated as:

    LumaBits = max(Rbits, Gbits, Bbits)

The maximum value of the luminance can be calculated as:

    LumaMax = 2 ^ LumaBits - 1

An image is composed of many pixels, and a pixel is defined by it color.  
So the maximun number of possible tones for a black and white image is:

    nLumaColors = LumaMax + 1

A grey scale table can be created using each grey tone.  
We can create a color table defined by control ponits, and each control point is defined by a color. The control points are distributted monotonically (or not) and extrapolated to the grey scale table.  
If nColors is the number of control points, we can split the grey scale table in nColors - 1 sectors. We can replace each grey scale sector by the sector defined by the corresponding control points.  
The ecuations for the linear transform are:

    G = k * (getUpperColor(GreyTable, sector) - getLowerColor(GreyTable, sector)) + getLowerColor(GreyTable, sector)
    C = k * (ColorTable[sector + 1] - ColorTable[sector]) + ColorTable[sector]

Examples
========

Here you can see some simple color transforms.

    # Replace the grey color by orange.
    colorTable = [[  0,   0,   0],
                  [225, 127,   0],
                  [255, 255, 255]]

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/middle-orange.png" alt="Replacing the grey color by orange" style="width: 640px; height: 480px" /></center>

    # Rainbow
    colorTable = [[255,   0, 255],
                  [  0,   0, 255],
                  [  0, 255, 255],
                  [  0, 255,   0],
                  [255, 255,   0],
                  [255,   0,   0]]

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/rainbow.png" alt="Rainbow gradient example" style="width: 640px; height: 480px" /></center>

    # Hot colors.
    colorTable = [[  0,   0,   0],
                  [255,   0,   0],
                  [255, 255,   0],
                  [255, 255, 255]]

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/hot-colors.png" alt="Using a red-yellow color palette" style="width: 640px; height: 480px" /></center>

    # Soft colors
    colorTable = [[127,   0, 127],
                  [255, 191, 255]]

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/soft-colors.png" alt="Replace the outermost colors by a contrastless colors" style="width: 640px; height: 480px" /></center>

    # Printing blue
    colorTable = [[  0,   0,   0],
                  [  0,   0,   0],
                  [  0, 127, 255],
                  [  0, 127, 255],
                  [127, 191, 255],
                  [127, 191, 255]]

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/printing-blue.png" alt="Extending outermost and middle colors" style="width: 640px; height: 480px" /></center>

    # Wrong luminance sorting
    colorTable = [[  0,   0,   0],
                  [  0, 255, 255],
                  [  0,   0, 255],
                  [255, 255, 255]]

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/wrong-luma-sort.png" alt="Switching the color luminance in wrong order" style="width: 640px; height: 480px" /></center>

Color reconstruction
====================

The idea is very simple, as said before, each color has a luminance value, the luminance value isn't a unique value, many colors shares the same luminance value, but in some cases when you see a black and white picture you can guess what is the original color of an object depending on his luminance and the context of the scene.  
So, the first step before you can recolor a B&amp;W image is to split the grey scale palette into a few characteristic colors.

    colorTable = [[  0,   0,   0],
                  [255,   0, 255],
                  [  0,   0, 255],
                  [  0, 255, 255],
                  [  0, 255,   0],
                  [255, 255,   0],
                  [255,   0,   0],
                  [255, 255, 255]]

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/colorsplit.png" alt="Color split" style="width: 640px; height: 480px" /></center>

And then, replace every color by it's supposed original color.

    colorTable = [[  0,   0,   0],
                  [ 40,  36,  33],
                  [ 41,  71, 105],
                  [ 69, 108, 151],
                  [ 92, 145, 199],
                  [171, 195, 181],
                  [209, 226, 220],
                  [255, 255, 255]]

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/recoloring.png" alt="Manual color recontruction" style="width: 640px; height: 480px" /></center>

It's also possible to automatically reconstruct the original colors if you have the original color palette. 

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/color-reconstruction.png" alt="Automatic color recontruction" style="width: 640px; height: 480px" /></center>

<center><img src="https://raw.github.com/hipersayanX/ColorScale/master/images/wrong-color-reconstruction.png" alt="Wrong color recontruction" style="width: 640px; height: 480px" /></center>

Content attribution
===================

[1](http://www.flickr.com/photos/kallu/3394931515/ "Japan'09")
[2](http://www.flickr.com/photos/eelssej_/430902088/ "the musical geisha")
[3](http://www.flickr.com/photos/freedomiiphotography/8190848576/ "Daisho in Temple, Miyajima, Japan")
[4](http://www.flickr.com/photos/osakajock/230790571/ "Geisha")
[5](http://www.flickr.com/photos/demawo/6010502526/ "A small shrine (若宮八幡社) in Toyota south, Aichi, Japan (HDR)... JTM Photo No.69")
[6](http://www.flickr.com/photos/gonmi/6195695770/ "Japan, 2011")
[7](http://www.flickr.com/photos/stevier/3171901675/ "Stew Bento Lunch - Stevie")
[8](http://www.flickr.com/photos/moriyoshi/5165504/ "Tokyo tower.")
[9](http://www.flickr.com/photos/70626035@N00/7106560853/ "Sakura * Prunus serrulata")
