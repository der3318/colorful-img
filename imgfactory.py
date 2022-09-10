# -*- coding: UTF-8 -*-

import os
import re
import colorsys
import numpy as np
import cv2
from colorthief import ColorThief
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import matplotlib

class ImgFactory:

    def __init__(self, _bgDim, _fgDim):
        """
        Parameters
        ----------
        _bgDim: tuple (row, col)
            Background dimension, (248, 682) in general
        _fgDim: tuple (row, col)
            Foreground/Item dimension, (200, 200) in general
        Returns
        ----------
        None
        """
        self.bgDim = _bgDim
        self.fgDim = _fgDim

    def listDir(self, _dirPath):
        """
        Parameters
        ----------
        _dirPath: string
            Path of the directory
        Returns
        ----------
        List
            Containing the paths of the png-images in the directory
        """
        imgList = []
        for pngFile in os.listdir(_dirPath):
            if not re.match(".*\.png", pngFile):    continue
            imgList.append( os.path.join(_dirPath, pngFile) )
        return imgList

    def getFont(self, _ttfPath, _size):
        """
        Parameters
        ----------
        _ttfPath: string
            Path of the ttfFile
        _size: int
            Font size
        Returns
        ----------
        ImageFont object
            The corresponding ImageFont object
        """
        return ImageFont.truetype(os.path.join(_ttfPath), _size)

    def getDomainColor(self, _imgPath):
        """
        Parameters
        ----------
        _imgPath: string
            Path of the image
        Returns
        ----------
        3-elemented tuple
            Indicating (r, g, b), from 0.0 to 1.0
        """
        r, g, b = ColorThief(_imgPath).get_color(quality = 1)
        return (r / 255, g / 255, b / 255)

    def dumpImg(self, _imgArr, _outputPath):
        """
        Parameters
        ----------
        _imgArr: numpy array
            Pixel values of the image, from 0.0 to 1.0
        _outputPath: string
            Prefered path of the ouptut file
        Returns
        ----------
        None
        """
        cv2.imwrite(_outputPath, _imgArr * 255)

    def readBg(self, _bgPath):
        """
        Parameters
        ----------
        _bgPath: string
            Path of the background file
        Returns
        ----------
        Numpy array
            The pixel values of the bg, with shape (self.bgDim[0], self.bgDim[1], 4) and value from 0.0 to 1.0
        """
        bg = cv2.resize(cv2.imread(_bgPath, -1), (self.bgDim[1], self.bgDim[0]), interpolation = cv2.INTER_CUBIC) / 255
        if bg.shape[2] < 4:
            newBg = np.ones([bg.shape[0], bg.shape[1], 4])
            newBg[:, :, :3] = bg[:, :, :3]
            bg = newBg
        else:
            white = np.ones([bg.shape[0], bg.shape[1], 3])
            bg[:, :, :3] = bg[:, :, :3] * bg[ :, :, [3] ] + white * (1 - bg[ :, :, [3] ])
            bg[:, :, 3] = 1.
        bg[:, :, :3] = np.clip(bg[:, :, :3] * 1.1, 0.0, 1.0)
        return bg

    def readFg(self, _fgPath):
        """
        Parameters
        ----------
        _fgPath: string
            Path of the foreground/item file
        Returns
        ----------
        Numpy array
            The pixel values of the fg, with shape (self.fgDim[0], self.fgDim[1], 4) and value from 0.0 to 1.0
        """
        fg = cv2.resize(cv2.imread(_fgPath, -1), (self.fgDim[1], self.fgDim[0]), interpolation = cv2.INTER_CUBIC) / 255
        fg = fg.reshape(fg.shape[0], fg.shape[1], -1)
        if fg.shape[2] < 4:
            newFg = np.ones([fg.shape[0], fg.shape[1], 4])
            newFg[:, :, :3] = fg[:, :, :3]
            fg = newFg
        else:
            white = np.ones([fg.shape[0], fg.shape[1], 3])
            fg[:, :, :3] = fg[:, :, :3] * fg[ :, :, [3] ] + white * (1 - fg[ :, :, [3] ])
        fg[:, :, :3] = np.clip(fg[:, :, :3] * 1.05, 0.0, 1.0)
        return fg

    def readDct(self, _dctPath):
        """
        Parameters
        ----------
        _dctPath: string
            Path of the decorator file
        Returns
        ----------
        Numpy array
            The pixel values of the dct, with shape (self.bgDim[0], self.bgDim[1], 4) and value from 0.0 to 1.0
        """
        dct = cv2.resize(cv2.imread(_dctPath, -1), (self.bgDim[1], self.bgDim[0]), interpolation = cv2.INTER_CUBIC) / 255
        if dct.shape[2] < 4:
            newDct = np.ones([dct.shape[0], dct.shape[1], 4])
            newDct[:, :, :3] = dct[:, :, :3]
            dct = newDct
        else:
            white = np.ones([dct.shape[0], dct.shape[1], 3])
            dct[:, :, :3] = dct[:, :, :3] * dct[ :, :, [3] ] + white * (1 - dct[ :, :, [3] ])
        return dct

    def readBanner(self, _bannerPath):
        """
        Parameters
        ----------
        _bannerPath: string
            Path of the banner file
        Returns
        ----------
        Numpy array
            The pixel values of the banner, with shape (?, ?, 4) and value from 0.0 to 1.0
        """
        banner = cv2.resize(cv2.imread(_bannerPath, -1), (self.bgDim[1], self.bgDim[0]), interpolation = cv2.INTER_CUBIC) / 255
        if banner.shape[2] < 4:
            newBanner = np.ones([banner.shape[0], banner.shape[1], 4])
            newBanner[:, :, :3] = banner[:, :, :3]
            banner = newBanner
        else:
            white = np.ones([banner.shape[0], banner.shape[1], 3])
            banner[:, :, :3] = banner[:, :, :3] * banner[ :, :, [3] ] + white * (1 - banner[ :, :, [3] ])
        return banner

    def readIcon(self, _iconPath, _dim):
        """
        Parameters
        ----------
        _iconPath: string
            Path of the icon file
        _dim: tuple (row, col)
            image dimension, (28, 52) in general
        Returns
        ----------
        Numpy array
            The pixel values of the icon, with shape (?, ?, 4) and value from 0.0 to 1.0
        """
        icon = cv2.resize(cv2.imread(_iconPath, -1), (_dim[1], _dim[0]), interpolation = cv2.INTER_CUBIC) / 255
        if icon.shape[2] < 4:
            newIcon = np.ones([icon.shape[0], icon.shape[1], 4])
            newIcon[:, :, :3] = icon[:, :, :3]
            icon = newIcon
        else:
            white = np.ones([icon.shape[0], icon.shape[1], 3])
            icon[:, :, :3] = icon[:, :, :3] * icon[ :, :, [3] ] + white * (1 - icon[ :, :, [3] ])
        return icon

    def combineImg(self, _bg, _dct, _fg, _rowShift, _colShift):
        """
        Parameters
        ----------
        _bg: numpy array
            The pixel values of the background, with shape (self.bgDim[0], self.bgDim[1], 4) and value from 0.0 to 1.0
        _dct: numpy array
            The pixel values of the decorator, with shape (self.bgDim[0], self.bgDim[1], 4) and value from 0.0 to 1.0
        _fg: numpy array
            The pixel values of the foreground/item, with shape (self.fgDim[0], self.fgDim[1], 4) and value from 0.0 to 1.0
        _rowShift: double
            Control the center of the foreground, mapping value [-1, 1] to the top/bottom
        _colShift: double
            Control the center of the foreground, mapping value [-1, 1] to the left/right
        Returns
        ----------
        Numpy array
            The pixel values of the combined img, with shape (self.bgDim[0], self.bgDim[1], 4) and value from 0.0 to 1.0
        """
        img = np.copy(_bg)
        img[:, :, :3] = _dct[:, :, :3] * _dct[ :, :, [3] ] + img[:, :, :3] * (1 - _dct[ :, :, [3] ])
        rowCenter = int( (self.bgDim[0] - 1.) * (_rowShift + 1.) / 2. )
        colCenter = int( (self.bgDim[1] - 1.) * (_colShift + 1.) / 2. )
        (rowMin, rowMax) = ( max(0, rowCenter - self.fgDim[0] // 2), min(rowCenter + self.fgDim[0] // 2, self.bgDim[0] - 1) )
        (colMin, colMax) = ( max(0, colCenter - self.fgDim[1] // 2), min(colCenter + self.fgDim[1] // 2, self.bgDim[1] - 1) )
        deltaRow = rowCenter - self.fgDim[0] // 2
        deltaCol = colCenter - self.fgDim[1] // 2
        fgCrop = _fg[rowMin - deltaRow:rowMax - deltaRow, colMin - deltaCol:colMax - deltaCol, :]
        img[rowMin:rowMax, colMin:colMax, :3] = fgCrop[:, :, :3] * fgCrop[ :, :, [3] ] + img[rowMin:rowMax, colMin:colMax, :3] * (1 - fgCrop[ :, :, [3] ])
        return img

    def renderImg(self, _imgArr, _domainRGB, _targetRGB, _styleID, _highS = False):
        """
        Parameters
        ----------
        _imgArr: numpy array
            The pixel values of the img, with shape (?, ?, 4) and value from 0.0 to 1.0
        _domainRGB: 3-elemented tuple
            Domain color of the input img, represented in (r, g, b), from 0.0 to 1.0
        _targetRGB: 3-elemented tuple
            Target style color, represented in (r, g, b), from 0.0 to 1.0
        _styleID: style index
            0 => targetColor, 1 => analogicA, 2 => analogicB, 3 => diff, 4 => complement
        Returns
        ----------
        Numpy array
            The pixel values of the rendered img, with the same shape and value from 0.0 to 1.0
        """
        domainH, domainS, _ = colorsys.rgb_to_hsv(_domainRGB[0], _domainRGB[1], _domainRGB[2])
        targetH, targetS, targetV = colorsys.rgb_to_hsv(_targetRGB[0], _targetRGB[1], _targetRGB[2])
        deltaH = targetH - domainH
        if deltaH < 0:  deltaH = deltaH + 1
        img = np.copy(_imgArr)
        hsv = matplotlib.colors.rgb_to_hsv(_imgArr[:, :, 2::-1])
        # change h
        hsv[ :, :, [0] ] = hsv[ :, :, [0] ] + (_styleID / 14)
        exceed = (hsv[ :, :, [0] ] > 1.).astype(int)
        hsv[ :, :, [0] ] = hsv[ :, :, [0] ] - exceed
        hsv[ :, :, [0] ] = hsv[ :, :, [0] ] + deltaH
        exceed = (hsv[ :, :, [0] ] > 1.).astype(int)
        hsv[ :, :, [0] ] = hsv[ :, :, [0] ] - exceed
        # change s
        if _highS:
            hsv[ :, :, [1] ] = hsv[ :, :, [1] ] + 0.05
            hsv[ :, :, [1] ] = np.clip(hsv[ :, :, [1] ], 0.0, 1.0)
        # change back
        rgb = matplotlib.colors.hsv_to_rgb(hsv)
        img[:, :, :3] = np.clip(rgb[:, :, 2::-1], 0.0, 1.0)
        return img

    def renderRGB(self, _targetRGB, _styleID):
        """
        Parameters
        ----------
        _targetRGB: 3-elemented tuple
            Target style color, represented in (r, g, b), from 0.0 to 1.0
        _styleID: style index
            0 => targetColor, 1 => analogicA, 2 => analogicB, 3 => diff, 4 => complement
        Returns
        ----------
        3-elemented tuple
            Rendered color, represented in (r, g, b), from 0.0 to 1.0
        """
        h, s, v = colorsys.rgb_to_hsv(_targetRGB[0], _targetRGB[1], _targetRGB[2])
        h = h + (_styleID / 8)
        if h > 1.0:     h = h - 1.
        r1, g1, b1 = colorsys.hsv_to_rgb(h, 0.45, 0.6)
        r2, g2, b2 = colorsys.hsv_to_rgb(h, 0.55, 0.7)
        r3, g3, b3 = colorsys.hsv_to_rgb(h, 0.6, 0.6)
        #return (r * 0.6, g * 0.6, b * 0.6)
        return (r1, g1, b1), (r2 * 0.7, g2 * 0.7, b2 * 0.7), (r3, g3, b3)

    def addText(self, _imgArr, _text, _font, _rgb, _rowShift, _colShift):
        """
        Parameters
        ----------
        _imgArr: numpy array
            The pixel values of the img, with shape (?, ?, 4) and value from 0.0 to 1.0
        _text: string
            Text to be shown on the image
        _font: ImageFont
            The font of the text
        _rgb: 3-elemented tuple
            Text color, represented in (r, g, b), from 0.0 to 1.0
        _rowShift: double
            Where the first letter appears, mapping value [-1, 1] to the top/bottom
        _colShift: double
            Where the first letter appears, mapping value [-1, 1] to the left/right
        Returns
        ----------
        Numpy array
            The pixel values of the img with text, with the same shape and value from 0.0 to 1.0
        """
        pImg = Image.fromarray( np.uint8(_imgArr[:, :, :3] * 255) )
        draw = ImageDraw.Draw(pImg)
        row = int( (_imgArr.shape[0] - 1.) * (_rowShift + 1.) / 2. )
        col = int( (_imgArr.shape[1] - 1.) * (_colShift + 1.) / 2. )
        draw.text( (col, row), _text, ( int(_rgb[2] * 255), int(_rgb[1] * 255), int(_rgb[0] * 255) ), font = _font )
        img = np.copy(_imgArr)
        img[:, :, :3] = np.asarray(pImg)[:, :, :] / 255
        return img

    def bgra2Bgr(self, _imgArr):
        """
        Parameters
        ----------
        _imgArr: numpy array
            The pixel values of the img, with shape (?, ?, 4) and value from 0.0 to 1.0
        Returns
        ----------
        Numpy array
            The pixel values of the 3-channeled img, with shape (?, ?, 3) and value from 0.0 to 1.0
        """
        white = np.ones( [_imgArr.shape[0], _imgArr.shape[1], 3] )
        return _imgArr[:, :, :3] * _imgArr[ :, :, [3] ] + white * (1 - _imgArr[ :, :, [3] ])

    def bgra2Gray(self, _imgArr):
        """
        Parameters
        ----------
        _imgArr: numpy array
            The pixel values of the img, with shape (?, ?, 4) and value from 0.0 to 1.0
        Returns
        ----------
        Numpy array
            The pixel values of the gray-scale img, with shape (?, ?, 1) and value from 0.0 to 1.0
        """
        return (cv2.cvtColor(np.uint8(_imgArr[:, :, :] * 255), cv2.COLOR_BGRA2GRAY) / 255).reshape([-1, _imgArr.shape[1], 1])

    def resizeImg(self, _imgArr, _dim):
        """
        Parameters
        ----------
        _imgArr: numpy array
            The pixel values of the img, with shape (?, ?, ?) and value from 0.0 to 1.0
        _dim: tuple (row, col)
            Output dimension
        Returns
        ----------
        Numpy array
            The pixel values of the resized img, with shape (?, ?, ?) and value from 0.0 to 1.0
        """
        return cv2.resize(np.uint8(_imgArr[:, :, :] * 255), (_dim[1], _dim[0]), interpolation = cv2.INTER_CUBIC) / 255

    def getTextImg(self, _text, _font, _rgb):
        """
        Parameters
        ----------
        _text: string
            Text to be shown on the image
        _font: ImageFont
            The font of the text
        _rgb: 3-elemented tuple
            Text color, represented in (r, g, b), from 0.0 to 0.99...
        Returns
        ----------
        Numpy array
            The pixel values of the img with text, with the same shape and value from 0.0 to 1.0
        """
        pImg = Image.fromarray( np.uint8(np.ones([self.bgDim[0], self.bgDim[1], 3]) * 255) )
        draw = ImageDraw.Draw(pImg)
        draw.text( (5, 5), _text, ( int(_rgb[2] * 255), int(_rgb[1] * 255), int(_rgb[0] * 255) ), font = _font )
        imgArr = np.asarray(pImg)
        exist0 = (imgArr[:, :, 0] < 255).astype(int)
        exist1 = (imgArr[:, :, 1] < 255).astype(int)
        exist2 = (imgArr[:, :, 2] < 255).astype(int)
        exist = ( (exist0 + exist1 + exist2) > 0 ).astype(int)
        rowEnd = np.argmax(np.amax(exist, axis = 1) + np.arange(self.bgDim[0]) /self.bgDim[0]) + 5
        colEnd = np.argmax(np.amax(exist, axis = 0) + np.arange(self.bgDim[1]) /self.bgDim[1]) + 5
        img = np.zeros([rowEnd, colEnd, 4])
        channelA = 1 - np.mean( ( imgArr[:rowEnd, :colEnd, :] / 255 - np.array([ _rgb[2], _rgb[1], _rgb[0] ]) ) ** 2, axis = 2 )
        minChannelA = np.amin(channelA)
        img[:, :, 3] = exist[:rowEnd, :colEnd] * (channelA - minChannelA) / (1 - minChannelA)
        img[:, :, :3] = imgArr[:rowEnd, :colEnd, :] / 255
        return img

    def addTextImg(self, _imgArr, _textArr, _rowShift, _colShift):
        """
        Parameters
        ----------
        _imgArr: numpy array
            The pixel values of the origin img, with shape (?, ?, 4) and value from 0.0 to 1.0
        _textArr: numpy array
            The pixel values of the text img, with shape (?, ?, 4) and value from 0.0 to 1.0
        _rowShift: double
            Where the first letter appears, mapping value [-1, 1] to the top/bottom
        _colShift: double
            Where the first letter appears, mapping value [-1, 1] to the left/right
        Returns
        ----------
        Numpy array
            The pixel values of the img with text, with the same shape and value from 0.0 to 1.0
        """
        img = np.copy(_imgArr)
        rowCenter = int( (_imgArr.shape[0] - 1.) * (_rowShift + 1.) / 2. )
        colCenter = int( (_imgArr.shape[1] - 1.) * (_colShift + 1.) / 2. )
        (rowMin, rowMax) = ( max(0, rowCenter - _textArr.shape[0] // 2), min(rowCenter + _textArr.shape[0] // 2, _imgArr.shape[0] - 1) )
        (colMin, colMax) = ( max(0, colCenter - _textArr.shape[1] // 2), min(colCenter + _textArr.shape[1] // 2, _imgArr.shape[1] - 1) )
        deltaRow = rowCenter - _textArr.shape[0] // 2
        deltaCol = colCenter - _textArr.shape[1] // 2
        textArrCrop = _textArr[rowMin - deltaRow:rowMax - deltaRow, colMin - deltaCol:colMax - deltaCol, :]
        img[rowMin:rowMax, colMin:colMax, :3] = textArrCrop[:, :, :3] * textArrCrop[ :, :, [3] ] + img[rowMin:rowMax, colMin:colMax, :3] * (1 - textArrCrop[ :, :, [3] ])
        return img

    def getFocusedFg(self, _fg):
        """
        Parameters
        ----------
        _fg: numpy array
            The pixel values of the foreground/item, with shape (self.fgDim[0], self.fgDim[1], 4) and value from 0.0 to 1.0
        Returns
        ----------
        Numpy array
            The pixel values of the focused fg, with shape (self.fgDim[0], self.fgDim[1], 4) and value from 0.0 to 1.0
        """
        exist = (_fg[:, :, 3] > 0.).astype(int)
        top = np.sum(exist[:self.fgDim[0] // 2, :])
        bottom = np.sum(exist[self.fgDim[0] // 2:, :])
        colStart = self.fgDim[1] // 8
        colEnd = self.fgDim[1] * 7 // 8
        if top > bottom:
            rowStart = 0
            rowEnd = self.fgDim[0] * 3 // 4
        else:
            rowStart = self.fgDim[0] // 4
            rowEnd = self.fgDim[0]
        fgCrop = _fg[rowStart:rowEnd, colStart:colEnd, :]
        return cv2.resize(np.uint8(fgCrop * 255), (self.fgDim[0], self.fgDim[1]), interpolation = cv2.INTER_CUBIC) / 255

