import os
import stat
import re
from ast import literal_eval

def getAllFiles(path, fileformat = ['.txt']):
    texts = []
    for child in os.listdir(path):
        dirname = os.path.join(path, child)
        name, extension = os.path.splitext(child)
        if extension == '':
            texts.extend(getAllFiles(dirname, fileformat))
        elif extension in fileformat:
            texts.append(dirname)
        else:
            name = [True if char.isdigit() else False for char in name]
            if name.count(True) == len(name):
                texts.extend(getAllFiles(dirname, fileformat))
    
    return texts

def prepareDirectory(path):
    if not os.path.isdir(os.path.abspath(path)):
        os.makedirs(path)

def readRecord(path):
    exact_path = os.path.abspath(path)
    if not os.path.isfile(exact_path):
        print("cannot read record file (%s).\n \
            make sure file is placed inside %s"%(path, os.path.abspath(os.curdir)))
        return None
    os.chmod(exact_path, stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH)

    with open(exact_path, 'r') as record_file:
        lines = record_file.read().split('\n')
        records = dict()
        for line in lines:
            data = line.split('-->')
            if len(data) < 4:
                continue
            regex = r"^[0-9\(\)\{\}\[\]\,\-\.\s]+$"
            classcode = data[0]
            file_index = data[1]
            filename = data[2]
            data = map(lambda value: literal_eval(value) if re.match(regex, value) else value, 
                data[3:])
            if records.has_key(classcode):
                files_data = records[classcode]
                files_data[file_index] = dict()
                files_data[file_index]['filename'] = filename
                files_data[file_index]['data'] = tuple(data)
            else:
                files_data = dict()
                files_data[file_index] = dict()
                files_data[file_index]['filename'] = filename
                files_data[file_index]['data'] = tuple(data)
                records[classcode] = files_data

        return records

def writeRecord(path, records):
    lines = []
    for classcode in sorted(records.keys()):
        for file_index in sorted(records[classcode].keys()):
            data = records[classcode][file_index]['data']
            filename = records[classcode][file_index]['filename']
            line = [classcode, file_index, filename]
            line.extend(map(lambda value: str(value), data))
            lines.append(line)
    exact_path = os.path.abspath(path)
    dirname = os.path.dirname(exact_path)
    prepareDirectory(dirname)
    if os.path.isfile(exact_path):
        os.chmod(exact_path, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
    with open(exact_path, 'w+') as record_file:
        lines = map(lambda line: "-->".join(line) + '\n', lines)
        record_file.writelines(lines)
    os.chmod(exact_path, stat.S_IRUSR|stat.S_IRGRP|stat.S_IROTH)
            
        
            
        
    
    
                
                
              
                    
                    
         	
