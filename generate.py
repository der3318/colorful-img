# -*- coding: UTF-8 -*-

import argparse
import os
import PIL
from imgfactory import ImgFactory

if __name__ == "__main__":

    # read input from command line arg
    parser = argparse.ArgumentParser(description = "Colorful Image Generation Script", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("filepath", help = "Filepath of the Input Image")
    args = parser.parse_args()

    # read image and create factory
    w, h = PIL.Image.open(args.filepath).size
    factory = ImgFactory((h, w), (h, w))
    image = factory.readBg(args.filepath)

    # dump different color style
    path, extension = os.path.splitext(args.filepath)
    for style in range(1, 14):
        rendered = factory.renderImg(image, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), style)
        output = "{}.style{:02d}{}".format(path, style, extension)
        factory.dumpImg(rendered, output)
        print(output)

