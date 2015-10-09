#!/usr/bin/python

import os
import glob
import sys


TESSERACT_DIR='/storage/projects/alpr/libraries/tesseract-ocr'

os.environ["TESSDATA_PREFIX"] = TESSERACT_DIR
#os.system("export TESSDATA_PREFIX=" + TESSERACT_DIR)

TESSERACT_BIN=TESSERACT_DIR + '/tesseract'
TESSERACT_TRAINDIR= TESSERACT_DIR + '/training'


country = raw_input("Two-Letter Country Code to Train: ").lower()

LANGUAGE_NAME='l' + country

box_files = glob.glob('./' + country + '/input/*.box')
if not box_files:
    print "Cannot find input files"
    sys.exit(1)

os.system("rm ./tmp/*")

font_properties_file = open('./tmp/font_properties','w')

for box_file in box_files:
    print "Processing: " + box_file

    file_without_dir = os.path.split(box_file)[1]
    file_without_ext = os.path.splitext(file_without_dir)[0]
    input_dir = os.path.dirname(box_file)

    tif_file = input_dir + '/' + file_without_ext + ".tif"

    train_cmd = "%s -l eng %s %s nobatch box.train.stderr" % (TESSERACT_BIN, tif_file, file_without_ext)
    print "Executing: " + train_cmd 
    os.system(train_cmd)
    os.system("mv ./" + file_without_ext + ".tr ./tmp/" + file_without_ext + ".tr")
    os.system("mv ./" + file_without_ext + ".txt ./tmp/" + file_without_ext + ".txt")

    font_name=file_without_dir.split('.')[1]
    font_properties_file.write(font_name + ' 0 0 1 0 0\n')

font_properties_file.close()

os.system(TESSERACT_TRAINDIR + "/unicharset_extractor ./" + country + "/input/*.box")
#os.system('mv ./unicharset ./" + country + "/input/" + LANGUAGE_NAME + ".unicharset')

# Shape clustering should currently only be used for the "indic" languages
#train_cmd = TESSERACT_TRAINDIR + '/shapeclustering -F ./' + country + '/input/font_properties -U unicharset ./' + country + '/input/*.tr'
#print "Executing: " + train_cmd
#os.system(train_cmd)


train_cmd = TESSERACT_TRAINDIR + '/mftraining -F ./tmp/font_properties -U unicharset -O ./tmp/' + LANGUAGE_NAME + '.unicharset ./tmp/*.tr'
print "Executing: " + train_cmd
os.system(train_cmd)
os.system("rm ./unicharset")
os.system("mv ./tmp/" + LANGUAGE_NAME + ".unicharset ./")
os.system("cp ./" + country + "/input/unicharambigs ./" + LANGUAGE_NAME + ".unicharambigs")


os.system(TESSERACT_TRAINDIR + '/cntraining ./tmp/*.tr')

#os.system("mv ./unicharset ./" + LANGUAGE_NAME + ".unicharset")
os.system("mv ./shapetable ./" + LANGUAGE_NAME + ".shapetable")
#os.system("rm ./shapetable")
os.system("mv ./pffmtable ./" + LANGUAGE_NAME + ".pffmtable")
os.system("mv ./inttemp ./" + LANGUAGE_NAME + ".inttemp")
os.system("mv ./normproto ./" + LANGUAGE_NAME + ".normproto")


os.system(TESSERACT_TRAINDIR + '/combine_tessdata ' + LANGUAGE_NAME + '.')

# If a config file is in the country's directory, use that.
config_file = os.path.join('./', country, country + '.config')
if os.path.isfile(config_file):
    print "Applying config file: " + config_file
    trainedata_file = LANGUAGE_NAME + '.traineddata'
    os.system(TESSERACT_TRAINDIR + '/combine_tessdata -o ' + trainedata_file + ' ' + config_file )

os.system("mv ./" + LANGUAGE_NAME + ".unicharset ./tmp/")
os.system("mv ./" + LANGUAGE_NAME + ".shapetable ./tmp/")
os.system("mv ./" + LANGUAGE_NAME + ".pffmtable ./tmp/")
os.system("mv ./" + LANGUAGE_NAME + ".inttemp ./tmp/")
os.system("mv ./" + LANGUAGE_NAME + ".normproto ./tmp/")
os.system("mv ./" + LANGUAGE_NAME + ".unicharambigs ./tmp/")
