
'''
Simple python script to rename all files to rename any files to
ECS 193A naming convention.
'''


import argparse

import io
import os
import shutil
import random

def parse_args():
    '''
    Get command line args.
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', required=True, help='path to \
            directory with images', dest='dir')

    parser.add_argument('--newdir', required=True, help='path to \
            new directory with renamed images', dest='new_dir')

    parser.add_argument('--start', required=True, help='naming \
            starting number', dest='num_start', type=int)

    args = parser.parse_args()

    return args

def rename(files, nums_start):
    '''
    Renames the files in a directory.
    '''

def main():

    args = parse_args()

    try:
        files = os.listdir(args.dir)
    except NotADirectoryError:
        print("No such directory ", args.dir)
        raise

    new_directory = args.new_dir
    
    # randomize the files
    random.shuffle(files)
    
    #os.mkdir(new_directory)
    shutil.copytree(args.dir, new_directory)

    current_index = args.num_start

    for file in files:
        full_name = os.path.join(new_directory, file)
        new_name = os.path.join(new_directory, 'IMG_' + \
                str(current_index) + '.jpg')

        current_index += 1
        os.rename(full_name, new_name)

    print("Rename successful!")

if __name__== "__main__":
  main()
