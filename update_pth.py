#! /usr/bin/python

import argparse
import glob
import os
import sys

def get_contents(yml_dir):
    yml_file = open(yml_dir)
    lines = yml_file.readlines()
    yml_file.close()
    return lines
    
def get_pth_files(pth_dir):
    pth_files = [os.path.basename(x) for x in glob.glob(pth_dir)]
    pth_files.sort()
    return pth_files

def init(yml_dir, pth_dir, netG):
    lines = get_contents(yml_dir)
    pth_files = get_pth_files(pth_dir)

    default = "    NET_G: '../models/birds_3stages/{}'\n"
    for i in range(len(lines)):
        if "/netG_" in lines[i]:
            try:
                init_pth = netG if netG in pth_files else pth_files[0]
                lines[i] = default.format(init_pth)
                
                yml_file = open(yml_dir, "w")
                new_file_contents = "".join(lines)

                yml_file.write(new_file_contents)
                yml_file.close()

                return init_pth[5:11]
            except:
                return None


def update(yml_dir, pth_dir):
    lines = get_contents(yml_dir)
    pth_files = get_pth_files(pth_dir)

    default = "    NET_G: '../models/birds_3stages/{}'\n"
    for i in range(len(lines)):
        if "/netG_" in lines[i]:
            index = lines[i].find("netG_")
            prev_pth = lines[i][index:index+15]
            try:
                prev_pth_i = pth_files.index(prev_pth)
            except:
                prev_pth_i = -1
                
            try:
                next_pth = pth_files[prev_pth_i+1]
                lines[i] = default.format(next_pth)
                
                yml_file = open(yml_dir, "w")
                new_file_contents = "".join(lines)

                yml_file.write(new_file_contents)
                yml_file.close()

                return next_pth[5:11]
            except:
                return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Automate Test")
    parser.add_argument("-n", "--netG", dest="netG", default='netG_200000')
    parser.add_argument("-m", "--mode", dest="mode", default='update')
    parser.add_argument("-d", "--base_dir", dest="base_dir", default="/home/monash/Desktop/StackGAN-v2-master/code")

    args = parser.parse_args()
    yml_dir = args.base_dir + "/cfg/eval_birds.yml"
    pth_dir = args.base_dir + "/../models/birds_3stages/*.pth"
    
    if args.mode.lower() == "update":
        print(update(yml_dir, pth_dir))
    elif args.mode.lower() == "init":
        print(init(yml_dir, pth_dir, args.netG))
    
    