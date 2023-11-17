# rename.py
Rename images in a given folder with a given list of names. In addition a prefix can be supplied which will be added at the begining of each file.

The script has the following options:

```bash 
(base) 💻 daniel:rename_pics $ python rename.py 
rename.py -n new_name_file.txt -i /path/to/images/ -p prefix -d
        -n / --newname= File with tab delimited columns
                old_name        new_name
                xxx.jpg xxx_yyy.jpg
        -w              Write a template file with current images 
                        names and empty second column
        -i / --input=   File path to images
        -t / --type=    Specify image file ending
        -p / --prefix=  Prefix for file name
        -d              Dry running the script
```

## How to use it:

1. Run the script with the **-w** flag (his requires the flags **-i** and **-t**)

```bash 
(base) 💻 daniel:rename_pics $ python rename.py -w -t .JPG -i test/
[info]  New name template file written: test1/new_name_list.tsv
[info]  Edit it and run the script with -n, -i, -t and optional -p flag.
```

This generates a new_name_list.tsv file which you can edit with your favorite spreadsheet application.
Just add the new desired name into the second column "New_name" and your set.

|Old_name|New_name|
|--------|--------|
|xxx.JPG |xxx_yyy.JPG|

2. Run the script as indicated with the flags **-n**, **-i**, **-t** and optional **-p**.
By adding -q you silence the majority of the output. By adding -d the script will only print what it is going to do.
You can check if everything is according to your likes. Once you're happy just run the script without -d.

```bash
(base) 💻 daniel:rename_pics $ python rename.py -n new_name_list.tsv -i test1/ -t .JPG -p 7dpi -q
[info]  Path to images: test1/
[info]  Number of images: 103
[info]  Images to rename: 103
[info]  Adding prefix to image: 7dpi
[info]  Renamed images copied to test1/renamed_images/
```


