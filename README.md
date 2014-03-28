train-ocr
=========

This repository provides code and data that can be used to train custom license plate fonts in support of the OpenALPR library.

The OCR library used by OpenALPR is Tesseract.  Many of the tedious aspects of OCR training have been automated via a Python script.  However, the input data still needs to be in a specific format to satisfy Tesseract.

For more information about training using Tesseract OCR, please read this tutorial: https://code.google.com/p/tesseract-ocr/wiki/TrainingTesseract3

To get started, first clone the repository and get familiar with the input files.  In the "eu/input" folder, there are a number of tif files and box files.  Each "font" will have at least one tif and box file.  A country's license plate may have many fonts, each one would just use a different name.

The naming convention is:
l[country_code].[fontname].exp[pagenumber].box

For example, the European German license plate font would look like:
leu.germany.exp0.box

Open up a tif file.  Notice, these are a series of similar looking letters and numbers.  The best way to generate these is from actual license plate images.  OpenALPR has a couple utilities to help generate these input files.  The first step is to find many pictures of your license plates.  Make sure to separate them by font.  Sometimes, even within a single region, the license plate fonts will vary (e.g., between old plates and new plates, or digital vs stamped plates, or vehicle plates vs bicycle plates).  Each unique font should be a different file in order to achieve the highest accuracy.

Adding a new Country
--------------------
If you plan on training OCR for a completely new country, you will first need to configure the dimensions of the plate and characters.  Find the openalpr.conf file in your runtime_data directory.  Create a new country by adding a [countrycode] section.  You can copy and paste a section from another country (e.g., us or eu).  

You should tweak the following values:

  - plate_width_mm = [width of full plate in mm]
  - plate_height_mm = [height of full plate in mm]
  - char_width_mm = [width of a single character in mm]
  - char_height_mm = [height of a single character in mm]
  - char_whitespace_top_mm = [whitespace between the character and the top of the plate in mm]
  - char_whitespace_bot_mm = [whitespace between the character and the bottom of the plate in mm]
  - template_max_width_px = [maximum width of the plate before processing.  Should be proportional to the plate dimensions]
  - template_max_height_px = [maximum height of the plate before processing.  Should be proportional to the plate dimensions]
  - min_plate_size_width_px = [Minimum size of a plate region to consider it valid.]
  - min_plate_size_height_px = [Minimum size of a plate region to consider it valid.]
  - ocr_language = [name of the OCR language -- typically just the letter l followed by your country code]


Classifying Characters
----------------------

You should gather a large library of license plate images.  Generally, more images will give you greater accuracy.  Each image should be at least 250px wide and should be cropped right on the license plate.  The imageclipper program (separate repo) is helpful for quickly cropping large numbers of images.  Save them as png files.

Each file should be prefaced with a two character identifier for the font/region.  For example, for Maryland plates, we would name the file:
*md*plate1.png

Create an empty output directory.

To start classifying characters, use the classifychars utility program included in OpenALPR.  Before running it, make sure you edit the following line in the classifychars.cpp program to match your country.
  Config* config = new Config("us");
  
Execute the command:
  classifychars [input image directory] [empty output directory]

A GUI will open up and analyze each license plate image in your input folder.  The steps to classify each plate are:
  1. Press the "Enter" key and type the letter or number for each position that you wish to classify.  Pressing 'Space' will skip the character.
  2. Use the arrow keys and press 'Space' to select the rendering that you wish to extract characters for.  The box will be highlighted in blue if it is selected.  For each plate, there may be good characters and bad characters.  You want to pick the best characters, since significant imperfections may confuse the OCR.
  3. Press the 's' key to save each character as a separate file in your out folder.
  4. Press the 'n' key to move onto the next plate and repeat this process until you've classified all the plates.


Building a Tesseract Training Sheet
-----------------------------------

Once you've classified all the characters, it may be a good idea to scan through the directory to make sure that the classifications match the images.  Each image filename should be prefaced with the character that it represents.  Once you've done this, it's time to create a training sheet.

The "prepcharsfortraining" utility program in OpenALPR will create the Tesseract training sheet for you.  Execute the following command:
prepcharsfortraining [output directory from above]

The output will be:
  - combined.box
  - combined.tif

Rename these files to match the naming convention used by Tesseract (explained above).  For example, leu.germany.exp0.box

You should create a training sheet for each unique license plate font that you wish to train.

Training the OCR
----------------

Lastly, you'll use the box/tif files created above to train your country's license plate OCR.  Create a new directory using your country code, and create an input directory within it.  Copy all the box/tif files created in the previous steps into this directory.

Execute the "train.py" file.  Type in your country code.

If all went well, you should have a new file named l[countrycode].traineddata.  Copy this file into your runtime_directory (runtime_data/ocr/tessdata/) and it is now ready for OpenALPR to use.

