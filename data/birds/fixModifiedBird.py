import os
import argparse
import misc
from addExtraBird import place_extrabird
from PIL import Image



def fixImages(source, output_directory, image_func, records, classcode, file_indices, *args, **kwds):
    if not records.has_key(classcode):
        print("Cannot find class start with %s from record"%(classcode))
        return
    
    category = records[classcode]
    for file_num in file_indices:
        if not file_num in category:
            continue
        filename = category[file_num]['filename']
        exact_path = os.path.join(os.path.abspath(source),filename)
        image = Image.open(exact_path)
        data = place_extrabird(image, *args, **kwds)
        if type(data) == tuple:
            new_img = data[0]
            category[file_num]['data'] = tuple(data[1:])
        else:
            new_img = data

        output_path = os.path.join(os.path.abspath(output_directory),filename)
        new_img.save(output_path)
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Fix modified Images")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--position", dest="position", type=(lambda x: tuple(x.split(','))),
        default=('10','10'))
    group.add_argument("-r", "--random", dest="random_position", action="store_true", default=False)
    parser.add_argument("directory")
    parser.add_argument("-C", "--classcode", required=True)
    parser.add_argument("-d", "--extra_directory", dest="extra_directory", default='extra_birds')
    parser.add_argument("-o", "--output_directory", dest="output_directory", default='output')
    parser.add_argument("-I", "--images", nargs='+', required=True)
    parser.add_argument("-R", "--record", dest="record", default="SavedRecord.txt")

    args = parser.parse_args()
    position = tuple(map(lambda x: int(x),args.position)) if not args.random_position else None
    bird_images = misc.getAllFiles(args.extra_directory, ['.jpg', '.png', '.tiff', '.gif'])
    records = misc.readRecord(args.record)

    records = fixImages(args.directory, args.output_directory, place_extrabird, 
        records, args.classcode, args.images, bird_images, position)
    misc.writeRecord(args.record, records)
        
        
    
