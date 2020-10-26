from __future__ import division

import os
import misc
import argparse
import random
import re
from PIL import Image, ImageDraw, ImageFont

def findGCD(dividend, divisor):
    remainder = dividend % divisor
    if remainder == 0:
        return divisor
    return findGCD(divisor, remainder)

def prepare_extra_bird(base_size, images, position=None, ratio=3):
    bird_image = images[random.randint(0, len(images)-1)]
    bird_image = Image.open(bird_image).convert("RGBA")
    bigger_index  = 0 if base_size[0] > base_size[1] else 1
    big = base_size[bigger_index]
    small = base_size[(bigger_index+1)%2]
    gcd = findGCD(big, small)
    big = big // gcd
    small = small // gcd
    smaller_ratio = round((small/big)*ratio)
    base_ratio = ratio
    while smaller_ratio < base_ratio:
        ratio+=1
        smaller_ratio = round((small/big)*ratio)
        #print(smaller_ratio)
    size_ratio = [0,0]
    size_ratio[bigger_index] = ratio
    size_ratio[(bigger_index+1)%2] = smaller_ratio
    bird_image = bird_image.resize((int(round(base_size[0]/size_ratio[0])),
        int(round(base_size[1]/size_ratio[1]))))

    if position == None:
        position_ratio = [0,0]
        position_ratio[0] = random.randint(0, size_ratio[0]-1) 
        position_ratio[1] = random.randint(0, size_ratio[1]-1)

        if (size_ratio[0]+1)%2==0 and position_ratio[0] == size_ratio[0]//2:
            position_ratio[0] += (1 if random.randint(0,1) == 1 else -1)
        elif size_ratio[0]%2==0 and (position_ratio[0] == size_ratio[0]//2 or position_ratio[0] == (size_ratio[0]-1)//2):
            position_ratio[0] += (-0.5 if position_ratio[0] == (size_ratio[0]-1)//2 else 0.5)

        if position_ratio[0] > 0 and position_ratio[0] < size_ratio[0]-1:
            position_ratio[1] = 0 if position_ratio[1]%2 == 0 else size_ratio[1]-1
        elif (size_ratio[1]+1)%2==0 and position_ratio[1] == size_ratio[1]//2:
            position_ratio[1] += (1 if random.randint(0,1) == 1 else -1)
        elif size_ratio[1]%2==0 and (position_ratio[1] == size_ratio[1]//2 or position_ratio[1] == (size_ratio[1]-1)//2):
            position_ratio[1] += (-0.5 if position_ratio[1] == (size_ratio[1]-1)//2 else 0.5)

        position = (int(round(base_size[0]*(position_ratio[0]/size_ratio[0]))), int(round(base_size[1]*(position_ratio[1]/size_ratio[1]))))
    box = (position[0], position[1], position[0]+bird_image.size[0], position[1]+bird_image.size[1])
    image = Image.new("RGBA", base_size, (255,255,255, 0))
    image.paste( bird_image, box)
    return image, tuple(position)

def place_extrabird(image, extra_images, position=None):
    image = image.convert("RGBA")
    size = image.size
    extra_img, position = prepare_extra_bird(size, extra_images, position)
    new_img = Image.alpha_composite(image, extra_img).convert("RGB")
    return new_img, position

def modify_images( images, modify_func, new_dir="output/Images", percentage=1, records=None, *args, **kwds):
    if records == None:
        records = dict()
    classregex = r"^[0-9]+"
    fileregex = r"([0-9]+).*$"
    random.shuffle(images)
    num = int(len(images)*percentage)
    for index in range(len(images)):
        image = images[index]
        basename  = os.path.basename(image)
        parentPath = os.path.basename(os.path.dirname(image))

        classcode = re.search(classregex, parentPath)
        if classcode:
            classcode = classcode.group()
            if classcode in records:
                category_record = records[classcode]
            else:
                category_record = dict()
                records[classcode] = category_record
        else:
            category_record = None

        adjusted_args = list(args)
        img = Image.open(image)
        if index < num:
            file_index = re.search(fileregex, basename)
            if file_index and len(file_index.groups()) > 0:
                file_index = file_index.groups()[0]
            else:
                file_index = None

            if category_record !=None and file_index and file_index in category_record:
                arguments = category_record[file_index]['data']
                num_replace = 0
                for i in range(len(adjusted_args)):
                    if adjusted_args[i] == None and num_replace < len(arguments):
                        adjusted_args[i] = arguments[num_replace]
                        num_replace += 1
                    if num_replace >= len(arguments):
                        break

            data = modify_func(img, *adjusted_args, **kwds)

            if type(data) == tuple:
                new_img = data[0]
                if category_record != None and file_index:
                    save_data = dict()
                    save_data['filename'] = os.path.join(parentPath, basename)
                    data = tuple(data[1:])
                    save_data['data'] = data
                    category_record[file_index] = save_data
            else:
                new_img = data
        else:
            new_img = img

        directory = os.path.dirname(image) if new_dir == None else os.path.join(new_dir, parentPath)
        misc.prepareDirectory(directory)
        new_img.save(os.path.join(directory, basename))
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Add Extra Bird")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--position", dest="position", type=(lambda x: tuple(x.split(','))),
        default=('10','10'))
    group.add_argument("-r", "--random", dest="random_position", action="store_true", default=False)
    parser.add_argument("-d", "--extra_directory", dest="extra_directory", default='extra_birds')
    parser.add_argument("-n", "--percentage", dest="percentage", default= 1, type=float)
    parser.add_argument("-o", "--output_directory", dest="output_directory", default='output/Images')
    parser.add_argument("-R", "--record", dest="record", default=None)
    parser.add_argument("directory", default="CUB_200_2011/images")

    args = parser.parse_args()
    position = tuple(map(lambda x: int(x),args.position)) if not args.random_position else None
    images = misc.getAllFiles(args.directory, ['.jpg', '.png', '.tiff', '.gif'])
    bird_images = misc.getAllFiles(args.extra_directory, ['.jpg', '.png', '.tiff', '.gif'])
    if args.record != None:
        records = misc.readRecord(args.record)
    else:
        args.record = "SavedRecord.txt"
        records = None

    records = modify_images(images, place_extrabird, args.output_directory, args.percentage, records, bird_images, position)
    misc.writeRecord(args.record, records)

    
    
    
