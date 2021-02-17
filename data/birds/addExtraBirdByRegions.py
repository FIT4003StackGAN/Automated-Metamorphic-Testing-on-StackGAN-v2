from PIL import Image
import random
import misc
import json
import os
import re
import argparse

def checkOverlapping(box, position):
	if position[0] < box[2] and position[0] > box[0] and position[1] < box[-1] and position[-1] > box[1]:
		return True
	return False

def get_insert_position(spaces, size, overlapping=False):
	#print(spaces)
	if overlapping:
		space = [spaces[0][0][2], spaces[2][0][-1], spaces[1][0][0]-size[0], spaces[-1][0][1]-size[1]]
		space[2] = space[0] if space[0] > space[2] else space[2]
		space[-1] = space[1] if space[1] > space[-1] else space[-1] 
		x = random.randint(space[0], space[2])
		y = random.randint(space[1], space[-1])

	else:
		available_space = filter(lambda x: x[0][2] - x[0][0] >= size[0] and x[0][3] - x[0][1] >= size[1], spaces)
		if len(available_space) > 0:
			space = random.choice(available_space)
		else:
			lengths = [0 for x in range(len(spaces))]
			lengths[0] = abs(spaces[0][0][0] - spaces[0][0][2])
			lengths[1] = abs(spaces[1][0][0] - spaces[1][0][2])
			lengths[2] = abs(spaces[2][0][1] - spaces[2][0][-1])
			lengths[-1] = abs(spaces[-1][0][1] - spaces[-1][0][-1])
			max_length = max(lengths)
			spaces_index = [x for x in range(len(spaces))]
			spaces_index = filter(lambda x: lengths[x] == max_length, spaces_index)
			spaces = filter(lambda x: spaces.index(x) in spaces_index, spaces)

			space = random.choice(spaces)
		#print(space)

		if space[0][2] - space[0][0] < size[0]:
			x = space[0][2] - size[0] if space[1] == 'left' else space[0][0]
		else:
			xmin = space[0][0]
			xmax = space[0][2] - size[0]

			x = random.randint(xmin, xmax)

		if space[0][3] - space[0][1] < size[1]:
			y = space[0][-1] - size[1] if space[1] == 'top' else space[0][1]
		else:
			ymin = space[0][1]
			ymax = space[0][3] - size[1]
			
			y = random.randint(ymin, ymax)

	return(x, y, x+size[0], y+size[1])

def countExtraSpace(xmin,xmax,need_length):
	space = abs(xmin - xmax) - need_length
	space = 0 if space < 0  else space
	return space

def get_free_spaces_from_bbox(detected_data, bbox=None, region=(0,0), size=(60,60)):
	#if bbox:
	#	bbox = misc.bbox_position(bbox, (detected_data['image_w'], detected_data['image_h']))
	if not bbox:
		bbox = [0, 0, detected_data['image_w'], detected_data['image_h']]

	padding = [x for x in region]

	dbox = [detected_data['left']-padding[0], 
		detected_data['top'] - padding[1], 
		detected_data['right'] - padding[0], 
		detected_data['bottom'] - padding[1]]

	if len(filter(lambda x: x > 5, dbox)) == 0 and padding[0]-size[0] >= 0 and padding[1]-size[1] >= 0:

		padding[0] -= size[0]
		padding[1] -= size[1]

		dbox[0] += size[0]
		dbox[1] += size[1]
		dbox[2] += size[0]
		dbox[-1] += size[1]

	dbox[2] = detected_data['image_w'] - dbox[2]
	dbox[-1] = detected_data['image_h'] - dbox[-1]

	#print(bbox)
		
	xmin = bbox[0] if bbox[0] > dbox[0] and bbox[0] < dbox[2]  else dbox[0]
	xmax = bbox[2] if bbox[2] < dbox[2] and bbox[2] > dbox[0] else dbox[2]
	ymin = bbox[1] if bbox[1] > dbox[1] and bbox[1] < dbox[-1] else dbox[1]
	ymax = bbox[-1] if bbox[-1] < dbox[-1] and bbox[-1] > dbox[1] else dbox[-1]

	'''
	left = ([bbox[0]+countExtraSpace(bbox[0],xmin,size[0]),
		ymin - size[1], xmin, ymax + size[1]], 'left')
	right = ([xmax, ymin - size[1],
		bbox[2]-countExtraSpace(xmax,bbox[2],size[0]),
		ymax + size[1]], 'right')
	top = ([xmin - size[0], bbox[1]+countExtraSpace(bbox[1],ymin,size[1]),
		xmax + size[0], ymin], 'top')
	bottom = ([xmin - size[0], ymax, xmax + size[0], 
		bbox[-1]-countExtraSpace(ymax, bbox[-1], size[1])],'bottom')
	'''
	left = ([bbox[0]+countExtraSpace(bbox[0],xmin,size[0]),
		ymin, xmin, ymax], 'left')
	right = ([xmax, ymin,
		bbox[2]-countExtraSpace(xmax,bbox[2],size[0]),
		ymax], 'right')
	top = ([xmin, bbox[1]+countExtraSpace(bbox[1],ymin,size[1]),
		xmax, ymin], 'top')
	bottom = ([xmin, ymax, xmax, 
		bbox[-1]-countExtraSpace(ymax, bbox[-1], size[1])],'bottom')

	#print(left, right, top, bottom)

	return [left, right, top, bottom]

def prepare_extrabird(extrabirds, size, image_size, position):
	extrabird = random.choice(extrabirds)
	bird_image = Image.open(extrabird).convert("RGBA").resize(size)
	background = Image.new("RGBA", image_size, (255,255,255, 0))
	background.paste(bird_image, position)

	return background


def insert_extrabird(image, extrabirds, size, detected_data, bbox=None, regions=(0, 0), record=None, overlapping=False):
	image = image.convert("RGBA")
	size = (size[0], size[1])
	spaces = get_free_spaces_from_bbox(detected_data, bbox, regions, size)
	if not record:
		position = get_insert_position(spaces, size, overlapping)
	else:
		position = record['data'][0]
		#print(position)
		position = [position[0], position[1], position[0]+size[0], position[1]+size[1]]
	if record != None:
		record['data'] = tuple([(position[0], position[1])])
	extra_image = prepare_extrabird(extrabirds,size,image.size,position)
	return Image.alpha_composite(image, extra_image).convert("RGB")


def load_arguments():
	parser = argparse.ArgumentParser(prog='Add extra bird on regions')
	parser.add_argument('imagespath', default="CUB_200_2011/images")
	parser.add_argument('-e', dest='extra_images', default="extra_birds")
	parser.add_argument('-d', dest="detected_jsonfile", default=None) #"detected_log.json"
	parser.add_argument('-b', dest="bbox_file", default=None) #"CUB_200_2011/bounding_boxes.txt"
	parser.add_argument('-i', dest="imagename_file", default=None) #"CUB_200_2011/images.txt"
	parser.add_argument('-r', dest="regions", type=int, default=1)
	parser.add_argument('-R', dest="record", default=None)
	parser.add_argument('-o', dest="output_directory", default="output")
	parser.add_argument('-s', dest="size", nargs='+', default=(60,60), type=int)
	parser.add_argument('-p', dest="percentage", type=float, default=1)
	parser.add_argument('-P', dest="overlapping_percent", type=float, default=0)

	args = parser.parse_args()
	return args

if __name__ == "__main__":
	args = load_arguments()
	file_format = ['.jpg', '.png', '.gif']
	images = misc.getAllFiles(args.imagespath, file_format)
	if args.percentage < 1 or args.overlapping_percent > 0:
		random.shuffle(images)
	extra_images = misc.getAllFiles(args.extra_images, file_format)
	required_bbox = False
	images_bbox = None
	detected_datas = None
	if args.bbox_file and args.imagename_file:
		images_bbox = misc.load_bbox(args.bbox_file, args.imagename_file)
		required_bbox = True
	if args.detected_jsonfile:
		detected_datas = misc.load_json_data(args.detected_jsonfile)
	num_modifying_image = int(args.percentage * len(images))
	if detected_datas and len(detected_datas) < num_modifying_image:
		num_modifying_image = len(detected_datas)
	num_overlapping = int(args.overlapping_percent*len(images))
	if detected_datas and len(detected_datas) < num_overlapping:
		num_overlapping = len(detected_datas)
	regions_no = args.regions - 1
	regions = (args.size[0]*regions_no, args.size[1]*regions_no)
	record_filename = None
	full_record = dict()
	if args.record:
		if os.path.isfile(args.record):
			full_record = misc.readRecord(args.record)

		record_filename = args.record

	require_num = num_modifying_image - misc.countRecord(full_record)  
	require_num = 0 if require_num < 0 else require_num
	modified_num = 0
	overlapped = 0

	for i in range(len(images)):
		image = images[i]
		imagename = os.path.basename(image)
		bbox = images_bbox[imagename] if required_bbox and imagename in images_bbox else None
		detected_data = filter(lambda x: os.path.basename(x['path']) == imagename, detected_datas) if detected_datas else None
		detected_data = detected_data[0] if detected_data and len(detected_data) > 0 else None
		classname = os.path.basename(os.path.dirname(image))
		directory = os.path.join(args.output_directory, classname)
		misc.prepareDirectory(directory)
		cls_record = None
		record = None
		cls_number = re.match(r"^([0-9]+)\.\w+$", classname)
		image_number = re.match(r"^.*_([0-9]+)_.*$", imagename)
		#if bbox and detected_data and cls_number and image_number:
		if (detected_data or bbox) and cls_number and image_number:
			cls_number = cls_number.groups()[0]
			image_number = image_number.groups()[0]
			if cls_number in full_record:
				cls_record = full_record[cls_number]
			elif require_num > modified_num:
				cls_record = dict()
				full_record[cls_number] = cls_record

			if cls_record != None and image_number in cls_record:
				record = cls_record[image_number]
			elif cls_record != None and require_num > modified_num:
				record = dict()
				cls_record[image_number] = record

		img = Image.open(image).convert("RGB")

		if record != None and modified_num < num_modifying_image:
			if bbox:
				bbox = misc.bbox_position(bbox, img.size)

				if not detected_data:
					detected_data = dict()
					detected_data['image_w'] = img.size[0]
					detected_data['image_h'] = img.size[1]
					detected_data['left'] = bbox[0]
					detected_data['top'] = bbox[1]
					detected_data['right'] = img.size[0] - bbox[2]
					detected_data['bottom'] = img.size[1] - bbox[-1]

					bbox = None

					#print(detected_data)

			if overlapped < num_overlapping:
				if detected_data and bbox:
					new_image = insert_extrabird(img, extra_images, args.size, detected_data, bbox, regions, record, True)
				else:
					new_image = insert_extrabird(img, extra_images, args.size, detected_data, None, regions, record, True)
				overlapped += 1
			else:
				if detected_data and bbox:
					new_image = insert_extrabird(img, extra_images, args.size, detected_data, bbox, regions, record)
				else:
					new_image = insert_extrabird(img, extra_images, args.size, detected_data, None, regions, record)
			#print(record)
			if 'data' in record:
				record['filename'] = os.path.join(classname, imagename)
				#cls_record[image_number] = record
				new_image.save(os.path.join(directory, imagename))
				modified_num += 1
			else:
				img.save(os.path.join(directory, imagename))

		else:
			img.save(os.path.join(directory, imagename))

	if record_filename:
		misc.writeRecord(record_filename, full_record)
	print("total number of modified image: %d"%modified_num)
	print("total number of overlapping insertion: %d"%overlapped)


























