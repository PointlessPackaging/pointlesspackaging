import argparse
import io
import os
import sys
import shutil
import cv2

width = 300
accpted_extensions = ['.jpg', '.jpeg', '.png', '.gif']

description = "Simple script that takes a directory of images and resizes them to width of " + str(width) + "px while still maintaining the aspect ratio."

def parse_args():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--src', required=True, help='Path to the directory with source images', dest='src')
    parser.add_argument('--dest', required=False, help='[Optional] New target directory. If supplied, a new directory will be created and all images will be copied and resized in this directory.', dest='dest')

    return parser.parse_args()

def query_yes_no():
    print("\n* You have NOT specified a destination.\nThe script will rewrite images to the same directory and original images will not be saved.\nAre you sure you want to continue?\n")
    
    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}
    print("Please respond with 'y' or 'n':", end=' ')
    while True:
        choice = input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond with 'y' or 'n':", end=' ')

def main():
    args = parse_args()
    source_dir = args.src # source directory name
    dest_dir = args.dest # destination directory name
    op_dir = source_dir # operation directory

    if os.path.isdir(source_dir) == False:
        print("Please enter a valid source directory.")
        raise NotADirectoryError

    if dest_dir == None and query_yes_no() == False:
        print("Script aborted.")
        raise SystemExit
        
    if dest_dir != None:
        """ Copy all files from source to destination directory """
        shutil.copytree(source_dir, dest_dir)
        op_dir = dest_dir

    try:
        """ Get all files in the copied directory """
        files = os.listdir(op_dir)
    except NotADirectoryError:
        print("Invalid source directory", op_dir)
        raise
    
    """ Check if absolute path """
    file_path = ''
    if os.path.isabs(op_dir) == False:
        file_path = './' + op_dir + '/'

    resized = 0
    total_img = 0

    for file in files:
        img_name = file_path+file
        if os.path.splitext(img_name)[1] in accpted_extensions: # check if image is jpg, png
            img = cv2.imread(img_name)
            orig_dim = img.shape
            total_img += 1
            if orig_dim[0] < 301:
                print("Did not resize", file, "with dimensions", orig_dim[:2])
                continue
            new_dim = (int((width/orig_dim[0]) * orig_dim[1]), width)
            resized_img = cv2.resize(img, new_dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite(img_name, resized_img)
            resized += 1
            print("Resized", file, "from", orig_dim[:2], "->", resized_img.shape[:2])
    
    print(f"\nImages Resized: {resized} out of {total_img} images.")
    print("Done!")

if __name__ == "__main__":
    main()
