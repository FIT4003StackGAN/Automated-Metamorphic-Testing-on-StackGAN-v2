from __future__ import division

import os
import misc
import argparse
import random
from PIL import Image

def prepare_tree(base_size, images, position=None, max_tree=3, ratio=5):
    bigger_index  = 0 if base_size[0] > base_size[1] else 1
    big = base_size[bigger_index]
    small = base_size[(bigger_index+1)%2]
    smaller_ratio = round((small/big)*ratio)
    base_ratio = ratio
    while smaller_ratio < base_ratio:
        ratio+=1
        smaller_ratio = round((small/big)*ratio)
    size_ratio = [0,0]
    size_ratio[bigger_index] = ratio
    size_ratio[(bigger_index+1)%2] = smaller_ratio

    middle_space = ((size_ratio[0]-base_ratio)//4)*2+3 if size_ratio[0]%2 > 0 else ((size_ratio[0]-base_ratio-1)//4)*2+2
    extra_space = (size_ratio[0] - middle_space)//2

    image = Image.new("RGBA", base_size, (255,255,255, 0))
    for i in range(random.randint(1,max_tree)):
        tree_image = images[random.randint(0, len(images)-1)]
        tree_image = Image.open(tree_image).convert("RGBA")
        tree_size = tree_image.size
        best_width = (base_size[1]/tree_size[1]) * tree_size[0]
        tree_image = tree_image.resize((int(round(best_width)), base_size[1]))

        if position == None:
            position_ratio = [0,0]
            position_ratio[0] = random.randint(1, size_ratio[0]-1) 
            position_ratio[1] = random.randint(0, size_ratio[1]//2)
            #print(position_ratio)
            if position_ratio[0] > extra_space and position_ratio[0] < size_ratio[0]-extra_space:
                position_ratio[0] = random.randint(1, extra_space) if position_ratio[0] %2 > 0 else random.randint(size_ratio[0]-extra_space, size_ratio[0]-1)
            #if size_ratio[0] % 2 == 0 and (size_ratio[0]//2 - position_ratio[0]) < 2:
            #    position_ratio[0] += -1 if position_ratio[0] != size_ratio[0]//2 else 1
            #elif size_ratio[0] % 2 != 0 and (size_ratio[0]//2 - position_ratio[0]) == 0:
            #    position_ratio[0] += -1 if position_ratio[0]%2 == 0 else 1
            tree_position = (int(round(base_size[0]*(position_ratio[0]/size_ratio[0]))), int(round(base_size[1]*(position_ratio[1]/size_ratio[1]))))
        else:
            tree_position = position
        if position_ratio[0] < size_ratio[0]//2:
            box = (tree_position[0] - tree_image.size[0], tree_position[1], tree_position[0], tree_position[1]+tree_image.size[1])
        else:
            box = (tree_position[0], tree_position[1], tree_position[0]+tree_image.size[0], tree_position[1]+tree_image.size[1])
        png_image = Image.new("RGBA", base_size, (255,255,255, 0)) 
        png_image.paste(tree_image, box)
        image = Image.alpha_composite(image, png_image)
    return image

def place_extratrees(image, extra_images, position=None, max_tree=3):
    img = image.convert("RGBA")
    size = img.size
    extra_img = prepare_tree(size, extra_images, position, max_tree)
    new_img = Image.alpha_composite(img, extra_img).convert("RGB")
    return new_img


def modify_images(images, modify_func, new_dir="output/Images", percentage=1, *args, **kwds):
    random.shuffle(images)
    num = int(len(images)*percentage)
    for index in range(len(images)):
        image = images[index]
        basename  = os.path.basename(image)
        parentPath = os.path.basename(os.path.dirname(image))
        img = Image.open(image)
        if index < num:
            new_img = modify_func(img, *args, **kwds)
        else:
            new_img = img
        directory = os.path.dirname(image) if new_dir == None else os.path.join(new_dir, parentPath)
        misc.prepareDirectory(directory)
        new_img.save(os.path.join(directory, basename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Add Extra Bird")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--position", dest="position", type=(lambda x: tuple(x.split(','))),
                        default=('10','10'))
    group.add_argument("-r", "--random", dest="random_position", action="store_true", default=False)
    parser.add_argument("-d", "--extra_directory", dest="extra_directory", default='extra_trees')
    parser.add_argument("-n", "--num_trees", dest="num_trees", default=3, type=int)
    parser.add_argument("--percentage", dest="percentage", default= 1, type=float)
    parser.add_argument("-o", "--output_directory", dest="output_directory", default='output/Images')
    parser.add_argument("directory")

    args = parser.parse_args()
    position = tuple(map(lambda x: int(x),args.position)) if not args.random_position else None
    images = misc.getAllFiles(args.directory, ['.jpg', '.png', '.tiff', '.gif'])
    bird_images = misc.getAllFiles(args.extra_directory, ['.jpg', '.png', '.tiff', '.gif'])
    modify_images(images, place_extratrees, args.output_directory, args.percentage, bird_images, position, args.num_trees)

    
    
    
