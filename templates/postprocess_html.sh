#!/bin/bash

# Post-processing HTML files after nbconvert:
# - Setting up title page
# - Fixing text-justify and image paths

if [[ -z $1 ]];
then 
    mode=4 # if run without parameter, choose mode 4
else
    mode=$1
fi

study_area_humanreadable=$(grep "study_area_humanreadable:" config.yml | cut -d'"' -f 2)
study_area_humanreadable=${study_area_humanreadable##study_area_humanreadable: }
study_area=$(grep "study_area:" config.yml | cut -d'"' -f 2)
study_area=${study_area##study_area: }

# Titlepage
cp templates/titlepage_template.html exports/"$study_area"/html/titlepage.html
sed -i "" -e "s/\[study_area_humanreadable\]/${study_area_humanreadable}/g" exports/"$study_area"/html/titlepage.html
sed -i "" -e "s/\[timestamp\]/$(date "+%Y-%m-%d %H:%M:%S")/g" exports/"$study_area"/html/titlepage.html
if [ $mode == 1 ];
then
	analysistype="Intrinsic Assessment of OpenStreetMap"
elif [ $mode == 2 ];
then
	analysistype="Intrinsic Assessment of"
else
	analysistype="Intrinsic \&amp; Extrinsic Assessment of"
fi
sed -i "" -e "s/\[analysistype\]/$analysistype/g" exports/"$study_area"/html/titlepage.html

# Preamble
sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/preamble.html
sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/preamble.html

if [ $mode == 1 ];
then
	cp results/OSM/"$study_area"/maps_static/titleimage.png exports/"$study_area"/html/titleimage.png
elif [ $mode == 2 ];
then
	cp results/REFERENCE/"$study_area"/maps_static/titleimage.png exports/"$study_area"/html/titleimage.png
else
	cp results/COMPARE/"$study_area"/maps_static/titleimage.png exports/"$study_area"/html/titleimage.png
fi

# Single notebooks
if [ $mode == 1 ] || [ $mode == 3 ] || [ $mode == 4 ]; 
then
	# OSM notebooks
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/1a.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/1a.html
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/1b.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/1b.html
fi

if [ $mode == 2 ] || [ $mode == 3 ] || [ $mode == 4 ]; 
then
	# REFERENCE notebooks
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/2a.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/2a.html
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/2b.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/2b.html
fi

# COMPARE notebooks
if [ $mode == 3 ] || [ $mode == 4 ]; 
then
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/3a.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/3a.html
fi

if [ $mode == 4 ]; 
then
	sed -i "" -e "s/text-align: left/text-align: justify/g" exports/"$study_area"/html/3b.html
	sed -i "" -e "s/src='..\/..\/images\//src='..\/..\/..\/images\//g" exports/"$study_area"/html/3b.html
fi
