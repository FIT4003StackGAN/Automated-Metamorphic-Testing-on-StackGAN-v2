import numpy as np
from PIL import Image
import argparse
import misc
import os

def turnColor(image, color):
    img = image.convert("HSV");
    width, height = image.size
    for i in range(width):
        for j in range(height):
            pix = img.getpixel((i,j))
            img.putpixel((i,j), (color, pix[1], pix[2]))
    _,a = image.convert("LA").split()
    r,g,b = img.convert("RGB").split()
    return Image.merge("RGBA", (r,g,b,a))

def turnGrey(image, level):
    img = image.convert("L");
    width, height = image.size
    for i in range(width):
        for j in range(height):
            pix = img.getpixel((i,j))
            img.putpixel((i,j), (pix + level))
    _,a = image.convert("LA").split()
    r,g,b = img.convert("RGB").split()
    return Image.merge("RGBA", (r,g,b,a))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Change color of a image")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-H", "--hue", dest="hue", type=int, default= -1)
    group.add_argument("-G", "--grey", dest="grey", type=int, default= 10)
    parser.add_argument("image", type=str)
    parser.add_argument("-o","--output_directory", type=str, default=None)

    args = parser.parse_args()
    image = Image.open(args.image)

    if args.hue > -1:
        new_img = turnColor(image, args.hue)
    else:
        new_img = turnGrey(image, args.grey)

    if args.output_directory: 
        misc.prepareDirectory(args.output_directory)
        imagename = os.path.basename(args.image)
        new_img.save(os.path.join(args.output_directory, imagename))
    else:
        new_img.show()

    print("Change and saved")
    
    
