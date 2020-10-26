import os
import misc
import argparse
from PIL import Image, ImageFilter


def blur_images(images, percentage, new_dir="output/Images"):
    for index in range(len(images)):
        image = images[index]
        basename = os.path.basename(image)
        parent_path = os.path.basename(os.path.dirname(image))
        img = Image.open(image)
        new_img = img.filter(ImageFilter.GaussianBlur(min(img.size) * percentage))
        directory = os.path.join(new_dir, parent_path)
        misc.prepareDirectory(directory)
        new_img.save(os.path.join(directory, basename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Blur Images")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("-n", "--percentage", dest="percentage", default=0.01, type=float)
    parser.add_argument("-o", "--output_directory", dest="output_directory", default='CUB_200_2011/images (blur)')
    parser.add_argument("directory", default="CUB_200_2011/images (original)")

    args = parser.parse_args()
    images = misc.getAllFiles(args.directory, ['.jpg', '.png', '.tiff', '.gif'])
    blur_images(images, args.percentage, args.output_directory)
