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
If you plan on training OCR for a completely new country, you will first need to configure the dimensions of the plate and characters.  Add a new file in runtime_data/config/ with your country's 2-digit code.  You can copy and paste a section from another country (e.g., us or eu).  

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

Understanding Your Country's Plates
------------------------
The first thing you need to know is how many fonts your country's license plates have.  In the US, for example, many states use very different fonts for their plates.  Some countries only use one font.  Here is an example of New York and West Virginia,.  Notice how different the "6" character is in both plates:

![ny](https://cloud.githubusercontent.com/assets/508260/7515059/78f64494-f491-11e4-9795-aef6b9100cd2.jpg)
![wv](https://cloud.githubusercontent.com/assets/508260/7515062/7c0fb5ac-f491-11e4-9bff-42e082995c45.jpg)

Each font needs to be trained separately.  You do not want to combine characters across fonts, this will greatly decrease your accuracy.  After each font is trained, they can be combined into one dataset for your entire country.

Creating the character tiles
----------------------------
Once you're ready to start training, you'll need to create a library of character tiles.  Each tile is a small image file that contains the black-and-white character and is named after the character.  For example, here are a few character tile examples:

![-0-0-2](https://cloud.githubusercontent.com/assets/508260/7515148/5b3711da-f492-11e4-96c2-1f62778450f4.png)
부-0-0-2.png

![0-0-az2012fighthunger](https://cloud.githubusercontent.com/assets/508260/7515157/731716ba-f492-11e4-9d78-a5c98e8f025b.jpg)
0-0-az2012.png

![c-1-az2012fallendisabled](https://cloud.githubusercontent.com/assets/508260/7515159/819e92f8-f492-11e4-9d79-7a865be9ec46.jpg)
c-1-az2012.png

![d-9-azpermsunddevil](https://cloud.githubusercontent.com/assets/508260/7515229/2e877890-f493-11e4-9c7c-5a193e9cefef.jpg)
d-9-az2012.jpg

![d-9-azpermuscan](https://cloud.githubusercontent.com/assets/508260/7515228/2e8567c6-f493-11e4-823b-2e8c7f035389.jpg)
d-9-2-az2012.jpg

You will want many of these character tiles for each character and each font.  The character tiles are all going to be slightly different, this is necessary for the OCR training to understand how to detect characters.  Notice in the above examples, the "D" characters have pixels located in different places, but they're clearly the same character.

Producing Tiles
----------------
There are two good ways to produce character tiles.

  1. Use actual images from license plates
  2. Use a TTF font that looks like the license plate font

Producing Tiles from Actual Plates
----------------------

You should gather a large library of license plate images (At least 100).  These license plate images should be cropped around the plate and the aspect ratio should match your configured width/height for your license plates.  Make sure each image is at least 250px wide.  The imageclipper program (separate repo) is helpful for quickly cropping large numbers of images.  Save them as png files.

Each file should be prefaced with a two character identifier for the font/region.  For example, for Maryland plates, we would name the file:
*md*plate1.png

Create an empty output directory.

To start classifying characters, use the classifychars utility program included in OpenALPR.

Execute the command:
  classifychars [country] [input image directory] [empty output directory]

A GUI will open up and analyze each license plate image in your input folder.  The steps to classify each plate are:
  1. Press the "Enter" key and type the letter or number for each position that you wish to classify.  Pressing 'Space' will skip the character.
  2. Use the arrow keys and press 'Space' to select the rendering that you wish to extract characters for.  The box will be highlighted in blue if it is selected.  For each plate, there may be good characters and bad characters.  You want to pick the best characters, since significant imperfections may confuse the OCR.
  3. Press the 's' key to save each character as a separate file in your out folder.
  4. Press the 'n' key to move onto the next plate and repeat this process until you've classified all the plates.

Producing Tiles from a TTF Font
-------------------------------
A TTF font can be used to produce tiles.  However, we need to add some realistic distortion to the characters.  This is necessary to make a robust OCR detector.

The process is as follows:

  1. Figure out all the characters that could possibly be in a license plate.
  2. Create a word document with all of these characters.  Make sure there is plenty of spacing between lines and characters.
  3. Copy and paste all of these characters to a text file (no spaces or line breaks)
  3. Print this word document.
  4. Take a few pictures (5 would be sufficient) of the word document with a digital camera.  Vary the angle/rotation very slightly (1-2 degrees) with each picture.
  5. Save the pictures to a folder.
  6. Run the openalpr-utils-binarizefontsheet program to produce tiles from each of the images.  Provide the program with the text file from step #3 and each image file.


Building a Tesseract Training Sheet
-----------------------------------

Once you've classified all the characters, it may be a good idea to scan through the directory to make sure that the classifications match the images.  Each image filename should be prefaced with the character that it represents.  Once you've done this, it's time to create a training sheet.

The "openalpr-utils-prepcharsfortraining" utility program in OpenALPR will create the Tesseract training sheet for you.  Execute the following command:
openalpr-utils-prepcharsfortraining [output directory from above]

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

Tesseract may report issues.  Most commonly it will complain that it could not line up the boxes on the provided image.  If you are getting many of these warnings, you can re-run the openalpr-utils-prepcharsfortraining utility and provide values for --tile_width and --tile_height.  Using different values will change how Tesseract sees the image and potentially improve results.
