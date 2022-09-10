# -*- coding: UTF-8 -*-

from imgfactory import ImgFactory

# init
factory = ImgFactory( (248, 682), (200, 200) )

# show all the img name in folder "bg"
print( factory.listDir("/data/irene_bgs") )

# get the font object
font1 = factory.getFont("fonts/WCL-01.ttf", 50)
font2 = factory.getFont("fonts/WCL-02.ttf", 40)
font3 = factory.getFont("fonts/Pacifico.ttf", 50)

# get the domain color of bg and fg
bgDomain = factory.getDomainColor("/data/irene_bgs/b001.png")
fgDomain = factory.getDomainColor("/data/prod_imgs_nb/1997134.png")
dctDomain = factory.getDomainColor("/data/irene_dcts/bubble-d-01.png")
print(bgDomain, fgDomain, dctDomain)

# generate numpy array of bg, fg and dct
bg = factory.readBg("/data/irene_bgs/b001.png")
print(bg.shape)
fg = factory.readFg("/data/prod_imgs_nb/1997134.png")
fg3ch = factory.bgra2Bgr(fg)
fg1ch = factory.bgra2Gray(fg)
print(fg.shape, fg3ch.shape, fg1ch.shape)
dct = factory.readDct("/data/irene_dcts/bubble-d-01.png")
print(dct.shape)

# change the color of bg according to fg
renderedBg = factory.renderImg(bg, bgDomain, fgDomain, 0)

# conbine the segments and add text
testImg = factory.combineImg(renderedBg, dct, fg, 0., -0.6)
testImg = factory.addText(testImg, "包包出清特價", font1, (0., 0.3, 0.), -0.8, -0.1)
testImg = factory.addText(testImg, "買一送一", font2, (0., 0.3, 0.), -0.2, 0.1)
testImg = factory.addText(testImg, "$300", font3, (0., 0.3, 0.), 0.1, 0.4)

# diff color demo
bgs = []
dcts = []
rgbs = []
for c in range(5):
    bgs.append( factory.renderImg(bg, bgDomain, fgDomain, c) )
    dcts.append( factory.renderImg(dct, dctDomain, fgDomain, c) )
    rgbs.append( factory.renderRGB(fgDomain, c) )
styleDicts = [
    {"bg": 0, "dct": 1, "text": 3},
    {"bg": 0, "dct": 2, "text": 3},
    {"bg": 1, "dct": 0, "text": 4},
    {"bg": 1, "dct": 2, "text": 4}]
for idx, styleDict in enumerate(styleDicts):
    tmpImg = factory.combineImg(bgs[ styleDict["bg"] ], dcts[ styleDict["dct"] ], fg, 0., -0.6)
    tmpImg = factory.addText(tmpImg, "Best Bag Forever", font3, rgbs[ styleDict["text"] ], -0.3, -0.1)
    factory.dumpImg(tmpImg, "/web/public/images/colormap" + str(idx + 1) + ".png")

# dump to file
factory.dumpImg(factory.resizeImg( testImg, (40, 95) ), "/web/public/images/tmp2.png")

# test only font
factory = ImgFactory( (248, 682), (200, 200) )
fg = factory.readFg("/data/prod_imgs_nb/1997134.png")
bg = factory.readBg("/data/irene_bgs/b001.png")
dct = factory.readDct("/data/irene_dcts/bubble-d-01.png")
img = factory.combineImg(bg, dct, fg, 0., -0.6)
font = factory.getFont("fonts/Pacifico.ttf", 50)
tmp = factory.getTextImg("Best Beg Forever", font, (0., 0.2, 0.8))
img = factory.addTextImg(img, tmp, 0, 0.3)
factory.dumpImg(img, "/web/public/images/font.png")

