#!/usr/bin/env python

import os
import sys
import pandas as pd
import getopt
import shutil


def eprint(*args, **kwargs):
    '''
    Error message handling. Print to stderr.
    '''
    print(*args, file=sys.stderr, **kwargs)


def usage():
    '''
    Print usage info
    '''
    print("rename.py -n new_name_file.txt -i /path/to/images/ -p prefix -d")
    print("\t-n / --newname=\tFile with tab delimited columns")
    print("\t\told_name\tnew_name")
    print("\t\txxx.jpg\txxx_yyy.jpg")
    print("\t-w\t\tWrite a template file with current images \n\t\t\tnames and empty second column")
    print("\t-i / --input=\tFile path to images")
    print("\t-t / --type=\tSpecify image file ending")
    print("\t-p / --prefix=\tPrefix for file name")
    print("\t-d\t\tDry running the script")
    sys.exit()


def input_data():
    '''
    Parse the commandline input:
      - '-n' new name file with two tab delimited columns
        File example:
            old_name    new_name
            xxx.jpg xxx_yyy.jpg

      - '-w' write a template file to add the names (depends on -i) 

      - '-i' image folder path
        Path example:
            /home/user/images/
      
      - '-t' image type e.g. .jpg, .tiff...

      - '-p' prefix; will be added at beginning of file name
        Prefix example:
            prefix_xxx_yyy.jpg

      - '-d' dry run the renaming for your convenience 
    '''

    # If command line input is of length 1 quit
    if len(sys.argv) == 1:
        usage()
    
    # Define the possible input flags
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:i:p:t:dwq", ["newname=", "input=", "prefix=", "type="])
    except getopt.GetoptError as err:
        eprint("[error]\t{}".format(err))
        usage()
    
    image_path = ""
    img_type = ""
    prefix = ""
    write_template = False
    dryrun = False
    quiet = False
    
    for o, a in opts:
        if o in ("-n", "--newname"):
            newname_file = a
        if o in ("-i", "--input"):
            image_path = a
        if o in ("-p", "--path"):
            prefix = a
        if o in ("-t", "--type"):
            img_type = a
        if o in ("-d"):
            dryrun = True
        if o in ("-w"):
            write_template = True
        if o in ("-q"):
            quiet = True
    
    if image_path == "":
        eprint("[error]\tNo path to images.")
        usage()
    
    if img_type == "":
        eprint("[error]\tNo image type. don't know what to lookf for.")
        usage()

    # Handle the -w flag and write a template file which can be edited
    if write_template:
        if image_path != "":
            # Get all files from specified path
            image_names = sorted(os.listdir(image_path))
            
            # Get rid of the pesky .DS_Store ...
            count=0
            pop_lst = []
            for name in image_names:
                if name.startswith("."):
                    pop_lst.append(count)
                count = count + 1

            for y in pop_lst:
                image_names.pop(y)

            # Remove all files with wrong file ending
            pop_lst = []
            for x in range(len(image_names)):
                if not image_names[x].endswith(img_type):
                    pop_lst.append(x)

            for z in pop_lst:
                image_names.pop(z)

            # Make an empty list with the same length as the image_names
            new_image_names = [''] * len(image_names)
            
            # Make pandas dataframe
            d = {"old_name" : image_names, "new_name" : new_image_names}
            df = pd.DataFrame(data=d)
            
            # Write the dataframe to file
            df.to_csv(image_path+"new_name_list.tsv", sep="\t", index=False)

            print("[info]\tNew name template file written: {}".format(image_path+"new_name_list.tsv"))
            print("[info]\tEdit it and run the script with -n, -i, -t and optional -p flag.")

            # Exit with 0; succesfully written template file
            sys.exit()
    
    else:
        # Read in the adjusted new name template file from option '-w'
        # Data will be stored as a dictonary:
        #   {old_name : new_name, ...}
        with open(newname_file, 'r') as file:
            newname_file_dict = {}
            for line in file:
                newname_file_dict[line.rstrip().split("\t")[0]]=line.rstrip().split("\t")[1]
        
        del newname_file_dict["old_name"]

        # Make sure that the path is formatted propperly
        if image_path == ".":
            image_path = "./"
        
        # Read in the images in the supplied folder. Remove all non
        # img_type images from the list.
        image_names = sorted(os.listdir(image_path))

        count=0
        pop_lst = []
        for name in image_names:
            if name.startswith("."):
                pop_lst.append(count)
            count = count + 1

        for w in pop_lst:
            image_names.pop(w)
            
        pop_lst = []
        for x in range(len(image_names)):
            if not image_names[x].endswith(img_type):
                pop_lst.append(x)
        
        for z in pop_lst:
            image_names.pop(z)
        
        if len(image_names) == 0:
            print("[error]\tNo images to rename in {}. Maybe check file ending.".format(image_path))
        
        return image_path, image_names, newname_file_dict, prefix, dryrun, quiet


def main():
    '''
    Run the main part of the script
    '''
    image_path, image_names, newname_file_dict, prefix, dryrun, quiet = input_data()

    print("[info]\tPath to images: {}".format(image_path))
    print("[info]\tNumber of images: {}".format(len(image_names)))
    print("[info]\tImages to rename: {}".format(len(newname_file_dict)))
    print("[info]\tAdding prefix to image: {}".format(prefix))
    if dryrun:
        print("[info]\tDry run.")

    # Create the output directory
    if not dryrun:
        try:
            os.mkdir(image_path + "renamed_images/")
        except OSError as err:
            print("[error]\tWhile creating the output directory an error was encountered.")
            eprint("{}".format(err))
            sys.exit(1)
   
    if not quiet:
        print("[info]\tRenaming:")
        print("Old_name\tNew_name\tPath")

    for name in image_names:
        if not quiet:
            print("{0}\t{1}\t{2}".format(name, newname_file_dict[name], image_path + "renamed_images/"+prefix+"_"+newname_file_dict[name]))

        if not dryrun:
            if prefix != "":
                shutil.copy(image_path+name, image_path+"renamed_images/"+prefix+"_"+newname_file_dict[name])
            else:
                shutil.copy(image_path+name, image_path+"renamed_images/"+newname_file_dict[name])
    
    print("[info]\tRenamed images copied to {}".format(image_path+"renamed_images/"))
    

if __name__ == '__main__':
    main()
